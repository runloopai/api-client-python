"""Make httpcore open additional HTTP/2 connections when stream slots run low.

httpcore multiplexes HTTP/2 on a single connection and gates new streams with a
semaphore (default MAX_CONCURRENT_STREAMS=100).  Its connection pool's
``is_available()`` ignores that limit, so once stream slots are exhausted,
further requests *block* on the semaphore instead of the pool opening another
connection — even when ``max_connections`` still has headroom.

Additionally, the pool may assign a *burst* of requests to a connection that
only has a few free slots left (``is_available()`` is checked once per request
but slots are not reserved).  Winners then share an overloaded connection while
the rest raise ``ConnectionNotAvailable`` and retry.

This module patches sync + async HTTP/2 connections so that:

1. ``is_available()`` is False when free stream slots are below a headroom
   threshold, so the pool prefers opening/reusing another connection.
2. Stream-slot acquire is non-blocking; if a race still over-assigns, we raise
   ``ConnectionNotAvailable`` and the pool retries on another connection.

Idempotent: safe to call ``install()`` more than once.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger("runloop_api_client._http2_pool_fix")

# If a connection has fewer free stream slots than this, treat it as unavailable
# so the pool opens another connection instead of stampeding the remainder.
# Must be >1: the pool assigns many queued requests to one "available" conn
# without reserving slots, so small remaining capacity still over-assigns.
_MIN_FREE_STREAM_SLOTS = 16

_installed = False


def _free_stream_slots(connection: Any) -> int | None:
    """Return free H2 stream slots, or None if unknown."""
    max_streams = getattr(connection, "_max_streams", None)
    events = getattr(connection, "_events", None)
    if not isinstance(max_streams, int) or max_streams <= 0 or events is None:
        return None
    return max_streams - len(events)


def _stream_slots_saturated(connection: Any) -> bool:
    """True when the connection should not accept more streams."""
    free = _free_stream_slots(connection)
    if free is None:
        return False
    return free < _MIN_FREE_STREAM_SLOTS


def _patch_is_available(cls: type) -> None:
    if getattr(cls.is_available, "_runloop_stream_overflow_patched", False):
        return

    original: Callable[[Any], bool] = cls.is_available

    def is_available(self: Any) -> bool:
        if not original(self):
            return False
        return not _stream_slots_saturated(self)

    is_available._runloop_stream_overflow_patched = True  # type: ignore[attr-defined]
    cls.is_available = is_available  # type: ignore[method-assign]


def _make_async_nonblocking_acquire(sem: Any, connection_not_available: type) -> Callable[[], Any]:
    original_acquire = sem.acquire

    async def acquire() -> None:
        if not getattr(sem, "_backend", ""):
            sem.setup()

        if sem._backend == "asyncio":
            inner = sem._anyio_semaphore
            try:
                inner.acquire_nowait()
                return
            except Exception:
                raise connection_not_available(
                    "HTTP/2 connection has no free stream slots"
                ) from None

        if sem._backend == "trio":
            inner = sem._trio_semaphore
            acquire_nowait = getattr(inner, "acquire_nowait", None)
            if acquire_nowait is not None:
                try:
                    acquire_nowait()
                    return
                except Exception:
                    raise connection_not_available(
                        "HTTP/2 connection has no free stream slots"
                    ) from None

        await original_acquire()

    return acquire


def _make_sync_nonblocking_acquire(sem: Any, connection_not_available: type) -> Callable[[], None]:
    inner = getattr(sem, "_semaphore", sem)

    def acquire() -> None:
        ok = inner.acquire(False)
        if not ok:
            raise connection_not_available("HTTP/2 connection has no free stream slots")

    return acquire


def _patch_async_connection(cls: type) -> None:
    from httpcore import ConnectionNotAvailable

    if getattr(cls.handle_async_request, "_runloop_stream_overflow_patched", False):
        return

    original = cls.handle_async_request

    async def handle_async_request(self: Any, request: Any) -> Any:
        sem = getattr(self, "_max_streams_semaphore", None)
        if sem is None:
            return await original(self, request)

        real_acquire = sem.acquire
        sem.acquire = _make_async_nonblocking_acquire(sem, ConnectionNotAvailable)
        try:
            return await original(self, request)
        finally:
            sem.acquire = real_acquire

    handle_async_request._runloop_stream_overflow_patched = True  # type: ignore[attr-defined]
    cls.handle_async_request = handle_async_request  # type: ignore[method-assign]


def _patch_sync_connection(cls: type) -> None:
    from httpcore import ConnectionNotAvailable

    if getattr(cls.handle_request, "_runloop_stream_overflow_patched", False):
        return

    original = cls.handle_request

    def handle_request(self: Any, request: Any) -> Any:
        sem = getattr(self, "_max_streams_semaphore", None)
        if sem is None:
            return original(self, request)

        real_acquire = sem.acquire
        sem.acquire = _make_sync_nonblocking_acquire(sem, ConnectionNotAvailable)
        try:
            return original(self, request)
        finally:
            sem.acquire = real_acquire

    handle_request._runloop_stream_overflow_patched = True  # type: ignore[attr-defined]
    cls.handle_request = handle_request  # type: ignore[method-assign]


def install() -> bool:
    """Patch httpcore HTTP/2 connections. Returns True if a patch was applied."""
    global _installed
    if _installed:
        return False

    try:
        from httpcore._async.http2 import AsyncHTTP2Connection
        from httpcore._sync.http2 import HTTP2Connection
    except ImportError as exc:  # pragma: no cover
        logger.warning("http2 stream-overflow patch skipped: %s", exc)
        return False

    _patch_is_available(AsyncHTTP2Connection)
    _patch_is_available(HTTP2Connection)
    _patch_async_connection(AsyncHTTP2Connection)
    _patch_sync_connection(HTTP2Connection)

    _installed = True
    logger.debug("installed httpcore HTTP/2 stream-overflow connection patch")
    return True
