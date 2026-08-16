"""Bounded retry helpers for tunnel service readiness."""

from __future__ import annotations

import time
import inspect
from typing import TypeVar, Callable, Awaitable

from .._exceptions import APIStatusError

T = TypeVar("T")


def _timeout(error: APIStatusError, *, port: int, path: str, timeout_seconds: float, attempts: int) -> None:
    message = f"Tunnel service was not ready for port {port} path {path!r} within {timeout_seconds:g} seconds."
    error.message = message
    error.args = (message,)
    error.attempts = attempts
    raise error


def wait_for_tunnel_service(
    operation: Callable[[], T],
    *,
    port: int,
    path: str = "/",
    timeout_seconds: float = 30.0,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Retry only ``tunnel_service_not_ready`` until a bounded deadline."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    deadline = clock() + timeout_seconds
    attempts = 0
    while True:
        attempts += 1
        try:
            return operation()
        except APIStatusError as error:
            error.attempts = attempts
            if error.code != "tunnel_service_not_ready":
                raise
            remaining = deadline - clock()
            if remaining <= 0 or attempts >= 1000:
                _timeout(error, port=port, path=path, timeout_seconds=timeout_seconds, attempts=attempts)
            delay = error.retry_after if error.retry_after is not None else 0.5
            sleep(min(max(delay, 0), remaining))


async def async_wait_for_tunnel_service(
    operation: Callable[[], Awaitable[T]],
    *,
    port: int,
    path: str = "/",
    timeout_seconds: float = 30.0,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], Awaitable[None]],
) -> T:
    """Async counterpart to :func:`wait_for_tunnel_service`."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    deadline = clock() + timeout_seconds
    attempts = 0
    while True:
        attempts += 1
        try:
            return await operation()
        except APIStatusError as error:
            error.attempts = attempts
            if error.code != "tunnel_service_not_ready":
                raise
            remaining = deadline - clock()
            if remaining <= 0 or attempts >= 1000:
                _timeout(error, port=port, path=path, timeout_seconds=timeout_seconds, attempts=attempts)
            delay = error.retry_after if error.retry_after is not None else 0.5
            result = sleep(min(max(delay, 0), remaining))
            if inspect.isawaitable(result):
                await result
