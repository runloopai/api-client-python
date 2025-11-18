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
            stdout_truncated=False,
            stderr_truncated=False,
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
            stdout_truncated=False,
            stderr_truncated=False,
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
            stdout_truncated=False,
            stderr_truncated=False,
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
            stdout_truncated=False,
            stderr_truncated=False,
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
            stdout_truncated=False,
            stderr_truncated=False,
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
            stdout_truncated=False,
            stderr_truncated=False,
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.stderr() == "error message"
        assert result.stderr(num_lines=20) == "error message"

    def test_stderr_empty(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test stderr method when stderr is None."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.stderr() == ""

    def test_result_property(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test result property."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.result == execution_view

    def test_stdout_with_truncation_and_streaming(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test stdout streams full output when truncated."""
        from types import SimpleNamespace as SN

        # Mock chunk data
        chunk1 = SN(output="line1\n")
        chunk2 = SN(output="line2\n")
        chunk3 = SN(output="line3\n")
        mock_stream.__iter__ = Mock(return_value=iter([chunk1, chunk2, chunk3]))

        # Setup client mock to return our stream
        mock_client.devboxes.executions.stream_stdout_updates = Mock(return_value=mock_stream)

        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="partial",
            stderr="",
            stdout_truncated=True,
            stderr_truncated=False,
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should stream full output
        output = result.stdout()
        assert output == "line1\nline2\nline3\n"
        mock_client.devboxes.executions.stream_stdout_updates.assert_called_once_with("exec_123", devbox_id="dev_123")

    def test_stderr_with_truncation_and_streaming(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test stderr streams full output when truncated."""
        from types import SimpleNamespace as SN

        # Mock chunk data
        chunk1 = SN(output="error1\n")
        chunk2 = SN(output="error2\n")
        mock_stream.__iter__ = Mock(return_value=iter([chunk1, chunk2]))

        # Setup client mock to return our stream
        mock_client.devboxes.executions.stream_stderr_updates = Mock(return_value=mock_stream)

        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="",
            stderr="partial error",
            stdout_truncated=False,
            stderr_truncated=True,
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should stream full output
        output = result.stderr()
        assert output == "error1\nerror2\n"
        mock_client.devboxes.executions.stream_stderr_updates.assert_called_once_with("exec_123", devbox_id="dev_123")

    def test_stdout_with_num_lines_when_truncated(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test stdout with num_lines parameter when truncated."""
        from types import SimpleNamespace as SN

        # Mock chunk data with many lines
        chunk1 = SN(output="line1\nline2\nline3\n")
        chunk2 = SN(output="line4\nline5\n")
        mock_stream.__iter__ = Mock(return_value=iter([chunk1, chunk2]))

        # Setup client mock to return our stream
        mock_client.devboxes.executions.stream_stdout_updates = Mock(return_value=mock_stream)

        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="line1\n",
            stderr="",
            stdout_truncated=True,
            stderr_truncated=False,
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should stream and return last 2 lines
        output = result.stdout(num_lines=2)
        assert output == "line4\nline5"

    def test_stdout_no_streaming_when_not_truncated(self, mock_client: Mock) -> None:
        """Test stdout doesn't stream when not truncated."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="complete output",
            stderr="",
            stdout_truncated=False,
            stderr_truncated=False,
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should return existing output without streaming
        output = result.stdout()
        assert output == "complete output"

    def test_stdout_with_num_lines_no_truncation(self, mock_client: Mock) -> None:
        """Test stdout with num_lines when not truncated."""
        execution = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="line1\nline2\nline3\nline4\nline5",
            stderr="",
            stdout_truncated=False,
            stderr_truncated=False,
        )
        result = ExecutionResult(mock_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should return last 2 lines without streaming
        output = result.stdout(num_lines=2)
        assert output == "line4\nline5"

    def test_count_non_empty_lines(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test the _count_non_empty_lines helper method."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]

        # Test various input strings
        assert result._count_non_empty_lines("") == 0
        assert result._count_non_empty_lines("single") == 1
        assert result._count_non_empty_lines("line1\nline2") == 2
        assert result._count_non_empty_lines("line1\nline2\n") == 2
        assert result._count_non_empty_lines("line1\n\nline3") == 2  # Empty line in middle
        assert result._count_non_empty_lines("line1\nline2\nline3\n\n") == 3  # Trailing newlines

    def test_get_last_n_lines(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test the _get_last_n_lines helper method."""
        result = ExecutionResult(mock_client, "dev_123", execution_view)  # type: ignore[arg-type]

        # Test various scenarios
        assert result._get_last_n_lines("", 5) == ""
        assert result._get_last_n_lines("single", 1) == "single"
        assert result._get_last_n_lines("line1\nline2\nline3", 2) == "line2\nline3"
        assert result._get_last_n_lines("line1\nline2\nline3\n", 2) == "line2\nline3"
        assert result._get_last_n_lines("line1\nline2", 10) == "line1\nline2"  # Request more than available
        assert result._get_last_n_lines("line1\nline2", 0) == ""  # Zero lines
