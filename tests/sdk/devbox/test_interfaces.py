"""Tests for Devbox interface classes.

Tests the command, file, and network interface helper classes that provide
structured access to devbox operations.
"""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock

import httpx

from tests.sdk.conftest import MockExecutionView
from runloop_api_client.sdk import Devbox


class TestCommandInterface:
    """Tests for _CommandInterface."""

    def test_exec_without_callbacks(self, mock_client: Mock, execution_view: MockExecutionView) -> None:
        """Test exec without streaming callbacks."""
        mock_client.devboxes.execute_async.return_value = execution_view
        mock_client.devboxes.executions.await_completed.return_value = execution_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.cmd.exec(command="echo hello")

        assert result.exit_code == 0
        assert result.stdout(num_lines=10) == "output"
        call_kwargs = mock_client.devboxes.execute_async.call_args[1]
        assert call_kwargs["command"] == "echo hello"
        assert "polling_config" not in call_kwargs
        assert "timeout" not in call_kwargs
        mock_client.devboxes.executions.await_completed.assert_not_called()

    def test_exec_with_stdout_callback(self, mock_client: Mock, mock_stream: Mock) -> None:
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

        mock_client.devboxes.execute_async.return_value = execution_async
        mock_client.devboxes.executions.await_completed.return_value = execution_completed
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream

        stdout_calls: list[str] = []

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.cmd.exec(command="echo hello", stdout=stdout_calls.append)

        assert result.exit_code == 0
        mock_client.devboxes.execute_async.assert_called_once()
        mock_client.devboxes.executions.await_completed.assert_called_once()

    def test_exec_with_stderr_callback(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test exec with stderr callback."""
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
            stdout="",
            stderr="error",
        )

        mock_client.devboxes.execute_async.return_value = execution_async
        mock_client.devboxes.executions.await_completed.return_value = execution_completed
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        stderr_calls: list[str] = []

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.cmd.exec(command="echo hello", stderr=stderr_calls.append)

        assert result.exit_code == 0
        mock_client.devboxes.execute_async.assert_called_once()

    def test_exec_with_output_callback(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test exec with output callback."""
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

        mock_client.devboxes.execute_async.return_value = execution_async
        mock_client.devboxes.executions.await_completed.return_value = execution_completed
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        output_calls: list[str] = []

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.cmd.exec(command="echo hello", output=output_calls.append)

        assert result.exit_code == 0
        mock_client.devboxes.execute_async.assert_called_once()

    def test_exec_with_all_callbacks(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test exec with all callbacks."""
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
            stderr="error",
        )

        mock_client.devboxes.execute_async.return_value = execution_async
        mock_client.devboxes.executions.await_completed.return_value = execution_completed
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        stdout_calls: list[str] = []
        stderr_calls: list[str] = []
        output_calls: list[str] = []

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.cmd.exec(
            command="echo hello",
            stdout=stdout_calls.append,
            stderr=stderr_calls.append,
            output=output_calls.append,
        )

        assert result.exit_code == 0
        mock_client.devboxes.execute_async.assert_called_once()

    def test_exec_async_returns_execution(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test exec_async returns Execution object."""
        execution_async = SimpleNamespace(
            execution_id="exec_123",
            devbox_id="dev_123",
            status="running",
        )

        mock_client.devboxes.execute_async.return_value = execution_async
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        execution = devbox.cmd.exec_async(command="long-running command")

        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"
        mock_client.devboxes.execute_async.assert_called_once()


class TestFileInterface:
    """Tests for _FileInterface."""

    def test_read(self, mock_client: Mock) -> None:
        """Test file read."""
        mock_client.devboxes.read_file_contents.return_value = "file content"

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.read(file_path="/path/to/file")

        assert result == "file content"
        call_kwargs = mock_client.devboxes.read_file_contents.call_args[1]
        assert call_kwargs["file_path"] == "/path/to/file"
        assert "timeout" not in call_kwargs

    def test_write_string(self, mock_client: Mock) -> None:
        """Test file write with string."""
        execution_detail = SimpleNamespace()
        mock_client.devboxes.write_file_contents.return_value = execution_detail

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.write(file_path="/path/to/file", contents="content")

        assert result == execution_detail
        call_kwargs = mock_client.devboxes.write_file_contents.call_args[1]
        assert call_kwargs["file_path"] == "/path/to/file"
        assert call_kwargs["contents"] == "content"
        assert "timeout" not in call_kwargs

    def test_write_bytes(self, mock_client: Mock) -> None:
        """Test file write with bytes."""
        execution_detail = SimpleNamespace()
        mock_client.devboxes.write_file_contents.return_value = execution_detail

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.write(file_path="/path/to/file", contents="content")

        assert result == execution_detail
        call_kwargs = mock_client.devboxes.write_file_contents.call_args[1]
        assert call_kwargs["file_path"] == "/path/to/file"
        assert call_kwargs["contents"] == "content"
        assert "timeout" not in call_kwargs

    def test_download(self, mock_client: Mock) -> None:
        """Test file download."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.read.return_value = b"file content"
        mock_client.devboxes.download_file.return_value = mock_response

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.download(path="/path/to/file")

        assert result == b"file content"
        call_kwargs = mock_client.devboxes.download_file.call_args[1]
        assert call_kwargs["path"] == "/path/to/file"
        assert "timeout" not in call_kwargs

    def test_upload(self, mock_client: Mock, tmp_path: Path) -> None:
        """Test file upload."""
        execution_detail = SimpleNamespace()
        mock_client.devboxes.upload_file.return_value = execution_detail

        devbox = Devbox(mock_client, "dev_123")
        # Create a temporary file for upload
        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test content")

        result = devbox.file.upload(path="/remote/path", file=temp_file)

        assert result == execution_detail
        call_kwargs = mock_client.devboxes.upload_file.call_args[1]
        assert call_kwargs["path"] == "/remote/path"
        assert call_kwargs["file"] is not None  # File object from temp_path
        assert "timeout" not in call_kwargs


class TestNetworkInterface:
    """Tests for _NetworkInterface."""

    def test_create_ssh_key(self, mock_client: Mock) -> None:
        """Test create SSH key."""
        ssh_key_response = SimpleNamespace(public_key="ssh-rsa ...")
        mock_client.devboxes.create_ssh_key.return_value = ssh_key_response

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.net.create_ssh_key(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == ssh_key_response
        mock_client.devboxes.create_ssh_key.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_create_tunnel(self, mock_client: Mock) -> None:
        """Test create tunnel."""
        tunnel_view = SimpleNamespace(port=8080)
        mock_client.devboxes.create_tunnel.return_value = tunnel_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.net.create_tunnel(
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == tunnel_view
        mock_client.devboxes.create_tunnel.assert_called_once_with(
            "dev_123",
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_remove_tunnel(self, mock_client: Mock) -> None:
        """Test remove tunnel."""
        mock_client.devboxes.remove_tunnel.return_value = object()

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.net.remove_tunnel(
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None  # Verify return value is propagated
        mock_client.devboxes.remove_tunnel.assert_called_once_with(
            "dev_123",
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )
