from __future__ import annotations

import re
import asyncio
from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock, patch

import pytest

from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.sdk.pty import DevboxPtyProcess, DevboxPtySession
from runloop_api_client.sdk.devbox import Devbox
from runloop_api_client.sdk.async_pty import AsyncDevboxPtyProcess, AsyncDevboxPtySession


class FakeWebSocket:
    def __init__(self, messages: list[bytes | str | None] | None = None) -> None:
        self.messages = list(messages or [])
        self.sent: list[bytes] = []
        self.closed = False

    def recv(self) -> bytes | str | None:
        if self.messages:
            return self.messages.pop(0)
        return None

    def send_binary(self, payload: bytes) -> None:
        self.sent.append(payload)

    def close(self) -> None:
        self.closed = True


class AsyncFakeWebSocket:
    def __init__(self) -> None:
        self.messages: asyncio.Queue[bytes | str | None] = asyncio.Queue()
        self.sent: list[bytes] = []
        self.closed = False

    async def recv(self) -> bytes | str | None:
        return await self.messages.get()

    async def send(self, payload: bytes) -> None:
        self.sent.append(payload)

    async def close(self) -> None:
        self.closed = True
        await self.messages.put(None)


def test_devbox_exposes_pty() -> None:
    client = Runloop(bearer_token="token", base_url="https://api.runloop.ai")
    devbox = Devbox(client, "dbx_123")

    assert devbox.pty is not None


def test_open_creates_tunnel_client_and_attaches_websocket() -> None:
    client = Runloop(bearer_token="root", base_url="https://api.runloop.ai")
    tunnel = SimpleNamespace(tunnel_key="abc123", auth_token="tunnel-token")
    client.devboxes.create_pty_tunnel = Mock(return_value=tunnel)  # type: ignore[method-assign]
    tunnel_client = Mock()
    tunnel_client.pty.connect.return_value = SimpleNamespace(connect_url="/pty/ws/session")
    ws = FakeWebSocket([b"hello", None])
    websocket_module = SimpleNamespace(create_connection=Mock(return_value=ws))

    with patch("runloop_api_client.sdk.pty.Runloop", Mock(return_value=tunnel_client)) as runloop_cls:
        with patch("runloop_api_client.sdk.pty.import_module", Mock(return_value=websocket_module)):
            session = Devbox(client, "dbx_123").pty.open(command="/bin/bash", cols=100, rows=40)

    assert list(session.raw_output) == [b"hello"]
    client.devboxes.create_pty_tunnel.assert_called_once_with("dbx_123")
    runloop_cls.assert_called_once_with(base_url="https://13-abc123.tunnel.runloop.ai", bearer_token="tunnel-token")
    _, kwargs = tunnel_client.pty.connect.call_args
    assert kwargs["command"] == "/bin/bash"
    assert kwargs["cols"] == 100
    assert kwargs["rows"] == 40


def test_open_connect_kwargs_and_websocket_headers() -> None:
    client = Runloop(bearer_token="root", base_url="https://api.runloop.ai")
    client.devboxes.create_pty_tunnel = Mock(  # type: ignore[method-assign]
        return_value=SimpleNamespace(tunnel_key="abc123", auth_token="tunnel-token")
    )
    tunnel_client = Mock()
    tunnel_client.pty.connect.return_value = SimpleNamespace(connect_url="pty/ws/session")
    ws = FakeWebSocket([None])
    websocket_module = SimpleNamespace(create_connection=Mock(return_value=ws))

    with patch("runloop_api_client.sdk.pty.Runloop", Mock(return_value=tunnel_client)):
        with patch("runloop_api_client.sdk.pty.import_module", Mock(return_value=websocket_module)):
            Devbox(client, "dbx_123").pty.open(command="/bin/bash", cols=100, rows=40, cwd="/work", env={"A": "B"})

    _, kwargs = tunnel_client.pty.connect.call_args
    assert kwargs == {"command": "/bin/bash", "cols": 100, "rows": 40, "cwd": "/work", "env": {"A": "B"}}
    websocket_module.create_connection.assert_called_once_with(
        "wss://13-abc123.tunnel.runloop.ai/pty/ws/session",
        header=["Authorization: Bearer tunnel-token"],
    )


def test_session_close_detaches_and_terminate_sends_close_control() -> None:
    tunnel_client = Mock()
    ws = FakeWebSocket([None])
    session = DevboxPtySession(tunnel_client, ws)

    session.close()

    assert ws.closed is True
    tunnel_client.pty.control.assert_not_called()

    ws2 = FakeWebSocket([None])
    session2 = DevboxPtySession(tunnel_client, ws2)
    session2.terminate()

    tunnel_client.pty.control.assert_called_with(action="close")
    assert ws2.closed is True


