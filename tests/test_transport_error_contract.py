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
from runloop_api_client.lib.tunnel_readiness import wait_for_tunnel_service, async_wait_for_tunnel_service


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


def test_retry_after_http_date_is_exposed_without_negative_delay() -> None:
    request = httpx.Request("GET", "https://8080-key.tunnel.runloop.ai/health")
    response = httpx.Response(
        503,
        request=request,
        headers={"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"},
        json={"error": "tunnel_service_not_ready", "retryable": True},
    )
    error = APIStatusError("not ready", response=response, body=response.json())
    assert error.retry_after == 0


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


def test_high_level_tunnel_readiness_polls_established_authenticated_url() -> None:
    clock_value = [0.0]
    delays: list[float] = []
    requests: list[httpx.Request] = []

    def sleep(delay: float) -> None:
        delays.append(delay)
        clock_value[0] += delay

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(
                503,
                request=request,
                headers={
                    "X-Runloop-Error-Code": "tunnel_service_not_ready",
                    "X-Runloop-Request-Id": "req_probe",
                    "Retry-After": "1.5",
                },
                json={
                    "error": "tunnel_service_not_ready",
                    "message": "Tunnel routing is not ready for this backend.",
                    "retryable": True,
                    "phase": "tunnel_readiness",
                    "request_id": "req_body",
                    "details": {"port": 8080, "path": "/health"},
                },
            )
        return httpx.Response(204, request=request)

    generated = Mock()
    generated.with_options.return_value = generated
    generated.base_url = httpx.URL("https://api.runloop.ai")
    tunnel = SimpleNamespace(
        tunnel_key="tunnel-key",
        auth_mode="authenticated",
        auth_token="tunnel-secret",
    )
    generated.devboxes.enable_tunnel.return_value = tunnel
    probe_client = httpx.Client(
        headers={"Authorization": "Bearer api-secret"},
        transport=httpx.MockTransport(handler),
    )

    with probe_client:
        result = Devbox(generated, "dbx").net.wait_for_tunnel_ready(
            8080,
            "/health",
            timeout_seconds=3,
            http_client=probe_client,
            clock=lambda: clock_value[0],
            sleep=sleep,
        )

    generated.with_options.assert_called_once_with(max_retries=0)
    generated.devboxes.enable_tunnel.assert_called_once_with("dbx", timeout=3)
    assert result is tunnel
    assert delays == [1.5]
    assert [str(request.url) for request in requests] == [
        "https://8080-tunnel-key.tunnel.runloop.ai/health",
        "https://8080-tunnel-key.tunnel.runloop.ai/health",
    ]
    assert all(request.headers["X-Runloop-Tunnel-Authorization"] == "Bearer tunnel-secret" for request in requests)
    assert all("authorization" not in request.headers for request in requests)


async def test_async_high_level_tunnel_readiness_stops_on_terminal_error() -> None:
    generated = Mock()
    generated.with_options.return_value = generated
    generated.base_url = httpx.URL("https://api.runloop.ai")
    generated.devboxes = SimpleNamespace(
        enable_tunnel=AsyncMock(return_value=SimpleNamespace(tunnel_key="key", auth_mode="open", auth_token=None))
    )
    sleep = AsyncMock()

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            503,
            request=request,
            headers={"X-Runloop-Error-Code": "tunnel_unavailable", "Retry-After": "0"},
            json={
                "error": "tunnel_unavailable",
                "message": "Tunnel is unavailable.",
                "retryable": False,
                "phase": "tunnel_readiness",
            },
        )

    probe_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    async with probe_client:
        with pytest.raises(APIStatusError) as caught:
            await AsyncDevbox(generated, "dbx").net.wait_for_tunnel_ready(
                3000,
                http_client=probe_client,
                sleep=sleep,
            )

    assert caught.value.code == "tunnel_unavailable"
    assert caught.value.attempts == 1
    assert caught.value.retryable is False
    sleep.assert_not_awaited()


def test_tunnel_readiness_timeout_identifies_port_and_path() -> None:
    clock_value = [0.0]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            503,
            request=request,
            headers={"X-Runloop-Error-Code": "tunnel_service_not_ready", "Retry-After": "2"},
            json={"error": "tunnel_service_not_ready", "retryable": True},
        )

    def sleep(delay: float) -> None:
        clock_value[0] += delay

    generated = Mock()
    generated.with_options.return_value = generated
    generated.base_url = httpx.URL("https://api.runloop.ai")
    generated.devboxes.enable_tunnel.return_value = SimpleNamespace(tunnel_key="key", auth_mode="open", auth_token=None)
    probe_client = httpx.Client(transport=httpx.MockTransport(handler))

    with probe_client, pytest.raises(APIStatusError) as caught:
        Devbox(generated, "dbx").net.wait_for_tunnel_ready(
            9090,
            "/ready",
            timeout_seconds=2,
            http_client=probe_client,
            clock=lambda: clock_value[0],
            sleep=sleep,
        )

    assert caught.value.code == "tunnel_service_not_ready"
    assert caught.value.attempts == 1
    assert "port 9090" in str(caught.value)
    assert "'/ready'" in str(caught.value)


