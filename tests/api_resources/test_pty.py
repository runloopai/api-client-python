from __future__ import annotations

import json

import httpx

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import PtyConnectView


def test_method_connect() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"connect_url": "/pty/ws/session", "session_id": "pty_123"})

    client = Runloop(
        bearer_token="token",
        base_url="https://13-key.tunnel.runloop.ai",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    response = client.pty.connect(command="/bin/sh", cols=100, rows=40)

    assert_matches_type(PtyConnectView, response, path=["response"])
    assert response.connect_url == "/pty/ws/session"
    assert requests[0].url == "https://13-key.tunnel.runloop.ai/pty/connect"
    assert json.loads(requests[0].content) == {"command": "/bin/sh", "cols": 100, "rows": 40}


def test_method_control() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    client = Runloop(
        bearer_token="token",
        base_url="https://13-key.tunnel.runloop.ai",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    response = client.pty.control(action="resize", cols=120, rows=30)

    assert response == {}
    assert requests[0].url == "https://13-key.tunnel.runloop.ai/pty/control"
    assert json.loads(requests[0].content) == {"action": "resize", "cols": 120, "rows": 30}


async def test_async_method_connect() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"connect_url": "/pty/ws/session"})

    client = AsyncRunloop(
        bearer_token="token",
        base_url="https://13-key.tunnel.runloop.ai",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )

    response = await client.pty.connect(command="/bin/sh")

    assert_matches_type(PtyConnectView, response, path=["response"])
    assert requests[0].url == "https://13-key.tunnel.runloop.ai/pty/connect"
