"""Bounded polling of an established tunnel's service endpoint."""

from __future__ import annotations

import json
import time
from typing import Mapping, Callable, Awaitable, cast

import httpx

from .._exceptions import APIError, APIStatusError, APITimeoutError, APIConnectionError
from .error_contract import is_safe_transport_retry


def tunnel_url(*, api_host: str, tunnel_key: str, port: int, path: str = "/") -> str:
    """Construct the established tunnel URL using the SDK's domain convention."""
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    if not path.startswith("/"):
        raise ValueError("path must start with '/'")
    if not tunnel_key or not all(
        character.isascii() and (character.isalnum() or character in "-_") for character in tunnel_key
    ):
        raise ValueError("tunnel_key contains characters that are unsafe in a tunnel hostname")
    base_domain = api_host[4:] if api_host.startswith("api.") else api_host
    return f"https://{port}-{tunnel_key}.tunnel.{base_domain}{path}"


def tunnel_auth_headers(*, auth_mode: str, auth_token: str | None, request: httpx.Request) -> Mapping[str, str]:
    """Return tunnel authentication without leaking the Runloop API bearer token."""
    if auth_mode != "authenticated":
        return {}
    if auth_token:
        return {"X-Runloop-Tunnel-Authorization": f"Bearer {auth_token}"}
    error = APIConnectionError(
        message="Authenticated tunnel is missing its tunnel authorization token.",
        request=request,
    )
    error.code = "tunnel_authentication_required"
    error.phase = "tunnel_readiness"
    error.retryable = False
    raise error


def _status_error(response: httpx.Response, attempts: int) -> APIStatusError:
    body: object = response.text
    try:
        body = cast(object, json.loads(response.text))
    except (TypeError, ValueError):
        pass
    payload = cast(Mapping[str, object], body) if isinstance(body, dict) else None
    body_message = payload.get("message") if payload is not None else None
    message = (
        body_message
        if isinstance(body_message, str)
        else f"Tunnel readiness check failed with HTTP status {response.status_code}."
    )
    error = APIStatusError(message, response=response, body=cast(object, body), attempts=attempts)
    if error.phase == "api":
        error.phase = "tunnel_readiness"
    return error


def _connection_error(error: httpx.HTTPError, request: httpx.Request, attempts: int) -> APIConnectionError:
    if isinstance(error, httpx.TimeoutException):
        return APITimeoutError(request=request, cause=error, attempts=attempts)
    return APIConnectionError(request=request, cause=error, attempts=attempts)


def _raise_timeout(error: APIError, *, port: int, path: str, timeout_seconds: float, attempts: int) -> None:
    message = f"Tunnel service was not ready for port {port} path {path!r} within {timeout_seconds:g} seconds."
    error.message = message
    error.args = (message,)
    error.attempts = attempts
    if error.cause is not None:
        raise error from error.cause
    raise error


def _retry_delay(error: APIError) -> float:
    return error.retry_after if error.retry_after is not None else 0.5


def _is_transient_status(error: APIStatusError) -> bool:
    if error.code == "tunnel_unavailable":
        return False
    should_retry = error.response.headers.get("x-should-retry")
    if should_retry == "false":
        return False
    if should_retry == "true":
        return True
    return error.code == "tunnel_service_not_ready"


def send_tunnel_probe(
    client: httpx.Client,
    url: str,
    headers: Mapping[str, str],
    timeout: float,
) -> httpx.Response:
    """Send one probe without client auth or cross-origin redirect forwarding."""
    request = client.build_request("GET", url, headers=headers, timeout=timeout)
    request.headers.pop("authorization", None)
    return client.send(request, auth=None, follow_redirects=False)


async def async_send_tunnel_probe(
    client: httpx.AsyncClient,
    url: str,
    headers: Mapping[str, str],
    timeout: float,
) -> httpx.Response:
    """Async counterpart to :func:`send_tunnel_probe`."""
    request = client.build_request("GET", url, headers=headers, timeout=timeout)
    request.headers.pop("authorization", None)
    return await client.send(request, auth=None, follow_redirects=False)


def wait_for_tunnel_service(
    request: Callable[[float], httpx.Response],
    *,
    port: int,
    path: str = "/",
    timeout_seconds: float = 30.0,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Poll an established tunnel URL until it returns a successful response."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    deadline = clock() + timeout_seconds
    attempts = 0
    failure: APIError | None = None
    while True:
        remaining = deadline - clock()
        if remaining <= 0:
            if failure is None:
                raise ValueError("tunnel readiness deadline expired before the first request")
            _raise_timeout(failure, port=port, path=path, timeout_seconds=timeout_seconds, attempts=attempts)
        attempts += 1
        try:
            response = request(remaining)
            if response.is_success:
                return
            failure = _status_error(response, attempts)
            if not _is_transient_status(failure):
                raise failure
        except httpx.HTTPError as cause:
            request_object = cause.request
            failure = _connection_error(cause, request_object, attempts)
            if not is_safe_transport_retry(cause):
                raise failure from cause

        remaining = deadline - clock()
        if remaining <= 0 or attempts >= 1000:
            _raise_timeout(failure, port=port, path=path, timeout_seconds=timeout_seconds, attempts=attempts)
        sleep(min(max(_retry_delay(failure), 0), remaining))


async def async_wait_for_tunnel_service(
    request: Callable[[float], Awaitable[httpx.Response]],
    *,
    port: int,
    path: str = "/",
    timeout_seconds: float = 30.0,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], Awaitable[None]],
) -> None:
    """Async counterpart to :func:`wait_for_tunnel_service`."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    deadline = clock() + timeout_seconds
    attempts = 0
    failure: APIError | None = None
    while True:
        remaining = deadline - clock()
        if remaining <= 0:
            if failure is None:
                raise ValueError("tunnel readiness deadline expired before the first request")
            _raise_timeout(failure, port=port, path=path, timeout_seconds=timeout_seconds, attempts=attempts)
        attempts += 1
        try:
            response = await request(remaining)
            if response.is_success:
                return
            failure = _status_error(response, attempts)
            if not _is_transient_status(failure):
                raise failure
        except httpx.HTTPError as cause:
            request_object = cause.request
            failure = _connection_error(cause, request_object, attempts)
            if not is_safe_transport_retry(cause):
                raise failure from cause

        remaining = deadline - clock()
        if remaining <= 0 or attempts >= 1000:
            _raise_timeout(failure, port=port, path=path, timeout_seconds=timeout_seconds, attempts=attempts)
        await sleep(min(max(_retry_delay(failure), 0), remaining))