def test_tunnel_readiness_does_not_follow_authenticated_redirects() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(302, request=request, headers={"Location": "https://attacker.test/token"})

    generated = Mock()
    generated.with_options.return_value = generated
    generated.base_url = httpx.URL("https://api.runloop.ai")
    generated.devboxes.enable_tunnel.return_value = SimpleNamespace(
        tunnel_key="key", auth_mode="authenticated", auth_token="tunnel-secret"
    )
    probe_client = httpx.Client(
        headers={"Authorization": "Bearer api-secret"},
        transport=httpx.MockTransport(handler),
    )

    with probe_client, pytest.raises(APIStatusError) as caught:
        Devbox(generated, "dbx").net.wait_for_tunnel_ready(8080, http_client=probe_client)

    assert caught.value.code == "http_302"
    assert len(requests) == 1
    assert requests[0].url.host == "8080-key.tunnel.runloop.ai"
    assert "authorization" not in requests[0].headers
    assert requests[0].headers["X-Runloop-Tunnel-Authorization"] == "Bearer tunnel-secret"


def test_tunnel_readiness_timeout_preserves_connect_cause() -> None:
    clock_value = [0.0]

    def request(_remaining: float) -> httpx.Response:
        http_request = httpx.Request("GET", "https://8080-key.tunnel.runloop.ai/health")
        raise httpx.ConnectTimeout("connect timed out", request=http_request)

    def sleep(delay: float) -> None:
        clock_value[0] += delay

    with pytest.raises(APIError) as caught:
        wait_for_tunnel_service(
            request,
            port=8080,
            path="/health",
            timeout_seconds=1,
            clock=lambda: clock_value[0],
            sleep=sleep,
        )

    assert caught.value.code == "connection_timeout"
    assert caught.value.attempts == 2
    assert isinstance(caught.value.cause, httpx.ConnectTimeout)
    assert caught.value.__cause__ is caught.value.cause


def test_retry_headers_do_not_make_terminal_readiness_error_transient() -> None:
    attempts = 0
    sleep = Mock()

    def request(_remaining: float) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        http_request = httpx.Request("GET", "https://8080-key.tunnel.runloop.ai/health")
        return httpx.Response(
            503,
            request=http_request,
            headers={
                "X-Runloop-Error-Code": "tunnel_backend_connect_timeout",
                "X-Should-Retry": "true",
                "Retry-After": "0",
            },
            json={"error": "tunnel_backend_connect_timeout", "retryable": True},
        )

    with pytest.raises(APIStatusError) as caught:
        wait_for_tunnel_service(request, port=8080, sleep=sleep)

    assert caught.value.code == "tunnel_backend_connect_timeout"
    assert caught.value.attempts == 1
    assert attempts == 1
    sleep.assert_not_called()


async def test_async_retry_headers_do_not_make_terminal_readiness_error_transient() -> None:
    attempts = 0
    sleep = AsyncMock()

    async def request(_remaining: float) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        http_request = httpx.Request("GET", "https://8080-key.tunnel.runloop.ai/health")
        return httpx.Response(
            503,
            request=http_request,
            headers={
                "X-Runloop-Error-Code": "tunnel_backend_connect_timeout",
                "X-Should-Retry": "true",
                "Retry-After": "0",
            },
            json={"error": "tunnel_backend_connect_timeout", "retryable": True},
        )

    with pytest.raises(APIStatusError) as caught:
        await async_wait_for_tunnel_service(request, port=8080, sleep=sleep)

    assert caught.value.code == "tunnel_backend_connect_timeout"
    assert caught.value.attempts == 1
    assert attempts == 1
    sleep.assert_not_awaited()


def test_generic_exception_is_not_retried_after_ambiguous_receipt() -> None:
    attempts = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        raise RuntimeError("response hook failed")

    client = Runloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=2,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    with client, pytest.raises(APIError) as caught:
        client.devboxes.enable_tunnel("dbx")

    assert attempts == 1
    assert caught.value.attempts == 1


def ambiguous_transfer_response(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        503,
        request=request,
        json={
            "error": "tunnel_backend_connection_reset",
            "message": "Tunnel response ended after partial delivery.",
            "retryable": True,
            "phase": "response_read",
        },
    )


def test_streamed_structured_ambiguous_error_is_not_retried() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return ambiguous_transfer_response(request)

    client = Runloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=1,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    with client, pytest.raises(APIStatusError) as caught:
        with client.devboxes.with_streaming_response.enable_tunnel("dbx"):
            pass

    assert attempts == 1
    assert caught.value.code == "tunnel_backend_connection_reset"


async def test_async_streamed_structured_ambiguous_error_is_not_retried() -> None:
    attempts = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return ambiguous_transfer_response(request)

    client = AsyncRunloop(
        bearer_token="test",
        base_url="https://example.test",
        max_retries=1,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    async with client:
        with pytest.raises(APIStatusError) as caught:
            async with client.devboxes.with_streaming_response.enable_tunnel("dbx"):
                pass

    assert attempts == 1
    assert caught.value.code == "tunnel_backend_connection_reset"
