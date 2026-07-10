"""Helpers for polling wait_for_status long-poll endpoints.

Each function wraps a server-side long-poll POST with a client-side retry
loop.  On each iteration the remaining timeout is forwarded to the server
so the server can long-poll for up to that duration.  408 responses and
client-side timeouts are converted to a caller-supplied placeholder so the
loop can continue.  No client-side sleep between iterations — the
server-side long-poll *is* the wait.
"""

from __future__ import annotations

import time
from typing import List, Type, TypeVar, Callable, Optional, Awaitable

import httpx

from .polling import PollingConfig, PollingTimeout
from .._constants import LONG_POLL_CLIENT_BUFFER_SECONDS, STATUS_LONG_POLL_SERVER_MAX_SECONDS
from .._exceptions import APIStatusError, APIConnectionError

T = TypeVar("T")


def wait_for_status(
    post_fn: Callable[..., T],
    path: str,
    statuses: List[str],
    cast_to: Type[T],
    placeholder: Callable[[], T],
    is_terminal: Callable[[T], bool],
    polling_config: Optional[PollingConfig] = None,
    server_max_timeout_seconds: float = STATUS_LONG_POLL_SERVER_MAX_SECONDS,
) -> T:
    """Sync long-poll for a status change, retrying until *is_terminal* or timeout."""
    config = polling_config or PollingConfig()
    timeout = config.interval_seconds * config.max_attempts
    if config.timeout_seconds is not None and config.timeout_seconds > 0:
        timeout = min(config.timeout_seconds, timeout)

    start_time = time.time()
    last_result: T | None = None

    while True:
        remaining = timeout - (time.time() - start_time)
        if remaining <= 0:
            raise PollingTimeout(f"Exceeded timeout of {timeout} seconds", last_result)

        # Cap the server hold at what the server honors, and give the client read
        # timeout a buffer beyond it so the server returns 408 first.
        server_timeout = min(remaining, server_max_timeout_seconds)
        try:
            last_result = post_fn(
                path,
                body={"statuses": statuses, "timeout_seconds": server_timeout},
                cast_to=cast_to,
                options={
                    "max_retries": 0,
                    "timeout": httpx.Timeout(server_timeout + LONG_POLL_CLIENT_BUFFER_SECONDS, connect=5.0),
                },
            )
        except (APIConnectionError, APIStatusError) as error:
            if isinstance(error, APIConnectionError) or error.response.status_code == 408:
                last_result = placeholder()
            else:
                raise

        if is_terminal(last_result):
            return last_result


async def async_wait_for_status(
    post_fn: Callable[..., Awaitable[T]],
    path: str,
    statuses: List[str],
    cast_to: Type[T],
    placeholder: Callable[[], T],
    is_terminal: Callable[[T], bool],
    polling_config: Optional[PollingConfig] = None,
    server_max_timeout_seconds: float = STATUS_LONG_POLL_SERVER_MAX_SECONDS,
) -> T:
    """Async long-poll for a status change, retrying until *is_terminal* or timeout."""
    config = polling_config or PollingConfig()
    timeout = config.interval_seconds * config.max_attempts
    if config.timeout_seconds is not None and config.timeout_seconds > 0:
        timeout = min(config.timeout_seconds, timeout)

    start_time = time.time()
    last_result: T | None = None

    while True:
        remaining = timeout - (time.time() - start_time)
        if remaining <= 0:
            raise PollingTimeout(f"Exceeded timeout of {timeout} seconds", last_result)

        # Cap the server hold at what the server honors, and give the client read
        # timeout a buffer beyond it so the server returns 408 first.
        server_timeout = min(remaining, server_max_timeout_seconds)
        try:
            last_result = await post_fn(
                path,
                body={"statuses": statuses, "timeout_seconds": server_timeout},
                cast_to=cast_to,
                options={
                    "max_retries": 0,
                    "timeout": httpx.Timeout(server_timeout + LONG_POLL_CLIENT_BUFFER_SECONDS, connect=5.0),
                },
            )
        except (APIConnectionError, APIStatusError) as error:
            if isinstance(error, APIConnectionError) or error.response.status_code == 408:
                last_result = placeholder()
            else:
                raise

        if is_terminal(last_result):
            return last_result
