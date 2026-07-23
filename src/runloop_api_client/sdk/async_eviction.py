"""Async client-side eviction notification monitor.

Async counterpart of :mod:`runloop_api_client.sdk.eviction`; see that module for the
delivery contract. Callbacks may be plain functions or coroutines.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from typing import TYPE_CHECKING, Dict, Union, Callable, Optional, Awaitable
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from .._client import AsyncRunloop
    from .._streaming import AsyncStream

    # Assumed Stainless-generated SSE event type for ``watch_evictions``; carries
    # ``devbox_id`` and ``eviction_deadline_ms``. Reconcile the import once the
    # generated code lands.
    from ..types import DevboxEvictionEvent

AsyncEvictionCallback = Callable[["DevboxEvictionEvent"], Union[None, Awaitable[None]]]
"""Sync or async callable invoked once with the eviction event for its devbox."""

_logger = logging.getLogger(__name__)


class AsyncEvictionMonitor:
    """Async fan-out of account-wide eviction notifications to per-devbox callbacks."""

    def __init__(self, client: "AsyncRunloop") -> None:
        self._client = client
        self._lock = asyncio.Lock()
        self._callbacks: Dict[str, AsyncEvictionCallback] = {}
        self._task: Optional["asyncio.Task[None]"] = None
        self._stream: Optional["AsyncStream[DevboxEvictionEvent]"] = None

    async def register(self, devbox_id: str, callback: AsyncEvictionCallback) -> None:
        """Add ``devbox_id`` to the interest set, starting the stream task if idle."""
        async with self._lock:
            self._callbacks[devbox_id] = callback
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

    async def _run(self) -> None:
        try:
            stream = await self._client.devboxes.watch_evictions()
            async with self._lock:
                self._stream = stream
            async with stream:
                async for event in stream:
                    await self._dispatch(event)
                    async with self._lock:
                        if not self._callbacks:
                            break
        except asyncio.CancelledError:
            raise
        except Exception:
            _logger.exception("async eviction monitor stream failed")
        finally:
            async with self._lock:
                self._stream = None
                self._task = None

    async def _dispatch(self, event: "DevboxEvictionEvent") -> None:
        async with self._lock:
            callback = self._callbacks.pop(event.devbox_id, None)
        if callback is None:
            return
        try:
            result = callback(event)
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
