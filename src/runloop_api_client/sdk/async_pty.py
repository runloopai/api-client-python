"""High-level asynchronous PTY support for devboxes."""

from __future__ import annotations

import uuid
import codecs
import asyncio
import inspect
from typing import Any, Union, Callable, Awaitable, AsyncIterator, cast
from importlib import import_module
from urllib.parse import urljoin, urlparse, urlunparse

from .._types import omit
from .._client import AsyncRunloop
from .._exceptions import APIStatusError

AsyncBytesCallback = Callable[[bytes], Union[None, Awaitable[None]]]
AsyncTextCallback = Callable[[str], Union[None, Awaitable[None]]]
_CLOSE_SENTINEL = object()
_RETRY_STATUS_CODES = {502, 503}


async def _sleep_for_attempt(attempt: int) -> None:
    await asyncio.sleep(min(0.25 * (2**attempt), 2.0))


def _is_retryable_status_error(exc: BaseException) -> bool:
    return isinstance(exc, APIStatusError) and exc.status_code in _RETRY_STATUS_CODES


def _is_retryable_ws_error(exc: BaseException) -> bool:
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if status in _RETRY_STATUS_CODES:
        return True
    response = getattr(exc, "response", None)
    return getattr(response, "status_code", None) in _RETRY_STATUS_CODES


def _base_domain(client: AsyncRunloop) -> str:
    host = client.base_url.host
    return host[4:] if host.startswith("api.") else host


def _tunnel_base_url(client: AsyncRunloop, tunnel_key: str) -> str:
    return f"https://13-{tunnel_key}.tunnel.{_base_domain(client)}"


def _websocket_url(base_url: str, connect_url: str) -> str:
    parsed = urlparse(urljoin(f"{base_url.rstrip('/')}/", connect_url.lstrip("/")))
    scheme = "wss" if parsed.scheme == "https" else "ws"
    return urlunparse(parsed._replace(scheme=scheme))


async def _maybe_await(result: None | Awaitable[None]) -> None:
    if inspect.isawaitable(result):
        await result


class AsyncDevboxPtyOps:
    """High-level PTY operations for an async devbox."""

    def __init__(self, client: AsyncRunloop, devbox_id: str) -> None:
        self._client = client
        self._devbox_id = devbox_id

    async def open(
        self,
        command: str | None = None,
        *,
        cols: int = 80,
        rows: int = 24,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        retry_attempts: int = 5,
    ) -> "AsyncDevboxPtySession":
        tunnel = await self._create_tunnel(retry_attempts)
        if not tunnel.auth_token:
            raise RuntimeError("PTY tunnel did not include an auth token")

        base_url = _tunnel_base_url(self._client, tunnel.tunnel_key)
        tunnel_client = AsyncRunloop(base_url=base_url, bearer_token=tunnel.auth_token)
        connect = await self._connect(tunnel_client, command, cols, rows, cwd, env, retry_attempts)
        ws_url = _websocket_url(base_url, connect.connect_url)
        ws = await self._attach(ws_url, tunnel.auth_token, retry_attempts)
        return AsyncDevboxPtySession(tunnel_client, ws)

    async def exec(
        self,
        command: str,
        *,
        cols: int = 80,
        rows: int = 24,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        retry_attempts: int = 5,
    ) -> "AsyncDevboxPtyProcess":
        marker = f"__RUNLOOP_PTY_EXIT_{uuid.uuid4().hex}__"
        session = await self.open("/bin/sh", cols=cols, rows=rows, cwd=cwd, env=env, retry_attempts=retry_attempts)
        wrapped = (
            f"{command}\n"
            "__runloop_status=$?\n"
            f"printf '\\n{marker}:%s\\n' \"$__runloop_status\"\n"
            "exit \"$__runloop_status\"\n"
        )
        process = AsyncDevboxPtyProcess(session, marker)
        await session.send(wrapped)
        return process

    async def _create_tunnel(self, retry_attempts: int) -> Any:
        for attempt in range(retry_attempts):
            try:
                return await self._client.devboxes.create_pty_tunnel(self._devbox_id)
            except Exception as exc:
                if attempt == retry_attempts - 1 or not _is_retryable_status_error(exc):
                    raise
                await _sleep_for_attempt(attempt)
        raise RuntimeError("unreachable")

    async def _connect(
        self,
        tunnel_client: AsyncRunloop,
        command: str | None,
        cols: int,
        rows: int,
        cwd: str | None,
        env: dict[str, str] | None,
        retry_attempts: int,
    ) -> Any:
        for attempt in range(retry_attempts):
            try:
                return await tunnel_client.pty.connect(
                    command=command if command is not None else omit,
                    cols=cols,
                    rows=rows,
                    cwd=cwd if cwd is not None else omit,
                    env=env if env is not None else omit,
                )
            except Exception as exc:
                if attempt == retry_attempts - 1 or not _is_retryable_status_error(exc):
                    raise
                await _sleep_for_attempt(attempt)
        raise RuntimeError("unreachable")

    async def _attach(self, ws_url: str, auth_token: str, retry_attempts: int) -> Any:
        websockets = import_module("websockets")
        for attempt in range(retry_attempts):
            try:
                try:
                    return await websockets.connect(ws_url, additional_headers={"Authorization": f"Bearer {auth_token}"})
                except TypeError:
                    return await websockets.connect(ws_url, extra_headers={"Authorization": f"Bearer {auth_token}"})
            except Exception as exc:
                if attempt == retry_attempts - 1 or not _is_retryable_ws_error(exc):
                    raise
                await _sleep_for_attempt(attempt)
        raise RuntimeError("unreachable")


