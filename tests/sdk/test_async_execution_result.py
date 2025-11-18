"""Comprehensive tests for AsyncExecutionResult class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock

import pytest

from tests.sdk.conftest import MockExecutionView
from runloop_api_client.sdk.async_execution_result import AsyncExecutionResult


class TestAsyncExecutionResult:
    """Tests for AsyncExecutionResult class."""

    def test_init(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test AsyncExecutionResult initialization."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        # Verify via public API
        assert result.devbox_id == "dev_123"
        assert result.execution_id == "exec_123"

    def test_devbox_id_property(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test devbox_id property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.devbox_id == "dev_123"

    def test_execution_id_property(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test execution_id property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.execution_id == "exec_123"

    def test_exit_code_property(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test exit_code property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.exit_code == 0

    def test_exit_code_none(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.exit_code is None

    def test_success_property(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test success property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.success is True

    def test_success_false(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.success is False

    def test_failed_property(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test failed property when exit code is zero."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.failed is False

    def test_failed_true(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.failed is True

    def test_failed_none(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]
        assert result.failed is False

    @pytest.mark.asyncio
    async def test_stdout(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test stdout method."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert await result.stdout() == "output"
        assert await result.stdout(num_lines=10) == "output"

    @pytest.mark.asyncio
    async def test_stdout_empty(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]
        assert await result.stdout() == ""

    @pytest.mark.asyncio
    async def test_stderr(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]
        assert await result.stderr() == "error message"
        assert await result.stderr(num_lines=20) == "error message"

    @pytest.mark.asyncio
    async def test_stderr_empty(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test stderr method when stderr is None."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert await result.stderr() == ""

    def test_result_property(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test result property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]
        assert result.result == execution_view

    @pytest.mark.asyncio
    async def test_stdout_with_truncation_and_streaming(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test stdout streams full output when truncated."""
        from types import SimpleNamespace as SN

        # Mock chunk data
        async def mock_iter():
            yield SN(output="line1\n")
            yield SN(output="line2\n")
            yield SN(output="line3\n")

        mock_async_stream.__aiter__ = Mock(return_value=mock_iter())

        # Setup client mock to return our stream
        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)

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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should stream full output
        output = await result.stdout()
        assert output == "line1\nline2\nline3\n"
        mock_async_client.devboxes.executions.stream_stdout_updates.assert_called_once_with(
            "exec_123", devbox_id="dev_123"
        )

    @pytest.mark.asyncio
    async def test_stderr_with_truncation_and_streaming(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test stderr streams full output when truncated."""
        from types import SimpleNamespace as SN

        # Mock chunk data
        async def mock_iter():
            yield SN(output="error1\n")
            yield SN(output="error2\n")

        mock_async_stream.__aiter__ = Mock(return_value=mock_iter())

        # Setup client mock to return our stream
        mock_async_client.devboxes.executions.stream_stderr_updates = AsyncMock(return_value=mock_async_stream)

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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should stream full output
        output = await result.stderr()
        assert output == "error1\nerror2\n"
        mock_async_client.devboxes.executions.stream_stderr_updates.assert_called_once_with(
            "exec_123", devbox_id="dev_123"
        )

    @pytest.mark.asyncio
    async def test_stdout_with_num_lines_when_truncated(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test stdout with num_lines parameter when truncated."""
        from types import SimpleNamespace as SN

        # Mock chunk data with many lines
        async def mock_iter():
            yield SN(output="line1\nline2\nline3\n")
            yield SN(output="line4\nline5\n")

        mock_async_stream.__aiter__ = Mock(return_value=mock_iter())

        # Setup client mock to return our stream
        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)

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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should stream and return last 2 lines
        output = await result.stdout(num_lines=2)
        assert output == "line4\nline5"

    @pytest.mark.asyncio
    async def test_stdout_no_streaming_when_not_truncated(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should return existing output without streaming
        output = await result.stdout()
        assert output == "complete output"

    @pytest.mark.asyncio
    async def test_stdout_with_num_lines_no_truncation(self, mock_async_client: AsyncMock) -> None:
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
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)  # type: ignore[arg-type]

        # Should return last 2 lines without streaming
        output = await result.stdout(num_lines=2)
        assert output == "line4\nline5"

    def test_count_non_empty_lines(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test the _count_non_empty_lines helper method."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]

        # Test various input strings
        assert result._count_non_empty_lines("") == 0
        assert result._count_non_empty_lines("single") == 1
        assert result._count_non_empty_lines("line1\nline2") == 2
        assert result._count_non_empty_lines("line1\nline2\n") == 2
        assert result._count_non_empty_lines("line1\n\nline3") == 2  # Empty line in middle
        assert result._count_non_empty_lines("line1\nline2\nline3\n\n") == 3  # Trailing newlines

    def test_get_last_n_lines(self, mock_async_client: AsyncMock, execution_view: MockExecutionView) -> None:
        """Test the _get_last_n_lines helper method."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)  # type: ignore[arg-type]

        # Test various scenarios
        assert result._get_last_n_lines("", 5) == ""
        assert result._get_last_n_lines("single", 1) == "single"
        assert result._get_last_n_lines("line1\nline2\nline3", 2) == "line2\nline3"
        assert result._get_last_n_lines("line1\nline2\nline3\n", 2) == "line2\nline3"
        assert result._get_last_n_lines("line1\nline2", 10) == "line1\nline2"  # Request more than available
        assert result._get_last_n_lines("line1\nline2", 0) == ""  # Zero lines
