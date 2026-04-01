"""Tests for CancellationToken and PollingCancelled exception."""

import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

import pytest

from src.runloop_api_client.lib.cancellation import CancellationToken, PollingCancelled


class TestPollingCancelled:
    """Test PollingCancelled exception."""

    def test_polling_cancelled_initialization(self):
        """Test PollingCancelled exception initialization."""
        exception = PollingCancelled("Operation was cancelled")
        assert "Operation was cancelled" in str(exception)

    def test_polling_cancelled_inherits_from_runloop_error(self):
        """Test that PollingCancelled inherits from RunloopError."""
        from src.runloop_api_client._exceptions import RunloopError

        exception = PollingCancelled("Test")
        assert isinstance(exception, RunloopError)


class TestCancellationToken:
    """Test CancellationToken class."""

    def test_initialization(self):
        """Test token is not cancelled on initialization."""
        token = CancellationToken()
        assert not token.is_cancelled()

    def test_cancel(self):
        """Test cancelling a token."""
        token = CancellationToken()
        token.cancel()
        assert token.is_cancelled()

    def test_cancel_idempotent(self):
        """Test that calling cancel() multiple times is safe."""
        token = CancellationToken()
        token.cancel()
        token.cancel()
        token.cancel()
        assert token.is_cancelled()

    def test_raise_if_cancelled_not_cancelled(self):
        """Test raise_if_cancelled() when token is not cancelled."""
        token = CancellationToken()
        # Should not raise
        token.raise_if_cancelled()

    def test_raise_if_cancelled_when_cancelled(self):
        """Test raise_if_cancelled() when token is cancelled."""
        token = CancellationToken()
        token.cancel()
        with pytest.raises(PollingCancelled, match="Polling operation was cancelled"):
            token.raise_if_cancelled()

    def test_sync_event_property(self):
        """Test sync_event property returns threading.Event."""
        token = CancellationToken()
        event = token.sync_event
        assert isinstance(event, threading.Event)
        assert not event.is_set()

        token.cancel()
        assert event.is_set()

    def test_sync_event_wait(self):
        """Test sync_event can be used with wait()."""
        token = CancellationToken()
        event = token.sync_event

        # Should timeout since not cancelled
        result = event.wait(timeout=0.01)
        assert not result

        token.cancel()
        # Should return immediately when cancelled
        result = event.wait(timeout=1.0)
        assert result

    @pytest.mark.asyncio
    async def test_async_event_property(self):
        """Test async_event property returns asyncio.Event."""
        token = CancellationToken()
        event = token.async_event
        assert isinstance(event, asyncio.Event)
        assert not event.is_set()

        token.cancel()
        assert event.is_set()

    @pytest.mark.asyncio
    async def test_async_event_wait(self):
        """Test async_event can be used with wait()."""
        token = CancellationToken()
        event = token.async_event

        # Should timeout since not cancelled
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(event.wait(), timeout=0.01)

        token.cancel()
        # Should return immediately when cancelled
        await asyncio.wait_for(event.wait(), timeout=1.0)

    @pytest.mark.asyncio
    async def test_async_event_lazy_creation(self):
        """Test that async_event is created lazily."""
        token = CancellationToken()
        # Access _async_event directly to check it's None
        assert token._async_event is None

        # Access property to trigger lazy creation
        event = token.async_event
        assert token._async_event is not None
        assert event is token._async_event

    @pytest.mark.asyncio
    async def test_async_event_set_if_already_cancelled(self):
        """Test that async_event is set immediately if token was already cancelled."""
        token = CancellationToken()
        token.cancel()

        # Async event should be set when created
        event = token.async_event
        assert event.is_set()

    def test_thread_safety(self):
        """Test that CancellationToken is thread-safe."""
        token = CancellationToken()
        results = []

        def cancel_token():
            token.cancel()
            results.append(token.is_cancelled())

        def check_token():
            # Busy wait until cancelled
            while not token.is_cancelled():
                pass
            results.append(token.is_cancelled())

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            # Start 4 checking threads
            for _ in range(4):
                futures.append(executor.submit(check_token))
            # Start 1 cancelling thread
            futures.append(executor.submit(cancel_token))

            # Wait for all to complete
            for future in futures:
                future.result(timeout=2.0)

        # All results should be True
        assert all(results)
        assert len(results) == 5

    def test_sync_and_async_events_synchronized(self):
        """Test that sync and async events are synchronized."""
        token = CancellationToken()

        # Get both events
        sync_event = token.sync_event
        async_event = token.async_event

        assert not sync_event.is_set()
        assert not async_event.is_set()

        # Cancel token
        token.cancel()

        # Both should be set
        assert sync_event.is_set()
        assert async_event.is_set()

    def test_multiple_tokens_independent(self):
        """Test that multiple tokens are independent."""
        token1 = CancellationToken()
        token2 = CancellationToken()

        token1.cancel()

        assert token1.is_cancelled()
        assert not token2.is_cancelled()

    @pytest.mark.asyncio
    async def test_async_cancellation_propagation(self):
        """Test cancellation in async context."""
        token = CancellationToken()

        async def wait_for_cancellation():
            await token.async_event.wait()
            return token.is_cancelled()

        # Start waiting task
        task = asyncio.create_task(wait_for_cancellation())

        # Give it a moment to start
        await asyncio.sleep(0.01)

        # Cancel token
        token.cancel()

        # Task should complete and return True
        result = await asyncio.wait_for(task, timeout=1.0)
        assert result is True
