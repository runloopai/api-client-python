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

import time
import logging
import threading
from typing import TYPE_CHECKING, Dict, Tuple, Callable, Optional
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ..types import DevboxEvictionEventView
    from .devbox import Devbox
    from .._client import Runloop
    from .._streaming import Stream

EvictionCallback = Callable[["Devbox", int], None]
"""Invoked once when the devbox it was registered for has a pending eviction.

Receives the :class:`~runloop_api_client.sdk.devbox.Devbox` and the eviction
deadline as a Unix timestamp in milliseconds.
"""

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
        self._callbacks: Dict[str, Tuple["Devbox", EvictionCallback]] = {}
        self._thread: Optional[threading.Thread] = None
        self._stream: Optional["Stream[DevboxEvictionEventView]"] = None

    def register(self, devbox: "Devbox", callback: EvictionCallback) -> None:
        """Add ``devbox`` to the interest set, starting the stream if idle."""
        with self._lock:
            self._callbacks[devbox.id] = (devbox, callback)
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

    # Reconnect backoff bounds (seconds). The server force-closes the stream on purpose — on a
    # leader change (FAILED_PRECONDITION) or a slow consumer (RESOURCE_EXHAUSTED) — and expects the
    # client to reconnect and re-read the snapshot, which re-delivers anything missed. So a single
    # stream ending is normal, not terminal: reconnect until no devbox is still interested.
    _RECONNECT_BACKOFF_INITIAL_S = 0.5
    _RECONNECT_BACKOFF_MAX_S = 30.0

    def _run(self) -> None:
        backoff = self._RECONNECT_BACKOFF_INITIAL_S
        try:
            while True:
                with self._lock:
                    if not self._callbacks:
                        return
                try:
                    # Force the SSE Accept header: the endpoint only streams for
                    # text/event-stream; the generated client's default (application/json) gets an
                    # empty text/plain response, so the feed would silently deliver nothing.
                    stream = self._client.devboxes.watch_evictions(
                        extra_headers={"Accept": "text/event-stream"}
                    )
                    with self._lock:
                        self._stream = stream
                    _logger.debug("eviction monitor stream connected")
                    with stream:
                        for event in stream:
                            _logger.debug("eviction monitor received event for %s", event.devbox_id)
                            self._dispatch(event)
                            with self._lock:
                                if not self._callbacks:
                                    return
                    # Clean end (server closed the stream): reset backoff and reconnect if still
                    # interested. The reconnect's snapshot re-delivers still-pending evictions.
                    backoff = self._RECONNECT_BACKOFF_INITIAL_S
                    _logger.debug("eviction monitor stream ended; reconnecting")
                except Exception:
                    # An intentional teardown (close/unregister clears the interest set, then closes
                    # the stream) surfaces here as a read error — exit quietly in that case.
                    with self._lock:
                        interested = bool(self._callbacks)
                    if not interested:
                        return
                    # Routine: the server force-closes on leader change / slow consumer, and a
                    # long-lived stream can drop (e.g. an HTTP/2 disconnect). Reconnecting recovers
                    # it, so keep this at debug to avoid log spam.
                    _logger.debug("eviction monitor stream error; reconnecting", exc_info=True)
                with self._lock:
                    if not self._callbacks:
                        return
                time.sleep(backoff)
                backoff = min(backoff * 2, self._RECONNECT_BACKOFF_MAX_S)
        finally:
            with self._lock:
                self._stream = None
                self._thread = None

    def _dispatch(self, event: "DevboxEvictionEventView") -> None:
        with self._lock:
            entry = self._callbacks.pop(event.devbox_id, None)
        if entry is None:
            return
        devbox, callback = entry
        try:
            callback(devbox, event.eviction_deadline_ms)
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
