"""High-level synchronous PTY support for devboxes."""

from __future__ import annotations

import time
import uuid
import queue
import codecs
import threading
from typing import Any, Callable, Iterator
from importlib import import_module
from urllib.parse import urljoin, urlparse, urlunparse

from .._types import omit
from .._client import Runloop
from .._exceptions import APIStatusError

BytesCallback = Callable[[bytes], None]
TextCallback = Callable[[str], None]
_CLOSE_SENTINEL = object()
_RETRY_STATUS_CODES = {502, 503}
_ACCEPTABLE_CLOSE_CODES = {1000, 1006, 4000}


def _sleep_for_attempt(attempt: int) -> None:
    time.sleep(min(0.25 * (2**attempt), 2.0))


def _is_retryable_status_error(exc: BaseException) -> bool:
    return isinstance(exc, APIStatusError) and exc.status_code in _RETRY_STATUS_CODES


def _is_retryable_ws_error(exc: BaseException) -> bool:
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if status in _RETRY_STATUS_CODES:
        return True
    response = getattr(exc, "response", None)
    return getattr(response, "status_code", None) in _RETRY_STATUS_CODES


def _base_domain(client: Runloop) -> str:
    host = client.base_url.host
    return host[4:] if host.startswith("api.") else host


def _tunnel_base_url(client: Runloop, tunnel_key: str) -> str:
    return f"https://13-{tunnel_key}.tunnel.{_base_domain(client)}"


def _websocket_url(base_url: str, connect_url: str) -> str:
    parsed = urlparse(urljoin(f"{base_url.rstrip('/')}/", connect_url.lstrip("/")))
    scheme = "wss" if parsed.scheme == "https" else "ws"
    return urlunparse(parsed._replace(scheme=scheme))


def _close_websocket(ws: Any) -> None:
    try:
        ws.close()
    except Exception:
        pass


class DevboxPtyOps:
    """High-level PTY operations for a synchronous devbox."""

    def __init__(self, client: Runloop, devbox_id: str) -> None:
        self._client = client
        self._devbox_id = devbox_id

    def open(
        self,
        command: str | None = None,
        *,
        cols: int = 80,
        rows: int = 24,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        retry_attempts: int = 5,
    ) -> "DevboxPtySession":
        tunnel = self._create_tunnel(retry_attempts)
        if not tunnel.auth_token:
            raise RuntimeError("PTY tunnel did not include an auth token")

        base_url = _tunnel_base_url(self._client, tunnel.tunnel_key)
        tunnel_client = Runloop(base_url=base_url, bearer_token=tunnel.auth_token)
        connect = self._connect(tunnel_client, command, cols, rows, cwd, env, retry_attempts)
        ws_url = _websocket_url(base_url, connect.connect_url)
        ws = self._attach(ws_url, tunnel.auth_token, retry_attempts)
        return DevboxPtySession(tunnel_client, ws)

    def exec(
        self,
        command: str,
        *,
        cols: int = 80,
        rows: int = 24,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        retry_attempts: int = 5,
    ) -> "DevboxPtyProcess":
        marker = f"__RUNLOOP_PTY_EXIT_{uuid.uuid4().hex}__"
        session = self.open("/bin/sh", cols=cols, rows=rows, cwd=cwd, env=env, retry_attempts=retry_attempts)
        wrapped = (
            f"{command}\n"
            "__runloop_status=$?\n"
            f"printf '\\n{marker}:%s\\n' \"$__runloop_status\"\n"
            "exit \"$__runloop_status\"\n"
        )
        process = DevboxPtyProcess(session, marker)
        session.send(wrapped)
        return process

    def _create_tunnel(self, retry_attempts: int) -> Any:
        for attempt in range(retry_attempts):
            try:
                return self._client.devboxes.create_pty_tunnel(self._devbox_id)
            except Exception as exc:
                if attempt == retry_attempts - 1 or not _is_retryable_status_error(exc):
                    raise
                _sleep_for_attempt(attempt)
        raise RuntimeError("unreachable")

    def _connect(
        self,
        tunnel_client: Runloop,
        command: str | None,
        cols: int,
        rows: int,
        cwd: str | None,
        env: dict[str, str] | None,
        retry_attempts: int,
    ) -> Any:
        for attempt in range(retry_attempts):
            try:
                return tunnel_client.pty.connect(
                    command=command if command is not None else omit,
                    cols=cols,
                    rows=rows,
                    cwd=cwd if cwd is not None else omit,
                    env=env if env is not None else omit,
                )
            except Exception as exc:
                if attempt == retry_attempts - 1 or not _is_retryable_status_error(exc):
                    raise
                _sleep_for_attempt(attempt)
        raise RuntimeError("unreachable")

    def _attach(self, ws_url: str, auth_token: str, retry_attempts: int) -> Any:
        websocket = import_module("websocket")
        for attempt in range(retry_attempts):
            try:
                return websocket.create_connection(ws_url, header=[f"Authorization: Bearer {auth_token}"])
            except Exception as exc:
                if attempt == retry_attempts - 1 or not _is_retryable_ws_error(exc):
                    raise
                _sleep_for_attempt(attempt)
        raise RuntimeError("unreachable")


