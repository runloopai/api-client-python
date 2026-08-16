"""Hermetic reproduction of the 2026-08-16 transport incident families.

Run with: uv run pytest tests/test_transport_error_contract.py -n 0
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock
from collections.abc import Callable

import httpx
import pytest

from runloop_api_client import Runloop, APIError, AsyncRunloop, APIStatusError
from runloop_api_client.sdk.devbox import Devbox
from runloop_api_client.sdk.async_devbox import AsyncDevbox


def customer_shape(error: APIError) -> dict[str, object]:
    """The supported diagnostic surface; callers need not inspect __cause__."""
    return {
        "type": type(error).__name__,
        "code": error.code,
        "phase": error.phase,
        "retryable": error.retryable,
        "request_id": error.request_id,
        "retry_after": error.retry_after,
        "attempts": error.attempts,
        "cause": type(error.cause).__name__ if error.cause else None,
    }


INCIDENTS: list[tuple[str, Callable[[httpx.Request], httpx.HTTPError], dict[str, object]]] = [
    (
        "connect",
        lambda request: httpx.ConnectTimeout("connect timed out", request=request),
        {
            "type": "APITimeoutError",
            "code": "connection_timeout",
            "phase": "connect",
            "retryable": True,
            "request_id": None,
            "retry_after": None,
            "attempts": 1,
            "cause": "ConnectTimeout",
        },
    ),
    (
        "write",
        lambda request: httpx.WriteError("write failed", request=request),
        {
            "type": "APIConnectionError",
            "code": "request_write_failed",
            "phase": "request_write",
            "retryable": False,
            "request_id": None,
            "retry_after": None,
            "attempts": 1,
            "cause": "WriteError",
        },
    ),
    (
        "idle",
        lambda request: httpx.RemoteProtocolError(
            "<ConnectionTerminated error_code:0, additional_data:idle_timeout>", request=request
        ),
        {
            "type": "APIConnectionError",
            "code": "http2_idle_timeout",
            "phase": "response_read",
            "retryable": False,
            "request_id": None,
            "retry_after": None,
            "attempts": 1,
            "cause": "RemoteProtocolError",
        },
    ),
]


@pytest.mark.parametrize(("_name", "failure", "expected"), INCIDENTS)
@pytest.mark.parametrize("operation", ["upload_file", "enable_tunnel"])
def test_sync_incident_transport_shapes(
    _name: str,
    failure: Callable[[httpx.Request], httpx.HTTPError],
    expected: dict[str, object],
    operation: str,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise failure(request)

    with Runloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        with pytest.raises(APIError) as caught:
            if operation == "upload_file":
                client.devboxes.upload_file("dbx", path="data.bin", file=b"data")
            else:
                client.devboxes.enable_tunnel("dbx")

    assert customer_shape(caught.value) == expected
    assert caught.value.__cause__ is caught.value.cause


@pytest.mark.parametrize(("_name", "failure", "expected"), INCIDENTS)
@pytest.mark.parametrize("operation", ["upload_file", "enable_tunnel"])
async def test_async_incident_transport_shapes(
    _name: str,
    failure: Callable[[httpx.Request], httpx.HTTPError],
    expected: dict[str, object],
    operation: str,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise failure(request)

    async with AsyncRunloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=0,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as client:
        with pytest.raises(APIError) as caught:
            if operation == "upload_file":
                await client.devboxes.upload_file("dbx", path="data.bin", file=b"data")
            else:
                await client.devboxes.enable_tunnel("dbx")

    assert customer_shape(caught.value) == expected
    assert caught.value.__cause__ is caught.value.cause


def structured_not_ready(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        503,
        request=request,
        headers={
            "X-Runloop-Error-Code": "tunnel_service_not_ready",
            "X-Runloop-Request-Id": "req_header",
            "Retry-After": "1.5",
            "X-Should-Retry": "false",
        },
        json={
            "error": "legacy_tunnel_error",
            "message": "Tunnel service is still becoming ready.",
            "retryable": True,
            "phase": "tunnel_readiness",
            "request_id": "req_body",
            "details": {"port": 8080, "path": "/health"},
        },
    )


def test_sync_structured_tunnel_not_ready_shape() -> None:
    client = Runloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(structured_not_ready)),
    )
    with client, pytest.raises(APIError) as caught:
        client.devboxes.enable_tunnel("dbx")
    assert customer_shape(caught.value) == {
        "type": "InternalServerError",
        "code": "tunnel_service_not_ready",
        "phase": "tunnel_readiness",
        "retryable": True,
        "request_id": "req_header",
        "retry_after": 1.5,
        "attempts": 1,
        "cause": None,
    }


async def test_async_structured_tunnel_not_ready_shape() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return structured_not_ready(request)

    client = AsyncRunloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=0,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    async with client:
        with pytest.raises(APIError) as caught:
            await client.devboxes.enable_tunnel("dbx")
    assert caught.value.code == "tunnel_service_not_ready"
    assert caught.value.request_id == "req_header"
    assert caught.value.retry_after == 1.5


def readiness_error(*, code: str = "tunnel_service_not_ready", retry_after: str = "2") -> APIStatusError:
    request = httpx.Request("POST", "https://example.test/v1/devboxes/dbx/enable_tunnel")
    response = httpx.Response(
        503,
        request=request,
        headers={"X-Runloop-Error-Code": code, "Retry-After": retry_after},
    )
    return APIStatusError("not ready", response=response, body={"error": code, "retryable": True})


def test_high_level_tunnel_readiness_honors_retry_after_and_deadline() -> None:
    clock_value = [0.0]
    delays: list[float] = []

    def sleep(delay: float) -> None:
        delays.append(delay)
        clock_value[0] += delay

    generated = Mock()
    generated.with_options.return_value = generated
    generated.devboxes.enable_tunnel.side_effect = [readiness_error(), readiness_error()]

    with pytest.raises(APIStatusError) as caught:
        Devbox(generated, "dbx").net.wait_for_tunnel_ready(
            8080,
            "/health",
            timeout_seconds=2,
            clock=lambda: clock_value[0],
            sleep=sleep,
        )

    generated.with_options.assert_called_once_with(max_retries=0)
    assert delays == [2.0]
    assert caught.value.code == "tunnel_service_not_ready"
    assert caught.value.attempts == 2
    assert "port 8080" in str(caught.value)
    assert "'/health'" in str(caught.value)


async def test_async_high_level_tunnel_readiness_stops_on_terminal_error() -> None:
    generated = Mock()
    generated.with_options.return_value = generated
    generated.devboxes = SimpleNamespace(
        enable_tunnel=AsyncMock(side_effect=readiness_error(code="tunnel_unavailable"))
    )
    sleep = AsyncMock()

    with pytest.raises(APIStatusError) as caught:
        await AsyncDevbox(generated, "dbx").net.wait_for_tunnel_ready(3000, sleep=sleep)

    assert caught.value.code == "tunnel_unavailable"
    assert caught.value.attempts == 1
    sleep.assert_not_awaited()
