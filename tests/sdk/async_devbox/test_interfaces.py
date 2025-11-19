"""Tests for AsyncDevbox interface classes.

Tests the async command, file, and network interface helper classes.
"""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import AsyncMock

import httpx
import pytest

from tests.sdk.conftest import MockExecutionView
from runloop_api_client.sdk import AsyncDevbox


class TestAsyncCommandInterface:
    """Tests for _AsyncCommandInterface."""

    @pytest.mark.asyncio
    async def test_exec_without_callbacks(
        self, mock_async_client: AsyncMock, execution_view: MockExecutionView
    ) -> None:
        """Test exec without streaming callbacks."""
        mock_async_client.devboxes.execute_async = AsyncMock(return_value=execution_view)
        mock_async_client.devboxes.executions.await_completed = AsyncMock(return_value=execution_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.cmd.exec(command="echo hello")

        assert result.exit_code == 0
        assert await result.stdout(num_lines=10) == "output"
        call_kwargs = mock_async_client.devboxes.execute_async.call_args[1]
        assert call_kwargs["command"] == "echo hello"
        assert "polling_config" not in call_kwargs
        assert "timeout" not in call_kwargs
        mock_async_client.devboxes.executions.await_completed.assert_not_called()

    @pytest.mark.asyncio
    async def test_exec_with_stdout_callback(self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock) -> None:
        """Test exec with stdout callback."""
        execution_async = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )
        execution_completed = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="completed",
            exit_status=0,
            stdout="output",
            stderr="",
        )

        mock_async_client.devboxes.execute_async = AsyncMock(return_value=execution_async)
        mock_async_client.devboxes.executions.await_completed = AsyncMock(return_value=execution_completed)
        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)

        stdout_calls: list[str] = []

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.cmd.exec(command="echo hello", stdout=stdout_calls.append)

        assert result.exit_code == 0
        mock_async_client.devboxes.execute_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_exec_async_returns_execution(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test exec_async returns AsyncExecution object."""
        execution_async = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )

        mock_async_client.devboxes.execute_async = AsyncMock(return_value=execution_async)
        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        execution = await devbox.cmd.exec_async(command="long-running command")

        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"
        mock_async_client.devboxes.execute_async.assert_called_once()


class TestAsyncFileInterface:
    """Tests for _AsyncFileInterface."""

    @pytest.mark.asyncio
    async def test_read(self, mock_async_client: AsyncMock) -> None:
        """Test file read."""
        mock_async_client.devboxes.read_file_contents = AsyncMock(return_value="file content")

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.read(file_path="/path/to/file")

        assert result == "file content"
        mock_async_client.devboxes.read_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_string(self, mock_async_client: AsyncMock) -> None:
        """Test file write with string."""
        execution_detail = SimpleNamespace()
        mock_async_client.devboxes.write_file_contents = AsyncMock(return_value=execution_detail)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.write(file_path="/path/to/file", contents="content")

        assert result == execution_detail
        mock_async_client.devboxes.write_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_bytes(self, mock_async_client: AsyncMock) -> None:
        """Test file write with bytes."""
        execution_detail = SimpleNamespace()
        mock_async_client.devboxes.write_file_contents = AsyncMock(return_value=execution_detail)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.write(file_path="/path/to/file", contents="content")

        assert result == execution_detail
        mock_async_client.devboxes.write_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_download(self, mock_async_client: AsyncMock) -> None:
        """Test file download."""
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.read = AsyncMock(return_value=b"file content")
        mock_async_client.devboxes.download_file = AsyncMock(return_value=mock_response)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.download(path="/path/to/file")

        assert result == b"file content"
        mock_async_client.devboxes.download_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload(self, mock_async_client: AsyncMock, tmp_path: Path) -> None:
        """Test file upload."""
        execution_detail = SimpleNamespace()
        mock_async_client.devboxes.upload_file = AsyncMock(return_value=execution_detail)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        # Create a temporary file for upload
        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test content")

        result = await devbox.file.upload(path="/remote/path", file=temp_file)

        assert result == execution_detail
        mock_async_client.devboxes.upload_file.assert_called_once()


class TestAsyncNetworkInterface:
    """Tests for _AsyncNetworkInterface."""

    @pytest.mark.asyncio
    async def test_create_ssh_key(self, mock_async_client: AsyncMock) -> None:
        """Test create SSH key."""
        ssh_key_response = SimpleNamespace(public_key="ssh-rsa ...")
        mock_async_client.devboxes.create_ssh_key = AsyncMock(return_value=ssh_key_response)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.net.create_ssh_key(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == ssh_key_response
        mock_async_client.devboxes.create_ssh_key.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_tunnel(self, mock_async_client: AsyncMock) -> None:
        """Test create tunnel."""
        tunnel_view = SimpleNamespace(tunnel_id="tunnel_123")
        mock_async_client.devboxes.create_tunnel = AsyncMock(return_value=tunnel_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.net.create_tunnel(
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == tunnel_view
        mock_async_client.devboxes.create_tunnel.assert_called_once()

    @pytest.mark.asyncio
    async def test_remove_tunnel(self, mock_async_client: AsyncMock) -> None:
        """Test remove tunnel."""
        mock_async_client.devboxes.remove_tunnel = AsyncMock(return_value=object())

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.net.remove_tunnel(
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None  # Verify return value is propagated
        mock_async_client.devboxes.remove_tunnel.assert_called_once()
