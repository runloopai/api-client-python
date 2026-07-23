"""Client-side eviction notification monitor.

Backs :meth:`runloop_api_client.sdk.devbox.Devbox.on_evict`. A single account-wide
SSE stream (the generated ``devboxes.watch_evictions`` endpoint) is opened lazily
the moment the first devbox registers interest, and torn down as soon as the last
interested devbox has been notified.

Delivery contract:

* The server replays every currently-pending eviction on connect, so a devbox that
  registers after its eviction was scheduled is still notified.
* Notifications for devboxes not in the interest set are discarded.
* A devbox is removed from the interest set *before* its callback runs, so the
  callback fires at most once even if the server repeats the notification.
"""

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Dict, Callable, Optional
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from .._client import Runloop
    from .._streaming import Stream

    # Assumed Stainless-generated SSE event type for ``watch_evictions``; carries
    # ``devbox_id`` and ``eviction_deadline_ms``. Reconcile the import once the
    # generated code lands.
    from ..types import DevboxEvictionEvent

EvictionCallback = Callable[["DevboxEvictionEvent"], None]
"""Invoked once with the eviction event for the devbox it was registered for."""

_logger = logging.getLogger(__name__)


class EvictionMonitor:
    """Fans account-wide eviction notifications out to per-devbox callbacks.

    One monitor is shared by every :class:`~runloop_api_client.sdk.devbox.Devbox`
    built from the same generated client (see :func:`monitor_for`), so all
    registered devboxes are served by a single SSE connection.
    """

    def __init__(self, client: "Runloop") -> None:
        self._client = client
        self._lock = threading.Lock()
        self._callbacks: Dict[str, EvictionCallback] = {}
        self._thread: Optional[threading.Thread] = None
        self._stream: Optional["Stream[DevboxEvictionEvent]"] = None

    def register(self, devbox_id: str, callback: EvictionCallback) -> None:
        """Add ``devbox_id`` to the interest set, starting the stream if idle."""
        with self._lock:
            self._callbacks[devbox_id] = callback
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(
                    target=self._run,
                    name="runloop-eviction-monitor",
                    daemon=True,
                )
                self._thread.start()

    def unregister(self, devbox_id: str) -> None:
        """Drop ``devbox_id``; close the stream if it was the last interested devbox."""
        with self._lock:
            self._callbacks.pop(devbox_id, None)
            empty = not self._callbacks
        if empty:
            self._close_stream()

    def close(self) -> None:
        """Clear all interest and tear down the stream."""
        with self._lock:
            self._callbacks.clear()
        self._close_stream()

    def _run(self) -> None:
        try:
            stream = self._client.devboxes.watch_evictions()
            with self._lock:
                self._stream = stream
            with stream:
                for event in stream:
                    self._dispatch(event)
                    with self._lock:
                        if not self._callbacks:
                            break
        except Exception:
            _logger.exception("eviction monitor stream failed")
        finally:
            with self._lock:
                self._stream = None
                self._thread = None

    def _dispatch(self, event: "DevboxEvictionEvent") -> None:
        with self._lock:
            callback = self._callbacks.pop(event.devbox_id, None)
        if callback is None:
            return
        try:
            callback(event)
        except Exception:
            _logger.exception("error in eviction callback for devbox %s", event.devbox_id)

    def _close_stream(self) -> None:
        with self._lock:
            stream = self._stream
            self._stream = None
        if stream is not None:
            try:
                stream.close()
            except Exception:
                _logger.debug("error closing eviction stream", exc_info=True)


_monitors: "WeakKeyDictionary[Runloop, EvictionMonitor]" = WeakKeyDictionary()
_monitors_lock = threading.Lock()


def monitor_for(client: "Runloop") -> EvictionMonitor:
    """Return the shared :class:`EvictionMonitor` for ``client``, creating it once."""
    with _monitors_lock:
        monitor = _monitors.get(client)
        if monitor is None:
            monitor = EvictionMonitor(client)
            _monitors[client] = monitor
        return monitor


def shutdown_monitor_for(client: "Runloop") -> None:
    """Tear down the shared monitor for ``client`` if one exists."""
    with _monitors_lock:
        monitor = _monitors.pop(client, None)
    if monitor is not None:
        monitor.close()
