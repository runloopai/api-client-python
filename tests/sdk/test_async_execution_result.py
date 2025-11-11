"""Comprehensive tests for AsyncExecutionResult class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from runloop_api_client.sdk.async_execution_result import AsyncExecutionResult


class TestAsyncExecutionResult:
    """Tests for AsyncExecutionResult class."""

    def test_init(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test AsyncExecutionResult initialization."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
        # Verify via public API
        assert result.devbox_id == "dev_123"
        assert result.execution_id == "exec_123"

    def test_devbox_id_property(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test devbox_id property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
        assert result.devbox_id == "dev_123"

    def test_execution_id_property(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test execution_id property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
        assert result.execution_id == "exec_123"

    def test_exit_code_property(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test exit_code property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
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
        )
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)
        assert result.exit_code is None

    def test_success_property(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test success property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
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
        )
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)
        assert result.success is False

    def test_failed_property(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test failed property when exit code is zero."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
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
        )
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)
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
        )
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)
        assert result.failed is False

    @pytest.mark.asyncio
    async def test_stdout(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test stdout method."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
        assert await result.stdout() == "output"

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
        )
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)
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
        )
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution)
        assert await result.stderr() == "error message"

    @pytest.mark.asyncio
    async def test_stderr_empty(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test stderr method when stderr is None."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
        assert await result.stderr() == ""

    def test_raw_property(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test raw property."""
        result = AsyncExecutionResult(mock_async_client, "dev_123", execution_view)
        assert result.raw == execution_view