class AsyncDevboxPtySession:
    """Attached async PTY session."""

    def __init__(self, tunnel_client: AsyncRunloop, websocket: Any) -> None:
        self._client = tunnel_client
        self._ws = websocket
        self._raw_callbacks: list[AsyncBytesCallback] = []
        self._text_callbacks: list[AsyncTextCallback] = []
        self._queue: asyncio.Queue[bytes | object] = asyncio.Queue()
        self._closed = asyncio.Event()
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._reader = asyncio.create_task(self._read_loop())

    @property
    def raw_output(self) -> AsyncIterator[bytes]:
        return self._raw_iter()

    async def _raw_iter(self) -> AsyncIterator[bytes]:
        while True:
            item = await self._queue.get()
            if item is _CLOSE_SENTINEL:
                return
            yield item  # type: ignore[misc]

    @property
    def output(self) -> AsyncIterator[str]:
        return self._text_iter()

    async def _text_iter(self) -> AsyncIterator[str]:
        decoder = codecs.getincrementaldecoder("utf-8")()
        async for chunk in self.raw_output:
            text = decoder.decode(chunk)
            if text:
                yield text
        tail = decoder.decode(b"", final=True)
        if tail:
            yield tail

    def on_data(self, callback: AsyncBytesCallback) -> None:
        self._raw_callbacks.append(callback)

    def on_output(self, callback: AsyncTextCallback) -> None:
        self._text_callbacks.append(callback)

    async def send(self, data: str | bytes) -> None:
        payload = data.encode("utf-8") if isinstance(data, str) else data
        await self._send(payload)

    async def resize(self, cols: int, rows: int) -> None:
        if cols <= 0 or rows <= 0:
            raise ValueError("cols and rows must be positive")
        await self._client.pty.control(action="resize", cols=cols, rows=rows)

    async def signal(self, signal: str) -> None:
        if not signal:
            raise ValueError("signal must be non-empty")
        await self._client.pty.control(action="signal", signal=signal)

    async def detach(self) -> None:
        await self._close_websocket()
        await self.wait_for_close()

    async def close(self) -> None:
        await self.detach()

    async def terminate(self) -> None:
        try:
            await self._client.pty.control(action="close")
        finally:
            await self.detach()

    async def wait_for_close(self, timeout: float | None = None) -> bool:
        try:
            if timeout is None:
                await self._closed.wait()
            else:
                await asyncio.wait_for(self._closed.wait(), timeout)
            return True
        except asyncio.TimeoutError:
            return False

    async def _send(self, payload: bytes) -> None:
        send = getattr(self._ws, "send", None)
        if send is None:
            await self._ws.send_bytes(payload)
        else:
            await send(payload)

    async def _recv(self) -> bytes | str | None:
        recv = getattr(self._ws, "recv", None)
        if recv is None:
            return cast(Union[bytes, str, None], await self._ws.receive())
        return cast(Union[bytes, str, None], await recv())

    async def _close_websocket(self) -> None:
        close = getattr(self._ws, "close", None)
        if close is not None:
            result = close()
            if inspect.isawaitable(result):
                await result

    async def _read_loop(self) -> None:
        try:
            while True:
                data = await self._recv()
                if data is None or data == b"" or data == "":
                    break
                chunk = data.encode("utf-8") if isinstance(data, str) else bytes(data)
                await self._emit(chunk)
        except Exception:
            pass
        finally:
            self._closed.set()
            await self._queue.put(_CLOSE_SENTINEL)

    async def _emit(self, chunk: bytes) -> None:
        await self._queue.put(chunk)
        for raw_callback in list(self._raw_callbacks):
            await _maybe_await(raw_callback(chunk))
        text = self._decoder.decode(chunk)
        if text:
            for text_callback in list(self._text_callbacks):
                await _maybe_await(text_callback(text))


