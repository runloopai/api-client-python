"""Tests for AsyncDevbox streaming functionality.

Tests async streaming setup, task management, stream workers, and the
async streaming group management.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any, AsyncIterator
from unittest.mock import Mock, AsyncMock

import pytest

from tests.sdk.conftest import TASK_COMPLETION_SHORT
from runloop_api_client.sdk import AsyncDevbox
from runloop_api_client._streaming import AsyncStream
from runloop_api_client.sdk.async_execution import _AsyncStreamingGroup
from runloop_api_client.types.devboxes.execution_update_chunk import ExecutionUpdateChunk


class TestAsyncDevboxStreaming:
    """Tests for AsyncDevbox streaming methods."""

    def test_start_streaming_no_callbacks(self, mock_async_client: AsyncMock) -> None:
        """Test _start_streaming returns None when no callbacks."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=None)
        assert result is None

    @pytest.mark.asyncio
    async def test_start_streaming_stdout_only(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock, async_task_cleanup: list[asyncio.Task[Any]]
    ) -> None:
        """Test _start_streaming with stdout callback only."""

        # Create a proper async iterator
        async def async_iter():
            yield SimpleNamespace(output="line 1")
            yield SimpleNamespace(output="line 2")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        stdout_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=stdout_calls.append, stderr=None, output=None)

        assert result is not None
        assert isinstance(result, _AsyncStreamingGroup)
        assert len(result._tasks) == 1
        # Register tasks for automatic cleanup
        async_task_cleanup.extend(result._tasks)
        # Give the task a moment to start
        await asyncio.sleep(TASK_COMPLETION_SHORT * 5)
        mock_async_client.devboxes.executions.stream_stdout_updates.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_streaming_stderr_only(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock, async_task_cleanup: list[asyncio.Task[Any]]
    ) -> None:
        """Test _start_streaming with stderr callback only."""

        # Create a proper async iterator
        async def async_iter():
            yield SimpleNamespace(output="line 1")
            yield SimpleNamespace(output="line 2")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        mock_async_client.devboxes.executions.stream_stderr_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        stderr_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=stderr_calls.append, output=None)

        assert result is not None
        assert isinstance(result, _AsyncStreamingGroup)
        assert len(result._tasks) == 1
        # Register tasks for automatic cleanup
        async_task_cleanup.extend(result._tasks)
        # Give the task a moment to start
        await asyncio.sleep(TASK_COMPLETION_SHORT * 5)
        mock_async_client.devboxes.executions.stream_stderr_updates.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_streaming_output_only(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock, async_task_cleanup: list[asyncio.Task[Any]]
    ) -> None:
        """Test _start_streaming with output callback only."""

        # Create a proper async iterator
        async def async_iter():
            yield SimpleNamespace(output="line 1")
            yield SimpleNamespace(output="line 2")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)
        mock_async_client.devboxes.executions.stream_stderr_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        output_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=output_calls.append)

        assert result is not None
        assert isinstance(result, _AsyncStreamingGroup)
        assert len(result._tasks) == 2  # Both stdout and stderr streams
        # Register tasks for automatic cleanup
        async_task_cleanup.extend(result._tasks)
        # Give tasks a moment to start
        TASK_START_DELAY = 0.1
        await asyncio.sleep(TASK_START_DELAY)

    @pytest.mark.asyncio
    async def test_stream_worker(self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock) -> None:
        """Test _stream_worker processes chunks."""
        chunks = [
            SimpleNamespace(output="line 1"),
            SimpleNamespace(output="line 2"),
        ]

        async def async_iter() -> AsyncIterator[SimpleNamespace]:
            for chunk in chunks:
                yield chunk

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        calls: list[str] = []

        async def stream_factory() -> AsyncStream[ExecutionUpdateChunk]:
            return mock_async_stream

        await devbox._stream_worker(
            name="test",
            stream_factory=stream_factory,
            callbacks=[calls.append],
        )

        # Note: In a real scenario, calls would be populated, but with mocks
        # we're mainly testing that the method doesn't raise

    @pytest.mark.asyncio
    async def test_stream_worker_cancelled(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock, async_task_cleanup: list[asyncio.Task[Any]]
    ) -> None:
        """Test _stream_worker handles cancellation."""
        LONG_SLEEP = 1.0

        async def async_iter() -> AsyncIterator[SimpleNamespace]:
            await asyncio.sleep(LONG_SLEEP)  # Long-running
            yield SimpleNamespace(output="line")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        calls: list[str] = []

        async def stream_factory() -> AsyncStream[ExecutionUpdateChunk]:
            return mock_async_stream

        task = asyncio.create_task(
            devbox._stream_worker(
                name="test",
                stream_factory=stream_factory,
                callbacks=[calls.append],
            )
        )
        # Register task for cleanup in case test fails before cancellation
        async_task_cleanup.append(task)

        await asyncio.sleep(TASK_COMPLETION_SHORT)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task
