"""Comprehensive tests for AsyncExecution class."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import (
    TASK_COMPLETION_LONG,
    TASK_COMPLETION_SHORT,
    MockExecutionView,
)
from runloop_api_client.sdk.async_execution import AsyncExecution, _AsyncStreamingGroup

# Legacy aliases for backward compatibility
SHORT_SLEEP = TASK_COMPLETION_SHORT
LONG_SLEEP = TASK_COMPLETION_LONG


class TestAsyncStreamingGroup:
    """Tests for _AsyncStreamingGroup."""

    @pytest.mark.asyncio
    async def test_wait(self) -> None:
        """Test wait method."""

        async def task() -> None:
            await asyncio.sleep(SHORT_SLEEP)

        tasks = [asyncio.create_task(task())]
        group = _AsyncStreamingGroup(tasks)
        await group.wait()

        assert all(task.done() for task in tasks)

    @pytest.mark.asyncio
    async def test_cancel(self) -> None:
        """Test cancel method."""

        async def task() -> None:
            await asyncio.sleep(LONG_SLEEP)  # Long-running task

        tasks = [asyncio.create_task(task())]
        group = _AsyncStreamingGroup(tasks)
        await group.cancel()

        # All tasks should be cancelled
        assert all(task.cancelled() for task in tasks)

    @pytest.mark.asyncio
    async def test_wait_multiple_tasks(self) -> None:
        """Test wait with multiple tasks."""
        MEDIUM_SLEEP = 0.02

        async def task1() -> None:
            await asyncio.sleep(SHORT_SLEEP)

        async def task2() -> None:
            await asyncio.sleep(MEDIUM_SLEEP)

        tasks = [asyncio.create_task(task1()), asyncio.create_task(task2())]
        group = _AsyncStreamingGroup(tasks)
        await group.wait()

        assert all(task.done() for task in tasks)

    @pytest.mark.asyncio
    async def test_cancel_multiple_tasks(self) -> None:
        """Test cancel with multiple tasks."""

        async def task1() -> None:
            await asyncio.sleep(1.0)

        async def task2() -> None:
            await asyncio.sleep(1.0)

        tasks = [asyncio.create_task(task1()), asyncio.create_task(task2())]
        group = _AsyncStreamingGroup(tasks)
        await group.cancel()

        assert all(task.cancelled() for task in tasks)


class TestAsyncExecution:
    """Tests for AsyncExecution class."""

    def test_init(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test AsyncExecution initialization."""
        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"
        assert execution._initial_result == execution_view

    @pytest.mark.asyncio
    async def test_init_with_streaming_group(
        self,
        mock_async_client: AsyncMock,
        execution_view: MockExecutionView,
        async_task_cleanup: list[asyncio.Task[Any]],
    ) -> None:
        """Test AsyncExecution initialization with streaming group."""

        async def task() -> None:
            await asyncio.sleep(SHORT_SLEEP)

        tasks = [asyncio.create_task(task())]
        # Register tasks for automatic cleanup
        async_task_cleanup.extend(tasks)
        streaming_group = _AsyncStreamingGroup(tasks)

        execution = AsyncExecution(mock_async_client, "dev_123", execution_view, streaming_group)  # type: ignore[arg-type]
        assert execution._streaming_group is streaming_group

    def test_properties(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test AsyncExecution properties."""
        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"

    def test_repr(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test AsyncExecution repr formatting."""
        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert repr(execution) == "<AsyncExecution id='exec_123'>"

    @pytest.mark.asyncio
    async def test_result_already_completed(
        self, mock_async_client: AsyncMock, execution_view: MockExecutionView
    ) -> None:
        """Test result when execution is already completed."""
        mock_async_client.devboxes.wait_for_command = AsyncMock(return_value=execution_view)

        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        result = await execution.result()

        assert result.exit_code == 0
        assert await result.stdout(num_lines=10) == "output"
        mock_async_client.devboxes.wait_for_command.assert_awaited_once_with(
            "exec_123",
            devbox_id="dev_123",
            statuses=["completed"],
        )

    @pytest.mark.asyncio
    async def test_result_needs_polling(self, mock_async_client: AsyncMock) -> None:
        """Test result when execution needs polling."""
        running_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )
        completed_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="output",
            stderr="",
            stdout_truncated=False,
            stderr_truncated=False,
        )

        mock_async_client.devboxes.wait_for_command = AsyncMock(return_value=completed_execution)

        execution = AsyncExecution(mock_async_client, "dev_123", running_execution)  # type: ignore[arg-type]
        result = await execution.result()

        assert result.exit_code == 0
        assert await result.stdout(num_lines=10) == "output"
        mock_async_client.devboxes.wait_for_command.assert_awaited_once_with(
            "exec_123",
            devbox_id="dev_123",
            statuses=["completed"],
        )

    @pytest.mark.asyncio
    async def test_result_with_streaming_group(self, mock_async_client: AsyncMock) -> None:
        """Test result with streaming group cleanup."""
        running_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )
        completed_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="output",
            stderr="",
        )

        mock_async_client.devboxes.wait_for_command = AsyncMock(return_value=completed_execution)

        async def task() -> None:
            await asyncio.sleep(SHORT_SLEEP)

        tasks = [asyncio.create_task(task())]
        streaming_group = _AsyncStreamingGroup(tasks)

        execution = AsyncExecution(mock_async_client, "dev_123", running_execution, streaming_group)  # type: ignore[arg-type]
        result = await execution.result()

        assert result.exit_code == 0
        assert execution._streaming_group is None  # Should be cleaned up
        mock_async_client.devboxes.wait_for_command.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_result_passes_options(self, mock_async_client: AsyncMock) -> None:
        """Ensure result forwards options to wait_for_command."""
        execution_view = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="output",
            stderr="",
        )

        mock_async_client.devboxes.wait_for_command = AsyncMock(return_value=execution_view)

        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        await execution.result(timeout=30.0, idempotency_key="abc123")

        mock_async_client.devboxes.wait_for_command.assert_awaited_once_with(
            "exec_123",
            devbox_id="dev_123",
            statuses=["completed"],
            timeout=30.0,
            idempotency_key="abc123",
        )

    @pytest.mark.asyncio
    async def test_get_state(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test get_state method."""
        updated_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )
        mock_async_client.devboxes.executions.retrieve = AsyncMock(return_value=updated_execution)

        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        result = await execution.get_state()

        assert result == updated_execution
        assert execution._initial_result == execution_view
        mock_async_client.devboxes.executions.retrieve.assert_awaited_once_with(
            "exec_123",
            devbox_id="dev_123",
        )

    @pytest.mark.asyncio
    async def test_kill(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test kill method."""
        mock_async_client.devboxes.executions.kill = AsyncMock(return_value=None)

        execution = AsyncExecution(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        await execution.kill()

        mock_async_client.devboxes.executions.kill.assert_awaited_once_with(
            "exec_123",
            devbox_id="dev_123",
        )
