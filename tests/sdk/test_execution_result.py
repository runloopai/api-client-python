"""Comprehensive tests for ExecutionResult class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import MockExecutionView
from runloop_api_client.sdk.execution_result import ExecutionResult


class TestExecutionResult:
    """Tests for ExecutionResult class."""

    def test_init(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test ExecutionResult initialization."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        # Verify via public API
        assert result.devbox_id == "dev_123"
        assert result.execution_id == "exec_123"

    def test_devbox_id_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test devbox_id property."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.devbox_id == "dev_123"

    def test_execution_id_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test execution_id property."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.execution_id == "exec_123"

    def test_exit_code_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test exit_code property."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.exit_code == 0

    def test_exit_code_none(self, mock_client: Mock) -> None:
        """Test exit_code property when exit_status is None."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
            exit_status=None,
            stdout="",
            stderr="",
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.exit_code is None

    def test_success_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test success property."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.success is True

    def test_success_false(self, mock_client: Mock) -> None:
        """Test success property when exit code is non-zero."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=1,
            stdout="",
            stderr="error",
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.success is False

    def test_failed_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test failed property when exit code is zero."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.failed is False

    def test_failed_true(self, mock_client: Mock) -> None:
        """Test failed property when exit code is non-zero."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=1,
            stdout="",
            stderr="error",
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.failed is True

    def test_failed_none(self, mock_client: Mock) -> None:
        """Test failed property when exit_status is None."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
            exit_status=None,
            stdout="",
            stderr="",
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.failed is False

    def test_stdout(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test stdout method."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.stdout() == "output"
        assert result.stdout(num_lines=10) == "output"

    def test_stdout_empty(self, mock_client: Mock) -> None:
        """Test stdout method when stdout is None."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout=None,
            stderr="",
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.stdout() == ""

    def test_stderr(self, mock_client: Mock) -> None:
        """Test stderr method."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=1,
            stdout="",
            stderr="error message",
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.stderr() == "error message"
        assert result.stderr(num_lines=20) == "error message"

    def test_stderr_empty(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test stderr method when stderr is None."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.stderr() == ""

    def test_raw_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test raw property."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.raw == execution_view
