"""Async client-side eviction notification monitor.

Async counterpart of :mod:`runloop_api_client.sdk.eviction`; see that module for the
delivery contract. Callbacks may be plain functions or coroutines.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from typing import TYPE_CHECKING, Dict, Tuple, Union, Callable, Optional, Awaitable
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ..types import DevboxEvictionEventView
    from .._client import AsyncRunloop
    from .._streaming import AsyncStream
    from .async_devbox import AsyncDevbox

AsyncEvictionCallback = Callable[["AsyncDevbox", int], Union[None, Awaitable[None]]]
"""Sync or async callable invoked once with the devbox and its eviction deadline (ms)."""

_logger = logging.getLogger(__name__)


class AsyncEvictionMonitor:
    """Async fan-out of account-wide eviction notifications to per-devbox callbacks."""

    def __init__(self, client: "AsyncRunloop") -> None:
        self._client = client
        self._lock = asyncio.Lock()
        self._callbacks: Dict[str, Tuple["AsyncDevbox", AsyncEvictionCallback]] = {}
        self._task: Optional["asyncio.Task[None]"] = None
        self._stream: Optional["AsyncStream[DevboxEvictionEventView]"] = None

    async def register(self, devbox: "AsyncDevbox", callback: AsyncEvictionCallback) -> None:
        """Add ``devbox`` to the interest set, starting the stream task if idle."""
        async with self._lock:
            self._callbacks[devbox.id] = (devbox, callback)
            if self._task is None or self._task.done():
                self._task = asyncio.create_task(self._run(), name="runloop-eviction-monitor")

    async def unregister(self, devbox_id: str) -> None:
        """Drop ``devbox_id``; close the stream if it was the last interested devbox."""
        async with self._lock:
            self._callbacks.pop(devbox_id, None)
            empty = not self._callbacks
        if empty:
            await self._close_stream()

    async def close(self) -> None:
        """Clear all interest and tear down the stream."""
        async with self._lock:
            self._callbacks.clear()
        await self._close_stream()

    # Reconnect backoff bounds (seconds). The server force-closes the stream on purpose — on a
    # leader change (FAILED_PRECONDITION) or a slow consumer (RESOURCE_EXHAUSTED) — and expects the
    # client to reconnect and re-read the snapshot, which re-delivers anything missed. So a single
    # stream ending is normal, not terminal: reconnect until no devbox is still interested.
    _RECONNECT_BACKOFF_INITIAL_S = 0.5
    _RECONNECT_BACKOFF_MAX_S = 30.0

    async def _run(self) -> None:
        backoff = self._RECONNECT_BACKOFF_INITIAL_S
        try:
            while True:
                async with self._lock:
                    if not self._callbacks:
                        return
                try:
                    # Force the SSE Accept header: the endpoint only streams for
                    # text/event-stream; the generated client's default (application/json) gets an
                    # empty text/plain response, so the feed would silently deliver nothing.
                    stream = await self._client.devboxes.watch_evictions(extra_headers={"Accept": "text/event-stream"})
                    async with self._lock:
                        self._stream = stream
                    _logger.debug("async eviction monitor stream connected")
                    async with stream:
                        async for event in stream:
                            _logger.debug("async eviction monitor received event for %s", event.devbox_id)
                            await self._dispatch(event)
                            async with self._lock:
                                if not self._callbacks:
                                    return
                    # Clean end (server closed the stream): reset backoff and reconnect if still
                    # interested. The reconnect's snapshot re-delivers still-pending evictions.
                    backoff = self._RECONNECT_BACKOFF_INITIAL_S
                    _logger.debug("async eviction monitor stream ended; reconnecting")
                except asyncio.CancelledError:
                    raise
                except Exception:
                    # An intentional teardown (close/unregister clears the interest set, then closes
                    # the stream) surfaces here as a read error — exit quietly in that case.
                    async with self._lock:
                        interested = bool(self._callbacks)
                    if not interested:
                        return
                    # Routine: the server force-closes on leader change / slow consumer, and a
                    # long-lived stream can drop (e.g. an HTTP/2 disconnect). Reconnecting recovers
                    # it, so keep this at debug to avoid log spam.
                    _logger.debug("async eviction monitor stream error; reconnecting", exc_info=True)
                async with self._lock:
                    if not self._callbacks:
                        return
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, self._RECONNECT_BACKOFF_MAX_S)
        finally:
            async with self._lock:
                self._stream = None
                self._task = None

    async def _dispatch(self, event: "DevboxEvictionEventView") -> None:
        async with self._lock:
            entry = self._callbacks.pop(event.devbox_id, None)
        if entry is None:
            return
        devbox, callback = entry
        try:
            result = callback(devbox, event.eviction_deadline_ms)
            if inspect.isawaitable(result):
                await result
        except Exception:
            _logger.exception("error in eviction callback for devbox %s", event.devbox_id)

    async def _close_stream(self) -> None:
        async with self._lock:
            stream = self._stream
            self._stream = None
        if stream is not None:
            try:
                await stream.close()
            except Exception:
                _logger.debug("error closing eviction stream", exc_info=True)


# asyncio is single-threaded, so the registry needs no lock.
_monitors: "WeakKeyDictionary[AsyncRunloop, AsyncEvictionMonitor]" = WeakKeyDictionary()


def monitor_for(client: "AsyncRunloop") -> AsyncEvictionMonitor:
    """Return the shared :class:`AsyncEvictionMonitor` for ``client``, creating it once."""
    monitor = _monitors.get(client)
    if monitor is None:
        monitor = AsyncEvictionMonitor(client)
        _monitors[client] = monitor
    return monitor


async def shutdown_monitor_for(client: "AsyncRunloop") -> None:
    """Tear down the shared monitor for ``client`` if one exists."""
    monitor = _monitors.pop(client, None)
    if monitor is not None:
        await monitor.close()