class AsyncDevboxPtyProcess:
    """PTY-backed async command process."""

    def __init__(self, session: AsyncDevboxPtySession, exit_marker: str) -> None:
        self._session = session
        self._exit_marker = exit_marker.encode("ascii")
        self._raw_callbacks: list[AsyncBytesCallback] = []
        self._text_callbacks: list[AsyncTextCallback] = []
        self._queue: asyncio.Queue[bytes | object] = asyncio.Queue()
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._pending = b""
        self._exit_code: int | None = None
        self._done = asyncio.Event()
        session.on_data(self._handle_data)

    @property
    def raw_output(self) -> AsyncIterator[bytes]:
        return self._raw_iter()

    async def _raw_iter(self) -> AsyncIterator[bytes]:
        while True:
            item = await self._queue.get()
            if item is _CLOSE_SENTINEL:
                return
            yield item  # type: ignore[misc]

    @property
    def output(self) -> AsyncIterator[str]:
        return self._text_iter()

    async def _text_iter(self) -> AsyncIterator[str]:
        decoder = codecs.getincrementaldecoder("utf-8")()
        async for chunk in self.raw_output:
            text = decoder.decode(chunk)
            if text:
                yield text
        tail = decoder.decode(b"", final=True)
        if tail:
            yield tail

    @property
    def exit_code(self) -> int | None:
        return self._exit_code

    def on_data(self, callback: AsyncBytesCallback) -> None:
        self._raw_callbacks.append(callback)

    def on_output(self, callback: AsyncTextCallback) -> None:
        self._text_callbacks.append(callback)

    async def write(self, chars: str | bytes) -> None:
        await self._session.send(chars)

    async def resize(self, cols: int, rows: int) -> None:
        await self._session.resize(cols, rows)

    async def interrupt(self) -> None:
        await self._session.signal("SIGINT")

    async def close(self) -> None:
        await self._session.terminate()

    async def wait(self, timeout: float | None = None) -> int | None:
        try:
            if timeout is None:
                await self._done.wait()
            else:
                await asyncio.wait_for(self._done.wait(), timeout)
        except asyncio.TimeoutError:
            return None
        return self._exit_code

    async def _handle_data(self, chunk: bytes) -> None:
        if self._done.is_set():
            return
        self._pending += chunk
        marker_index = self._pending.find(self._exit_marker)
        if marker_index >= 0:
            await self._publish(self._pending[:marker_index])
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
            await self._queue.put(_CLOSE_SENTINEL)
            return

        keep = len(self._exit_marker) + 32
        if len(self._pending) > keep:
            await self._publish(self._pending[:-keep])
            self._pending = self._pending[-keep:]

    async def _publish(self, chunk: bytes) -> None:
        if not chunk:
            return
        await self._queue.put(chunk)
        for raw_callback in list(self._raw_callbacks):
            await _maybe_await(raw_callback(chunk))
        text = self._decoder.decode(chunk)
        if text:
            for text_callback in list(self._text_callbacks):
                await _maybe_await(text_callback(text))
