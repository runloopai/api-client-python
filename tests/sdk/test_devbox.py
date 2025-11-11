"""Comprehensive tests for sync Devbox class."""

from __future__ import annotations

import time
import tempfile
import threading
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

import httpx
import pytest

from tests.sdk.conftest import create_mock_httpx_response
from runloop_api_client.sdk import Devbox, StorageObject
from runloop_api_client._types import NotGiven, omit
from runloop_api_client._streaming import Stream
from runloop_api_client.sdk.devbox import (
    _FileInterface,
    _CommandInterface,
    _NetworkInterface,
)
from runloop_api_client._exceptions import APIStatusError
from runloop_api_client.lib.polling import PollingConfig
from runloop_api_client.sdk.execution import _StreamingGroup

# Test constants
SHORT_SLEEP = 0.1  # Brief pause for thread operations
NUM_CONCURRENT_THREADS = 5  # Number of threads for concurrent operation tests


class TestDevbox:
    """Tests for Devbox class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Devbox initialization."""
        devbox = Devbox(mock_client, "dev_123")
        assert devbox.id == "dev_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Devbox string representation."""
        devbox = Devbox(mock_client, "dev_123")
        assert repr(devbox) == "<Devbox id='dev_123'>"

    def test_context_manager_enter_exit(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test context manager behavior with successful shutdown."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        with Devbox(mock_client, "dev_123") as devbox:
            assert devbox.id == "dev_123"

        call_kwargs = mock_client.devboxes.shutdown.call_args[1]
        assert isinstance(call_kwargs["timeout"], NotGiven)

    def test_context_manager_exception_handling(self, mock_client: Mock) -> None:
        """Test context manager handles exceptions during shutdown."""
        mock_client.devboxes.shutdown.side_effect = RuntimeError("Shutdown failed")

        with pytest.raises(ValueError, match="Test error"):
            with Devbox(mock_client, "dev_123") as devbox:
                raise ValueError("Test error")

        # Shutdown should be called even when body raises exception
        mock_client.devboxes.shutdown.assert_called_once()

    def test_get_info(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test get_info method."""
        mock_client.devboxes.retrieve.return_value = devbox_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == devbox_view
        mock_client.devboxes.retrieve.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_await_running(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test await_running method."""
        mock_client.devboxes.await_running.return_value = devbox_view
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.await_running(polling_config=polling_config)

        assert result == devbox_view
        mock_client.devboxes.await_running.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    def test_await_suspended(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test await_suspended method."""
        mock_client.devboxes.await_suspended.return_value = devbox_view
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.await_suspended(polling_config=polling_config)

        assert result == devbox_view
        mock_client.devboxes.await_suspended.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    def test_shutdown(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test shutdown method."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.shutdown(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == devbox_view
        mock_client.devboxes.shutdown.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_suspend(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test suspend method."""
        mock_client.devboxes.suspend.return_value = None
        mock_client.devboxes.await_suspended.return_value = devbox_view
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.suspend(
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == devbox_view
        mock_client.devboxes.suspend.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )
        mock_client.devboxes.await_suspended.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    def test_resume(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test resume method."""
        mock_client.devboxes.resume.return_value = None
        mock_client.devboxes.await_running.return_value = devbox_view
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.resume(
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == devbox_view
        mock_client.devboxes.resume.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )
        mock_client.devboxes.await_running.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    def test_keep_alive(self, mock_client: Mock) -> None:
        """Test keep_alive method."""
        # Return value not used - testing parameter passing only
        mock_client.devboxes.keep_alive.return_value = object()

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.keep_alive(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None
        mock_client.devboxes.keep_alive.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_snapshot_disk(self, mock_client: Mock) -> None:
        """Test snapshot_disk waits for completion."""
        snapshot_data = SimpleNamespace(id="snap_123")
        snapshot_status = SimpleNamespace(status="completed")

        mock_client.devboxes.snapshot_disk_async.return_value = snapshot_data
        mock_client.devboxes.disk_snapshots.await_completed.return_value = snapshot_status

        devbox = Devbox(mock_client, "dev_123")
        polling_config = PollingConfig(timeout_seconds=60.0)
        snapshot = devbox.snapshot_disk(
            name="test-snapshot",
            metadata={"key": "value"},
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
        )

        assert snapshot.id == "snap_123"
        call_kwargs = mock_client.devboxes.snapshot_disk_async.call_args[1]
        assert call_kwargs["commit_message"] is omit or call_kwargs["commit_message"] is None
        assert call_kwargs["metadata"] == {"key": "value"}
        assert call_kwargs["name"] == "test-snapshot"
        assert call_kwargs["extra_headers"] == {"X-Custom": "value"}
        assert isinstance(call_kwargs["timeout"], NotGiven)
        call_kwargs2 = mock_client.devboxes.disk_snapshots.await_completed.call_args[1]
        assert call_kwargs2["polling_config"] == polling_config
        assert isinstance(call_kwargs2["timeout"], NotGiven)

    def test_snapshot_disk_async(self, mock_client: Mock) -> None:
        """Test snapshot_disk_async returns immediately."""
        snapshot_data = SimpleNamespace(id="snap_123")
        mock_client.devboxes.snapshot_disk_async.return_value = snapshot_data

        devbox = Devbox(mock_client, "dev_123")
        snapshot = devbox.snapshot_disk_async(
            name="test-snapshot",
            metadata={"key": "value"},
            extra_headers={"X-Custom": "value"},
        )

        assert snapshot.id == "snap_123"
        call_kwargs = mock_client.devboxes.snapshot_disk_async.call_args[1]
        assert call_kwargs["commit_message"] is omit or call_kwargs["commit_message"] is None
        assert call_kwargs["metadata"] == {"key": "value"}
        assert call_kwargs["name"] == "test-snapshot"
        assert call_kwargs["extra_headers"] == {"X-Custom": "value"}
        assert isinstance(call_kwargs["timeout"], NotGiven)
        # Verify async method does not wait for completion
        if hasattr(mock_client.devboxes.disk_snapshots, "await_completed"):
            assert not mock_client.devboxes.disk_snapshots.await_completed.called

    def test_close(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test close method calls shutdown."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        devbox = Devbox(mock_client, "dev_123")
        devbox.close()

        call_kwargs = mock_client.devboxes.shutdown.call_args[1]
        assert isinstance(call_kwargs["timeout"], NotGiven)

    def test_cmd_property(self, mock_client: Mock) -> None:
        """Test cmd property returns CommandInterface."""
        devbox = Devbox(mock_client, "dev_123")
        cmd = devbox.cmd
        assert isinstance(cmd, _CommandInterface)
        assert cmd._devbox is devbox

    def test_file_property(self, mock_client: Mock) -> None:
        """Test file property returns FileInterface."""
        devbox = Devbox(mock_client, "dev_123")
        file_interface = devbox.file
        assert isinstance(file_interface, _FileInterface)
        assert file_interface._devbox is devbox

    def test_net_property(self, mock_client: Mock) -> None:
        """Test net property returns NetworkInterface."""
        devbox = Devbox(mock_client, "dev_123")
        net = devbox.net
        assert isinstance(net, _NetworkInterface)
        assert net._devbox is devbox


class TestCommandInterface:
    """Tests for _CommandInterface."""

    def test_exec_without_callbacks(self, mock_client: Mock, execution_view: SimpleNamespace) -> None:
        """Test exec without streaming callbacks."""
        mock_client.devboxes.execute_and_await_completion.return_value = execution_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.cmd.exec("echo hello")

        assert result.exit_code == 0
        assert result.stdout() == "output"
        call_kwargs = mock_client.devboxes.execute_and_await_completion.call_args[1]
        assert call_kwargs["command"] == "echo hello"
        assert isinstance(call_kwargs["shell_name"], NotGiven) or call_kwargs["shell_name"] is None
        assert call_kwargs["polling_config"] is None
        assert isinstance(call_kwargs["timeout"], NotGiven)

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
        result = devbox.cmd.exec("echo hello", stdout=stdout_calls.append)

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
        result = devbox.cmd.exec("echo hello", stderr=stderr_calls.append)

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
        result = devbox.cmd.exec("echo hello", output=output_calls.append)

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
            "echo hello",
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
        execution = devbox.cmd.exec_async("long-running command")

        assert execution.execution_id == "exec_123"
        assert execution.devbox_id == "dev_123"
        mock_client.devboxes.execute_async.assert_called_once()


class TestFileInterface:
    """Tests for _FileInterface."""

    def test_read(self, mock_client: Mock) -> None:
        """Test file read."""
        mock_client.devboxes.read_file_contents.return_value = "file content"

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.read("/path/to/file")

        assert result == "file content"
        call_kwargs = mock_client.devboxes.read_file_contents.call_args[1]
        assert call_kwargs["file_path"] == "/path/to/file"
        assert isinstance(call_kwargs["timeout"], NotGiven)

    def test_write_string(self, mock_client: Mock) -> None:
        """Test file write with string."""
        execution_detail = SimpleNamespace()
        mock_client.devboxes.write_file_contents.return_value = execution_detail

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.write("/path/to/file", "content")

        assert result == execution_detail
        call_kwargs = mock_client.devboxes.write_file_contents.call_args[1]
        assert call_kwargs["file_path"] == "/path/to/file"
        assert call_kwargs["contents"] == "content"
        assert isinstance(call_kwargs["timeout"], NotGiven)

    def test_write_bytes(self, mock_client: Mock) -> None:
        """Test file write with bytes."""
        execution_detail = SimpleNamespace()
        mock_client.devboxes.write_file_contents.return_value = execution_detail

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.write("/path/to/file", b"content")

        assert result == execution_detail
        call_kwargs = mock_client.devboxes.write_file_contents.call_args[1]
        assert call_kwargs["file_path"] == "/path/to/file"
        assert call_kwargs["contents"] == "content"
        assert isinstance(call_kwargs["timeout"], NotGiven)

    def test_download(self, mock_client: Mock) -> None:
        """Test file download."""
        mock_response = Mock()
        mock_response.read.return_value = b"file content"
        mock_client.devboxes.download_file.return_value = mock_response

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.file.download("/path/to/file")

        assert result == b"file content"
        call_kwargs = mock_client.devboxes.download_file.call_args[1]
        assert call_kwargs["path"] == "/path/to/file"
        assert isinstance(call_kwargs["timeout"], NotGiven)

    def test_upload(self, mock_client: Mock) -> None:
        """Test file upload."""
        execution_detail = SimpleNamespace()
        mock_client.devboxes.upload_file.return_value = execution_detail

        devbox = Devbox(mock_client, "dev_123")
        # Create a temporary file for upload
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            temp_path = Path(f.name)

        try:
            result = devbox.file.upload("/remote/path", temp_path)
        finally:
            temp_path.unlink()

        assert result == execution_detail
        call_kwargs = mock_client.devboxes.upload_file.call_args[1]
        assert call_kwargs["path"] == "/remote/path"
        assert call_kwargs["file"] is not None  # File object from temp_path
        assert isinstance(call_kwargs["timeout"], NotGiven)


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
        # Return value not used - testing parameter passing only
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

        assert result is not None
        mock_client.devboxes.remove_tunnel.assert_called_once_with(
            "dev_123",
            port=8080,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )


class TestDevboxStreaming:
    """Tests for Devbox streaming methods."""

    def test_start_streaming_no_callbacks(self, mock_client: Mock) -> None:
        """Test _start_streaming returns None when no callbacks."""
        devbox = Devbox(mock_client, "dev_123")
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=None)
        assert result is None

    def test_start_streaming_stdout_only(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with stdout callback only."""
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        stdout_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=stdout_calls.append, stderr=None, output=None)

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 1
        mock_client.devboxes.executions.stream_stdout_updates.assert_called_once()

    def test_start_streaming_stderr_only(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with stderr callback only."""
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        stderr_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=stderr_calls.append, output=None)

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 1
        mock_client.devboxes.executions.stream_stderr_updates.assert_called_once()

    def test_start_streaming_output_only(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with output callback only."""
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        output_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=output_calls.append)

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 2  # Both stdout and stderr streams

    def test_start_streaming_all_callbacks(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with all callbacks."""
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        stdout_calls: list[str] = []
        stderr_calls: list[str] = []
        output_calls: list[str] = []
        result = devbox._start_streaming(
            "exec_123",
            stdout=stdout_calls.append,
            stderr=stderr_calls.append,
            output=output_calls.append,
        )

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 2  # Both stdout and stderr streams

    def test_spawn_stream_thread(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _spawn_stream_thread creates and starts thread."""
        mock_stream.__iter__ = Mock(
            return_value=iter(
                [
                    SimpleNamespace(output="line 1"),
                    SimpleNamespace(output="line 2"),
                ]
            )
        )
        mock_stream.__enter__ = Mock(return_value=mock_stream)
        mock_stream.__exit__ = Mock(return_value=None)

        devbox = Devbox(mock_client, "dev_123")
        stop_event = threading.Event()
        calls: list[str] = []

        def stream_factory() -> Stream:
            return mock_stream

        thread = devbox._spawn_stream_thread(
            name="test",
            stream_factory=stream_factory,
            callbacks=[calls.append],
            stop_event=stop_event,
        )

        assert isinstance(thread, threading.Thread)
        # Give thread time to start
        time.sleep(SHORT_SLEEP)
        # Thread may have already finished if stream is short
        if thread.is_alive():
            stop_event.set()
            thread.join(timeout=1.0)
        assert not thread.is_alive()

    def test_spawn_stream_thread_stop_event(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _spawn_stream_thread respects stop event."""
        mock_stream.__iter__ = Mock(
            return_value=iter(
                [
                    SimpleNamespace(output="line 1"),
                    SimpleNamespace(output="line 2"),
                ]
            )
        )
        mock_stream.__enter__ = Mock(return_value=mock_stream)
        mock_stream.__exit__ = Mock(return_value=None)

        devbox = Devbox(mock_client, "dev_123")
        stop_event = threading.Event()
        calls: list[str] = []

        def stream_factory() -> Stream:
            return mock_stream

        thread = devbox._spawn_stream_thread(
            name="test",
            stream_factory=stream_factory,
            callbacks=[calls.append],
            stop_event=stop_event,
        )

        stop_event.set()
        thread.join(timeout=1.0)
        assert not thread.is_alive()


class TestDevboxErrorHandling:
    """Tests for Devbox error handling scenarios."""

    def test_network_error(self, mock_client: Mock) -> None:
        """Test handling of network errors."""
        mock_client.devboxes.retrieve.side_effect = httpx.NetworkError("Connection failed")

        devbox = Devbox(mock_client, "dev_123")
        with pytest.raises(httpx.NetworkError):
            devbox.get_info()

    @pytest.mark.parametrize(
        "status_code,message",
        [
            (404, "Not Found"),
            (500, "Internal Server Error"),
            (503, "Service Unavailable"),
        ],
    )
    def test_api_error(self, mock_client: Mock, status_code: int, message: str) -> None:
        """Test handling of API errors with various status codes."""
        response = create_mock_httpx_response(status_code=status_code, headers={}, text=message)
        error = APIStatusError(message=message, response=response, body=None)

        mock_client.devboxes.retrieve.side_effect = error

        devbox = Devbox(mock_client, "dev_123")
        with pytest.raises(APIStatusError):
            devbox.get_info()

    def test_timeout_error(self, mock_client: Mock) -> None:
        """Test handling of timeout errors."""
        mock_client.devboxes.retrieve.side_effect = httpx.TimeoutException("Request timed out")

        devbox = Devbox(mock_client, "dev_123")
        with pytest.raises(httpx.TimeoutException):
            devbox.get_info(timeout=1.0)


class TestDevboxEdgeCases:
    """Tests for Devbox edge cases."""

    def test_empty_responses(self, mock_client: Mock) -> None:
        """Test handling of empty responses."""
        empty_view = SimpleNamespace(id="dev_123", status="", name="")
        mock_client.devboxes.retrieve.return_value = empty_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.get_info()
        assert result == empty_view

    def test_none_values(self, mock_client: Mock) -> None:
        """Test handling of None values."""
        view_with_none = SimpleNamespace(id="dev_123", status=None, name=None)
        mock_client.devboxes.retrieve.return_value = view_with_none

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.get_info()
        assert result.status is None
        assert result.name is None

    def test_concurrent_operations(self, mock_client: Mock) -> None:
        """Test concurrent operations."""
        mock_client.devboxes.retrieve.return_value = SimpleNamespace(id="dev_123", status="running")

        devbox = Devbox(mock_client, "dev_123")
        results = []

        def get_info() -> None:
            results.append(devbox.get_info())

        threads = [threading.Thread(target=get_info) for _ in range(NUM_CONCURRENT_THREADS)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(results) == NUM_CONCURRENT_THREADS


class TestDevboxPythonSpecific:
    """Tests for Python-specific Devbox behavior."""

    def test_context_manager_vs_manual_cleanup(self, mock_client: Mock, devbox_view: SimpleNamespace) -> None:
        """Test context manager provides automatic cleanup."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        # Context manager approach (Pythonic)
        with Devbox(mock_client, "dev_123"):
            pass

        mock_client.devboxes.shutdown.assert_called_once()

        # Manual cleanup (TypeScript-like)
        devbox = Devbox(mock_client, "dev_123")
        devbox.shutdown()
        assert mock_client.devboxes.shutdown.call_count == 2

    def test_path_handling(self, mock_client: Mock) -> None:
        """Test Path handling (Python-specific)."""
        object_view = SimpleNamespace(id="obj_123", upload_url="https://upload.example.com")
        mock_client.objects.create.return_value = object_view

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test")
            temp_path = Path(f.name)

        try:
            with patch("httpx.put") as mock_put:
                mock_response = create_mock_httpx_response()
                mock_put.return_value = mock_response

                obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
                obj.upload_content(temp_path)  # Path object works

                mock_put.assert_called_once()
        finally:
            temp_path.unlink()