def test_resize_signal_and_process_helpers() -> None:
    tunnel_client = Mock()
    ws = FakeWebSocket([])
    session = DevboxPtySession(tunnel_client, ws)
    process = DevboxPtyProcess(session, "__RUNLOOP_TEST__")

    session.resize(120, 30)
    session.signal("SIGTERM")
    process.write("hello")
    process.interrupt()
    process.close()

    assert ws.sent == [b"hello"]
    tunnel_client.pty.control.assert_any_call(action="resize", cols=120, rows=30)
    tunnel_client.pty.control.assert_any_call(action="signal", signal="SIGTERM")
    tunnel_client.pty.control.assert_any_call(action="signal", signal="SIGINT")
    tunnel_client.pty.control.assert_any_call(action="close")


def test_process_detects_exit_marker_and_filters_output() -> None:
    tunnel_client = Mock()
    ws = FakeWebSocket([])
    session = DevboxPtySession(tunnel_client, ws)
    process = DevboxPtyProcess(session, "__RUNLOOP_TEST__")

    session._emit(b"out")  # pyright: ignore[reportPrivateUsage]
    session._emit(b"put\n__RUNLOOP_TEST__:7\n")  # pyright: ignore[reportPrivateUsage]

    assert list(process.raw_output) == [b"output\n"]
    assert process.wait(timeout=0) == 7


def test_exec_wraps_command_and_sends_marker() -> None:
    client = Runloop(bearer_token="root", base_url="https://api.runloop.ai")
    client.devboxes.create_pty_tunnel = Mock(  # type: ignore[method-assign]
        return_value=SimpleNamespace(tunnel_key="abc123", auth_token="tunnel-token")
    )
    tunnel_client = Mock()
    tunnel_client.pty.connect.return_value = SimpleNamespace(connect_url="/pty/ws/session")
    ws = FakeWebSocket([None])

    with patch("runloop_api_client.sdk.pty.Runloop", Mock(return_value=tunnel_client)):
        websocket_module = SimpleNamespace(create_connection=Mock(return_value=ws))
        with patch("runloop_api_client.sdk.pty.import_module", Mock(return_value=websocket_module)):
            process = Devbox(client, "dbx_123").pty.exec("echo hi")

    sent = ws.sent[0].decode("utf-8")
    assert "echo hi\n__runloop_status=$?" in sent
    assert re.search(r"__RUNLOOP_PTY_EXIT_[a-f0-9]{32}__:%s", sent)
    assert process.exit_code is None


@pytest.mark.asyncio
async def test_async_session_and_process() -> None:
    tunnel_client = AsyncMock()
    ws = AsyncFakeWebSocket()
    session = AsyncDevboxPtySession(tunnel_client, ws)
    process = AsyncDevboxPtyProcess(session, "__RUNLOOP_TEST__")

    await ws.messages.put(b"hello")
    await ws.messages.put(b"\n__RUNLOOP_TEST__:3\n")

    assert [chunk async for chunk in process.raw_output] == [b"hello\n"]
    assert await process.wait(timeout=1) == 3

    await process.write("x")
    await process.resize(90, 20)
    await process.interrupt()
    await process.close()

    assert ws.sent == [b"x"]
    tunnel_client.pty.control.assert_any_await(action="resize", cols=90, rows=20)
    tunnel_client.pty.control.assert_any_await(action="signal", signal="SIGINT")
    tunnel_client.pty.control.assert_any_await(action="close")


@pytest.mark.asyncio
async def test_async_open_attaches_with_authorization_header() -> None:
    client = AsyncRunloop(bearer_token="root", base_url="https://api.runloop.ai")
    client.devboxes.create_pty_tunnel = AsyncMock(  # type: ignore[method-assign]
        return_value=SimpleNamespace(tunnel_key="abc123", auth_token="tunnel-token")
    )
    tunnel_client = AsyncMock()
    tunnel_client.pty.connect.return_value = SimpleNamespace(connect_url="/pty/ws/session")
    ws = AsyncFakeWebSocket()
    connect = AsyncMock(return_value=ws)

    with patch("runloop_api_client.sdk.async_pty.AsyncRunloop", Mock(return_value=tunnel_client)):
        with patch("runloop_api_client.sdk.async_pty.import_module", Mock(return_value=SimpleNamespace(connect=connect))):
            from runloop_api_client.sdk.async_devbox import AsyncDevbox

            await AsyncDevbox(client, "dbx_123").pty.open(command="/bin/sh")

    connect.assert_awaited_once_with(
        "wss://13-abc123.tunnel.runloop.ai/pty/ws/session",
        additional_headers={"Authorization": "Bearer tunnel-token"},
    )
