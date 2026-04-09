"""Cancellation support for polling operations."""

from __future__ import annotations

import asyncio
import threading
from typing import TYPE_CHECKING

from .._exceptions import RunloopError

if TYPE_CHECKING:
    pass

__all__ = ["PollingCancelled", "CancellationToken"]


class PollingCancelled(RunloopError):
    """Exception raised when a polling operation is cancelled."""

    pass


class CancellationToken:
    """Thread-safe cancellation token for polling operations.

    Similar to JavaScript's AbortSignal. Works in both sync and async contexts.

    Example (sync):
        >>> token = CancellationToken()
        >>> # In another thread:
        >>> token.cancel()
        >>> # In polling code:
        >>> token.raise_if_cancelled()  # Raises PollingCancelled

    Example (async):
        >>> token = CancellationToken()
        >>> # In another task:
        >>> token.cancel()
        >>> # In async polling code:
        >>> await asyncio.wait_for(token.async_event.wait(), timeout=1.0)
    """

    def __init__(self) -> None:
        """Create a new cancellation token."""
        self._cancelled = False
        self._sync_event = threading.Event()
        self._async_event: asyncio.Event | None = None
        self._lock = threading.Lock()

    def cancel(self) -> None:
        """Mark this token as cancelled.

        Thread-safe and can be called multiple times. Sets both sync and async events.
        """
        with self._lock:
            if self._cancelled:
                return
            self._cancelled = True
            self._sync_event.set()
            if self._async_event is not None:
                self._async_event.set()

    def is_cancelled(self) -> bool:
        """Check if this token has been cancelled.

        Returns:
            True if cancel() has been called, False otherwise.
        """
        return self._cancelled

    def raise_if_cancelled(self) -> None:
        """Raise PollingCancelled if this token has been cancelled.

        Raises:
            PollingCancelled: If cancel() has been called.
        """
        if self._cancelled:
            raise PollingCancelled("Polling operation was cancelled")

    @property
    def sync_event(self) -> threading.Event:
        """Get the synchronous event for cancellation checking.

        Returns:
            threading.Event that is set when cancel() is called.
        """
        return self._sync_event

    @property
    def async_event(self) -> asyncio.Event:
        """Get the asynchronous event for cancellation checking.

        Lazily creates the async event on first access. If cancel() was already called,
        the event will be set immediately.

        Returns:
            asyncio.Event that is set when cancel() is called.
        """
        if self._async_event is None:
            self._async_event = asyncio.Event()
            if self._cancelled:
                self._async_event.set()
        return self._async_event
