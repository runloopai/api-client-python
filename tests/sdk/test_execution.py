"""Comprehensive tests for Execution class."""

from __future__ import annotations

import time
import threading
from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import (
    THREAD_STARTUP_DELAY,
    TASK_COMPLETION_SHORT,
    MockExecutionView,
)
from runloop_api_client.sdk.execution import Execution, _StreamingGroup

# Legacy aliases for backward compatibility during transition
SHORT_SLEEP = THREAD_STARTUP_DELAY
MEDIUM_SLEEP = TASK_COMPLETION_SHORT * 10  # 0.2


class TestStreamingGroup:
    """Tests for _StreamingGroup."""

    def test_init(self) -> None:
        """Test _StreamingGroup initialization."""
        threads = [threading.Thread(target=lambda: None)]
        stop_event = threading.Event()
        group = _StreamingGroup(threads, stop_event)
        assert group._threads == threads
        assert group._stop_event is stop_event

    def test_stop(self) -> None:
        """Test stop method sets event."""
        stop_event = threading.Event()
        threads = [threading.Thread(target=lambda: None)]
        group = _StreamingGroup(threads, stop_event)

        assert not stop_event.is_set()
        group.stop()
        assert stop_event.is_set()

    def test_join(self) -> None:
        """Test join waits for threads."""
        stop_event = threading.Event()
        thread = threading.Thread(target=lambda: time.sleep(SHORT_SLEEP))
        thread.start()
        group = _StreamingGroup([thread], stop_event)

        group.join(timeout=1.0)
        assert not thread.is_alive()

    def test_active_property(self) -> None:
        """Test active property."""
        stop_event = threading.Event()
        thread = threading.Thread(target=lambda: time.sleep(MEDIUM_SLEEP))
        thread.start()
        group = _StreamingGroup([thread], stop_event)

        assert group.active is True
        thread.join()
        assert group.active is False

    def test_active_multiple_threads(self) -> None:
        """Test active property with multiple threads."""
        stop_event = threading.Event()
        thread1 = threading.Thread(target=lambda: time.sleep(SHORT_SLEEP))
        thread2 = threading.Thread(target=lambda: time.sleep(MEDIUM_SLEEP))
        thread1.start()
        thread2.start()
        group = _StreamingGroup([thread1, thread2], stop_event)

        assert group.active is True
        thread1.join()
        assert group.active is True  # thread2 still active
        thread2.join()
        assert group.active is False


class TestExecution:
    """Tests for Execution class."""

    def test_init(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test Execution initialization."""
        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"
        assert execution._initial_result == execution_view

    def test_init_with_streaming_group(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test Execution initialization with streaming group."""
        threads = [threading.Thread(target=lambda: None)]
        stop_event = threading.Event()
        streaming_group = _StreamingGroup(threads, stop_event)

        execution = Execution(mock_client, "dev_123", execution_view, streaming_group)  # type: ignore[arg-type]
        assert execution._streaming_group is streaming_group

    def test_properties(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test Execution properties."""
        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"

    def test_repr(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test Execution repr formatting."""
        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert repr(execution) == "<Execution id='exec_123'>"

    def test_result_already_completed(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test result delegates to wait_for_command when already completed."""
        mock_client.devboxes = Mock()
        mock_client.devboxes.wait_for_command.return_value = execution_view

        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        result = execution.result()

        assert result.exit_code == 0
        assert result.stdout(num_lines=10) == "output"
        mock_client.devboxes.wait_for_command.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
            statuses=["completed"],
        )

    def test_result_needs_polling(self, mock_client: Mock) -> None:
        """Test result when execution needs to poll for completion."""
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

        mock_client.devboxes = Mock()
        mock_client.devboxes.wait_for_command.return_value = completed_execution

        execution = Execution(mock_client, "dev_123", running_execution)  # type: ignore[arg-type]
        result = execution.result()

        assert result.exit_code == 0
        assert result.stdout(num_lines=10) == "output"
        mock_client.devboxes.wait_for_command.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
            statuses=["completed"],
        )

    def test_result_with_streaming_group(self, mock_client: Mock) -> None:
        """Test result waits for streaming group to finish."""
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

        mock_client.devboxes = Mock()
        mock_client.devboxes.wait_for_command.return_value = completed_execution

        stop_event = threading.Event()
        thread = threading.Thread(target=lambda: time.sleep(SHORT_SLEEP))
        thread.start()
        streaming_group = _StreamingGroup([thread], stop_event)

        execution = Execution(mock_client, "dev_123", running_execution, streaming_group)  # type: ignore[arg-type]
        result = execution.result()

        assert result.exit_code == 0
        assert execution._streaming_group is None  # Should be cleaned up
        mock_client.devboxes.wait_for_command.assert_called_once()

    def test_result_passes_options(self, mock_client: Mock) -> None:
        """Ensure options are forwarded to wait_for_command."""
        execution_view = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="output",
            stderr="",
        )

        mock_client.devboxes = Mock()
        mock_client.devboxes.wait_for_command.return_value = execution_view

        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        execution.result(timeout=30.0, idempotency_key="abc123")

        mock_client.devboxes.wait_for_command.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
            statuses=["completed"],
            timeout=30.0,
            idempotency_key="abc123",
        )

    def test_get_state(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test get_state method."""
        updated_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )
        mock_client.devboxes.executions = Mock()
        mock_client.devboxes.executions.retrieve.return_value = updated_execution

        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        result = execution.get_state()

        assert result == updated_execution
        assert execution._initial_result == execution_view
        mock_client.devboxes.executions.retrieve.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
        )

    def test_kill(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test kill method."""
        mock_client.devboxes.executions.kill.return_value = None

        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        execution.kill()

        mock_client.devboxes.executions.kill.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
        )