class DevboxPtySession:
    """Attached PTY session."""

    def __init__(self, tunnel_client: Runloop, websocket: Any) -> None:
        self._client = tunnel_client
        self._ws = websocket
        self._raw_callbacks: list[BytesCallback] = []
        self._text_callbacks: list[TextCallback] = []
        self._queue: queue.Queue[bytes | object] = queue.Queue()
        self._closed = threading.Event()
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    @property
    def raw_output(self) -> Iterator[bytes]:
        while True:
            item = self._queue.get()
            if item is _CLOSE_SENTINEL:
                return
            yield item  # type: ignore[misc]

    @property
    def output(self) -> Iterator[str]:
        decoder = codecs.getincrementaldecoder("utf-8")()
        for chunk in self.raw_output:
            text = decoder.decode(chunk)
            if text:
                yield text
        tail = decoder.decode(b"", final=True)
        if tail:
            yield tail

    def on_data(self, callback: BytesCallback) -> None:
        self._raw_callbacks.append(callback)

    def on_output(self, callback: TextCallback) -> None:
        self._text_callbacks.append(callback)

    def send(self, data: str | bytes) -> None:
        payload = data.encode("utf-8") if isinstance(data, str) else data
        self._ws.send_binary(payload)

    def resize(self, cols: int, rows: int) -> None:
        if cols <= 0 or rows <= 0:
            raise ValueError("cols and rows must be positive")
        self._client.pty.control(action="resize", cols=cols, rows=rows)

    def signal(self, signal: str) -> None:
        if not signal:
            raise ValueError("signal must be non-empty")
        self._client.pty.control(action="signal", signal=signal)

    def detach(self) -> None:
        _close_websocket(self._ws)
        self.wait_for_close()

    def close(self) -> None:
        self.detach()

    def terminate(self) -> None:
        try:
            self._client.pty.control(action="close")
        finally:
            self.detach()

    def wait_for_close(self, timeout: float | None = None) -> bool:
        closed = self._closed.wait(timeout)
        if closed and self._reader.is_alive() and threading.current_thread() is not self._reader:
            self._reader.join(timeout=0)
        return closed

    def _read_loop(self) -> None:
        try:
            while True:
                data = self._ws.recv()
                if data in (None, b"", ""):
                    break
                chunk = data.encode("utf-8") if isinstance(data, str) else bytes(data)
                self._emit(chunk)
        except Exception:
            pass
        finally:
            self._closed.set()
            self._queue.put(_CLOSE_SENTINEL)

    def _emit(self, chunk: bytes) -> None:
        self._queue.put(chunk)
        for raw_callback in list(self._raw_callbacks):
            raw_callback(chunk)
        text = self._decoder.decode(chunk)
        if text:
            for text_callback in list(self._text_callbacks):
                text_callback(text)


class DevboxPtyProcess:
    """PTY-backed command process."""

    def __init__(self, session: DevboxPtySession, exit_marker: str) -> None:
        self._session = session
        self._exit_marker = exit_marker.encode("ascii")
        self._raw_callbacks: list[BytesCallback] = []
        self._text_callbacks: list[TextCallback] = []
        self._queue: queue.Queue[bytes | object] = queue.Queue()
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._pending = b""
        self._exit_code: int | None = None
        self._done = threading.Event()
        session.on_data(self._handle_data)

    @property
    def raw_output(self) -> Iterator[bytes]:
        while True:
            item = self._queue.get()
            if item is _CLOSE_SENTINEL:
                return
            yield item  # type: ignore[misc]

    @property
    def output(self) -> Iterator[str]:
        decoder = codecs.getincrementaldecoder("utf-8")()
        for chunk in self.raw_output:
            text = decoder.decode(chunk)
            if text:
                yield text
        tail = decoder.decode(b"", final=True)
        if tail:
            yield tail

    @property
    def exit_code(self) -> int | None:
        return self._exit_code

    def on_data(self, callback: BytesCallback) -> None:
        self._raw_callbacks.append(callback)

    def on_output(self, callback: TextCallback) -> None:
        self._text_callbacks.append(callback)

    def write(self, chars: str | bytes) -> None:
        self._session.send(chars)

    def resize(self, cols: int, rows: int) -> None:
        self._session.resize(cols, rows)

    def interrupt(self) -> None:
        self._session.signal("SIGINT")

    def close(self) -> None:
        self._session.terminate()

    def wait(self, timeout: float | None = None) -> int | None:
        self._done.wait(timeout)
        if self._exit_code is None:
            self._session.wait_for_close(timeout=0)
        return self._exit_code

    def _handle_data(self, chunk: bytes) -> None:
        if self._done.is_set():
            return
        self._pending += chunk
        marker_index = self._pending.find(self._exit_marker)
        if marker_index >= 0:
            self._publish(self._pending[:marker_index])
            rest = self._pending[marker_index + len(self._exit_marker) :]
            if rest.startswith(b":"):
                digits = bytearray()
                for byte in rest[1:]:
                    if 48 <= byte <= 57:
                        digits.append(byte)
                    else:
                        break
                if digits:
                    self._exit_code = int(digits.decode("ascii"))
            self._pending = b""
            self._done.set()
            self._queue.put(_CLOSE_SENTINEL)
            return

        keep = len(self._exit_marker) + 32
        if len(self._pending) > keep:
            self._publish(self._pending[:-keep])
            self._pending = self._pending[-keep:]

    def _publish(self, chunk: bytes) -> None:
        if not chunk:
            return
        self._queue.put(chunk)
        for raw_callback in list(self._raw_callbacks):
            raw_callback(chunk)
        text = self._decoder.decode(chunk)
        if text:
            for text_callback in list(self._text_callbacks):
                text_callback(text)
