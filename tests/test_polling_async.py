"""Tests for async polling with cancellation."""

import asyncio
from typing import Any
from unittest.mock import Mock, AsyncMock, patch

import pytest

from src.runloop_api_client.lib.polling import PollingConfig, PollingTimeout
from src.runloop_api_client.lib.polling_async import async_poll_until
from src.runloop_api_client.lib.cancellation import CancellationToken, PollingCancelled


class TestAsyncPollUntil:
    """Test async_poll_until function."""

    @pytest.mark.asyncio
    async def test_immediate_success(self):
        """Test when condition is met on first attempt."""
        retriever = AsyncMock(return_value="completed")
        is_terminal = Mock(return_value=True)

        result = await async_poll_until(retriever, is_terminal)

        assert result == "completed"
        assert retriever.call_count == 1
        assert is_terminal.call_count == 1

    @pytest.mark.asyncio
    async def test_success_after_multiple_attempts(self):
        """Test when condition is met after several attempts."""
        values = ["pending", "running", "completed"]
        retriever = AsyncMock(side_effect=values)
        is_terminal = Mock(side_effect=[False, False, True])

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            result = await async_poll_until(retriever, is_terminal)

        assert result == "completed"
        assert retriever.call_count == 3
        assert is_terminal.call_count == 3
        assert mock_sleep.call_count == 2

    @pytest.mark.asyncio
    async def test_max_attempts_exceeded(self):
        """Test when max attempts is exceeded."""
        retriever = AsyncMock(return_value="still_running")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(max_attempts=3, interval_seconds=0.01)

        with patch("asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(PollingTimeout) as exc_info:
                await async_poll_until(retriever, is_terminal, config)

        assert "Exceeded maximum attempts (3)" in str(exc_info.value)
        assert retriever.call_count == 3

    @pytest.mark.asyncio
    async def test_timeout_exceeded(self):
        """Test when timeout is exceeded."""
        retriever = AsyncMock(return_value="still_running")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(timeout_seconds=0.1, interval_seconds=0.01)

        start_time = 1000.0
        with patch("time.time", side_effect=[start_time, start_time + 0.05, start_time + 0.15]):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                with pytest.raises(PollingTimeout) as exc_info:
                    await async_poll_until(retriever, is_terminal, config)

        assert "Exceeded timeout of 0.1 seconds" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_error_without_handler(self):
        """Test that exceptions are re-raised when no error handler is provided."""
        retriever = AsyncMock(side_effect=ValueError("Test error"))
        is_terminal = Mock(return_value=False)

        with pytest.raises(ValueError, match="Test error"):
            await async_poll_until(retriever, is_terminal)

    @pytest.mark.asyncio
    async def test_error_with_handler_continue(self):
        """Test error handler that allows polling to continue."""
        retriever = AsyncMock(side_effect=[ValueError("Test error"), "recovered"])
        is_terminal = Mock(side_effect=[False, True])

        def error_handler(_: Exception) -> str:
            return "error_handled"

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await async_poll_until(retriever, is_terminal, on_error=error_handler)

        assert result == "recovered"
        assert retriever.call_count == 2


class TestAsyncPollUntilWithCancellation:
    """Test async_poll_until with CancellationToken."""

    @pytest.mark.asyncio
    async def test_cancellation_before_first_poll(self):
        """Test cancellation before first poll attempt."""
        token = CancellationToken()
        token.cancel()

        retriever = AsyncMock(return_value="value")
        is_terminal = Mock(return_value=False)

        with pytest.raises(PollingCancelled, match="Polling operation was cancelled"):
            await async_poll_until(retriever, is_terminal, cancellation_token=token)

        assert retriever.call_count == 0

    @pytest.mark.asyncio
    async def test_cancellation_during_polling(self):
        """Test cancellation during polling loop."""
        token = CancellationToken()
        retriever = AsyncMock(side_effect=["value1", "value2", "value3"])
        is_terminal = Mock(return_value=False)

        call_count = 0

        async def cancel_on_second_call(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                token.cancel()
            if token.is_cancelled():
                raise PollingCancelled("Polling operation was cancelled")

        with patch("asyncio.sleep", side_effect=cancel_on_second_call):
            with pytest.raises(PollingCancelled):
                await async_poll_until(retriever, is_terminal, cancellation_token=token)

        assert retriever.call_count == 2

    @pytest.mark.asyncio
    async def test_cancellation_during_sleep(self):
        """Test that cancellation wakes up from sleep."""
        token = CancellationToken()
        retriever = AsyncMock(return_value="value")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(interval_seconds=10.0)  # Long sleep

        async def cancel_after_delay():
            await asyncio.sleep(0.05)
            token.cancel()

        # Start cancellation task
        cancel_task = asyncio.create_task(cancel_after_delay())

        # Poll should be interrupted by cancellation
        with pytest.raises(PollingCancelled):
            await async_poll_until(retriever, is_terminal, config, cancellation_token=token)

        await cancel_task

        # Should have attempted once before cancellation
        assert retriever.call_count == 1

    @pytest.mark.asyncio
    async def test_no_cancellation_completes_normally(self):
        """Test that polling completes normally without cancellation."""
        token = CancellationToken()
        retriever = AsyncMock(side_effect=["pending", "completed"])
        is_terminal = Mock(side_effect=[False, True])

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await async_poll_until(retriever, is_terminal, cancellation_token=token)

        assert result == "completed"
        assert not token.is_cancelled()

    @pytest.mark.asyncio
    async def test_cancellation_after_completion_no_effect(self):
        """Test that cancelling after completion has no effect."""
        token = CancellationToken()
        retriever = AsyncMock(return_value="completed")
        is_terminal = Mock(return_value=True)

        result = await async_poll_until(retriever, is_terminal, cancellation_token=token)

        token.cancel()

        assert result == "completed"

    @pytest.mark.asyncio
    async def test_cancellation_with_error_handler(self):
        """Test cancellation works with error handler."""
        token = CancellationToken()
        retriever = AsyncMock(side_effect=[ValueError("error"), "value"])
        is_terminal = Mock(return_value=False)

        def error_handler(_: Exception) -> str:
            return "handled"

        async def cancel_on_first_sleep(*args, **kwargs):
            token.cancel()
            raise PollingCancelled("Polling operation was cancelled")

        with patch("asyncio.sleep", side_effect=cancel_on_first_sleep):
            with pytest.raises(PollingCancelled):
                await async_poll_until(retriever, is_terminal, on_error=error_handler, cancellation_token=token)

    @pytest.mark.asyncio
    async def test_none_cancellation_token_works_normally(self):
        """Test that passing None as cancellation_token works (backward compatibility)."""
        retriever = AsyncMock(side_effect=["pending", "completed"])
        is_terminal = Mock(side_effect=[False, True])

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await async_poll_until(retriever, is_terminal, cancellation_token=None)

        assert result == "completed"

    @pytest.mark.asyncio
    async def test_cancellable_sleep_blocks_correctly(self):
        """Test that cancellable sleep blocks for the correct duration."""
        token = CancellationToken()
        retriever = AsyncMock(side_effect=["pending", "completed"])
        is_terminal = Mock(side_effect=[False, True])
        config = PollingConfig(interval_seconds=0.1)

        start = asyncio.get_event_loop().time()
        result = await async_poll_until(retriever, is_terminal, config, cancellation_token=token)
        elapsed = asyncio.get_event_loop().time() - start

        assert result == "completed"
        # Should have slept approximately 0.1 seconds
        assert 0.08 <= elapsed <= 0.15

    @pytest.mark.asyncio
    async def test_concurrent_polling_with_shared_token(self):
        """Test multiple concurrent polls with the same token."""
        token = CancellationToken()

        async def poll_task():
            retriever = AsyncMock(return_value="value")
            is_terminal = Mock(return_value=False)
            config = PollingConfig(interval_seconds=0.01)
            await async_poll_until(retriever, is_terminal, config, cancellation_token=token)

        # Start multiple polling tasks
        tasks = [asyncio.create_task(poll_task()) for _ in range(3)]

        # Give them time to start
        await asyncio.sleep(0.05)

        # Cancel the shared token
        token.cancel()

        # All tasks should raise PollingCancelled
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            assert isinstance(result, PollingCancelled)

    @pytest.mark.asyncio
    async def test_cancellation_timeout_error_handling(self):
        """Test that asyncio.TimeoutError during cancellable sleep is handled correctly."""
        token = CancellationToken()
        retriever = AsyncMock(side_effect=["value1", "completed"])
        is_terminal = Mock(side_effect=[False, True])
        config = PollingConfig(interval_seconds=0.1)

        # The cancellable sleep should handle TimeoutError correctly and continue
        result = await async_poll_until(retriever, is_terminal, config, cancellation_token=token)

        assert result == "completed"
        assert retriever.call_count == 2

    @pytest.mark.asyncio
    async def test_cancellation_from_different_task(self):
        """Test that token can be cancelled from a different async task."""
        token = CancellationToken()
        retriever = AsyncMock(return_value="value")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(interval_seconds=1.0)

        async def cancel_from_other_task():
            await asyncio.sleep(0.1)
            token.cancel()

        # Start both tasks
        poll_task = asyncio.create_task(async_poll_until(retriever, is_terminal, config, cancellation_token=token))
        cancel_task = asyncio.create_task(cancel_from_other_task())

        # Wait for both
        with pytest.raises(PollingCancelled):
            await poll_task

        await cancel_task
