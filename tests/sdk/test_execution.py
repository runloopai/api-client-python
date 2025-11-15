"""Comprehensive tests for Execution class."""

from __future__ import annotations

import time
import threading
from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import (
    TASK_COMPLETION_LONG,
    THREAD_STARTUP_DELAY,
    TASK_COMPLETION_SHORT,
    MockExecutionView,
)
from runloop_api_client.sdk.execution import Execution, _StreamingGroup

# Legacy aliases for backward compatibility during transition
SHORT_SLEEP = THREAD_STARTUP_DELAY
MEDIUM_SLEEP = TASK_COMPLETION_SHORT * 10  # 0.2
LONG_SLEEP = TASK_COMPLETION_LONG


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
        assert execution._latest == execution_view

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

    def test_result_already_completed(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test result when execution is already completed."""
        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        result = execution.result()

        assert result.exit_code == 0
        assert result.stdout() == "output"
        # Verify await_completed is not called when already completed
        if hasattr(mock_client.devboxes.executions, "await_completed"):
            assert not mock_client.devboxes.executions.await_completed.called

    def test_result_needs_polling(self, mock_client: Mock) -> None:
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
        )

        mock_client.devboxes.executions.await_completed.return_value = completed_execution

        execution = Execution(mock_client, "dev_123", running_execution)  # type: ignore[arg-type]
        result = execution.result()

        assert result.exit_code == 0
        assert result.stdout() == "output"
        mock_client.devboxes.executions.await_completed.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
            polling_config=None,
        )

    def test_result_with_streaming_group(self, mock_client: Mock) -> None:
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

        mock_client.devboxes.executions.await_completed.return_value = completed_execution

        stop_event = threading.Event()
        thread = threading.Thread(target=lambda: time.sleep(SHORT_SLEEP))
        thread.start()
        streaming_group = _StreamingGroup([thread], stop_event)

        execution = Execution(mock_client, "dev_123", running_execution, streaming_group)  # type: ignore[arg-type]
        result = execution.result()

        assert result.exit_code == 0
        assert execution._streaming_group is None  # Should be cleaned up

    def test_get_state(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test get_state method."""
        updated_execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )
        mock_client.devboxes.executions.retrieve.return_value = updated_execution

        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        result = execution.get_state()

        assert result == updated_execution
        assert execution._latest == updated_execution
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
            kill_process_group=None,
        )

    def test_kill_with_process_group(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test kill with kill_process_group."""
        mock_client.devboxes.executions.kill.return_value = None

        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        execution.kill(kill_process_group=True)

        mock_client.devboxes.executions.kill.assert_called_once_with(
            "exec_123",
            devbox_id="dev_123",
            kill_process_group=True,
        )

    def test_kill_with_streaming_cleanup(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test kill cleans up streaming."""
        mock_client.devboxes.executions.kill.return_value = None

        stop_event = threading.Event()
        # Thread needs to be started to be joinable
        thread = threading.Thread(target=lambda: time.sleep(LONG_SLEEP))
        thread.start()
        streaming_group = _StreamingGroup([thread], stop_event)

        execution = Execution(mock_client, "dev_123", execution_view, streaming_group)  # type: ignore[arg-type]
        execution.kill()

        assert execution._streaming_group is None  # Should be cleaned up
        assert stop_event.is_set()  # Should be stopped

    def test_stop_streaming_no_group(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test _stop_streaming when no streaming group."""
        execution = Execution(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        execution._stop_streaming()  # Should not raise

    def test_stop_streaming_with_group(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test _stop_streaming with streaming group."""
        stop_event = threading.Event()
        # Thread needs to be started to be joinable
        thread = threading.Thread(target=lambda: time.sleep(LONG_SLEEP))
        thread.start()
        streaming_group = _StreamingGroup([thread], stop_event)

        execution = Execution(mock_client, "dev_123", execution_view, streaming_group)  # type: ignore[arg-type]
        execution._stop_streaming()

        assert execution._streaming_group is None
        assert stop_event.is_set()
