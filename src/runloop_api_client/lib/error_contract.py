"""Stable normalization for Runloop API and HTTPX transport failures.

This module is handwritten and intentionally lives under ``lib`` so generated
client updates only need a small integration point.
"""

from __future__ import annotations

import time
import email.utils
from typing import Mapping, cast
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class ErrorDetails:
    code: str
    phase: str
    retryable: bool
    request_id: str | None = None
    retry_after: float | None = None


def _number(value: object) -> float | None:
    try:
        parsed = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def parse_retry_after(headers: httpx.Headers, body: object = None) -> float | None:
    """Parse Retry-After while accepting the SDK's millisecond extension."""
    milliseconds = _number(headers.get("retry-after-ms"))
    if milliseconds is not None:
        return milliseconds / 1000
    seconds = _number(headers.get("retry-after"))
    if seconds is not None:
        return seconds
    retry_date = email.utils.parsedate_tz(headers.get("retry-after"))
    if retry_date is not None:
        return max(float(email.utils.mktime_tz(retry_date) - time.time()), 0)
    if isinstance(body, Mapping):
        payload = cast(Mapping[str, object], body)
        details = payload.get("details")
        if isinstance(details, Mapping):
            return _number(cast(Mapping[str, object], details).get("retry_after"))
    return None


def status_error_details(response: httpx.Response, body: object) -> ErrorDetails:
    payload: Mapping[str, object] = cast(Mapping[str, object], body) if isinstance(body, Mapping) else {}
    header_code = response.headers.get("x-runloop-error-code")
    body_code = payload.get("error")
    code = header_code or (body_code if isinstance(body_code, str) else None) or f"http_{response.status_code}"
    body_phase = payload.get("phase")
    phase = body_phase if isinstance(body_phase, str) else "api"
    retryable_value = payload.get("retryable")
    retryable = retryable_value if isinstance(retryable_value, bool) else response.status_code in {408, 409, 429}
    if response.status_code >= 500 and not isinstance(retryable_value, bool):
        retryable = True
    request_id: str | None = response.headers.get("x-runloop-request-id")
    body_request_id = payload.get("request_id")
    if request_id is None and isinstance(body_request_id, str):
        request_id = body_request_id
    return ErrorDetails(
        code=code,
        phase=phase,
        retryable=retryable,
        request_id=request_id,
        retry_after=parse_retry_after(response.headers, cast(object, body)),
    )


def transport_error_details(error: BaseException) -> ErrorDetails:
    if isinstance(error, httpx.ConnectTimeout):
        return ErrorDetails("connection_timeout", "connect", True)
    if isinstance(error, httpx.WriteTimeout):
        return ErrorDetails("request_write_timeout", "request_write", False)
    if isinstance(error, httpx.WriteError):
        return ErrorDetails("request_write_failed", "request_write", False)
    if isinstance(error, httpx.ReadTimeout):
        return ErrorDetails("response_read_timeout", "response_read", False)
    if isinstance(error, httpx.RemoteProtocolError):
        if "idle_timeout" in str(error).lower():
            return ErrorDetails("http2_idle_timeout", "response_read", False)
        return ErrorDetails("http2_protocol_error", "transport", False)
    if isinstance(error, httpx.TimeoutException):
        return ErrorDetails("connection_timeout", "connect", True)
    return ErrorDetails("connection_failed", "connect", isinstance(error, httpx.ConnectError))


def is_safe_transport_retry(error: BaseException) -> bool:
    """Only retry failures that prove the request body was not partially sent."""
    # Preserve the generated client's handling of non-HTTPX exceptions (for
    # example a pre-send auth hook failure). HTTPX errors carry enough phase
    # information for the stricter partial-write audit below.
    if not isinstance(error, httpx.HTTPError):
        return True
    return isinstance(error, (httpx.ConnectTimeout, httpx.ConnectError))
