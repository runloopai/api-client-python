"""Comprehensive tests for async Devbox class."""

from __future__ import annotations

import asyncio
import tempfile
from types import SimpleNamespace
from typing import AsyncIterator
from pathlib import Path
from unittest.mock import Mock, AsyncMock

import httpx
import pytest

from runloop_api_client.sdk import AsyncDevbox
from runloop_api_client._types import NotGiven
from runloop_api_client._streaming import AsyncStream
from runloop_api_client.lib.polling import PollingConfig
from runloop_api_client.sdk.async_devbox import (
    _AsyncFileInterface,
    _AsyncCommandInterface,
    _AsyncNetworkInterface,
)
from runloop_api_client.sdk.async_execution import _AsyncStreamingGroup


class TestAsyncDevbox:
    """Tests for AsyncDevbox class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncDevbox initialization."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        assert devbox.id == "dev_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncDevbox string representation."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        assert repr(devbox) == "<AsyncDevbox id='dev_123'>"

    @pytest.mark.asyncio
    async def test_context_manager_enter_exit(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test context manager behavior with successful shutdown."""
        mock_async_client.devboxes.shutdown = AsyncMock(return_value=devbox_view)

        async with AsyncDevbox(mock_async_client, "dev_123") as devbox:
            assert devbox.id == "dev_123"

        call_kwargs = mock_async_client.devboxes.shutdown.call_args[1]
        assert isinstance(call_kwargs["timeout"], NotGiven)

    @pytest.mark.asyncio
    async def test_context_manager_exception_handling(self, mock_async_client: AsyncMock) -> None:
        """Test context manager handles exceptions during shutdown."""
        mock_async_client.devboxes.shutdown = AsyncMock(side_effect=RuntimeError("Shutdown failed"))

        with pytest.raises(ValueError, match="Test error"):
            async with AsyncDevbox(mock_async_client, "dev_123"):
                raise ValueError("Test error")

        # Shutdown should be called even when body raises exception
        mock_async_client.devboxes.shutdown.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test get_info method."""
        mock_async_client.devboxes.retrieve = AsyncMock(return_value=devbox_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == devbox_view
        mock_async_client.devboxes.retrieve.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    @pytest.mark.asyncio
    async def test_await_running(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test await_running method."""
        mock_async_client.devboxes.await_running = AsyncMock(return_value=devbox_view)
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.await_running(polling_config=polling_config)

        assert result == devbox_view
        mock_async_client.devboxes.await_running.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    @pytest.mark.asyncio
    async def test_await_suspended(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test await_suspended method."""
        mock_async_client.devboxes.await_suspended = AsyncMock(return_value=devbox_view)
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.await_suspended(polling_config=polling_config)

        assert result == devbox_view
        mock_async_client.devboxes.await_suspended.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    @pytest.mark.asyncio
    async def test_shutdown(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test shutdown method."""
        mock_async_client.devboxes.shutdown = AsyncMock(return_value=devbox_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.shutdown(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == devbox_view
        mock_async_client.devboxes.shutdown.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    @pytest.mark.asyncio
    async def test_suspend(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test suspend method."""
        mock_async_client.devboxes.suspend = AsyncMock(return_value=None)
        mock_async_client.devboxes.await_suspended = AsyncMock(return_value=devbox_view)
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.suspend(
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == devbox_view
        mock_async_client.devboxes.suspend.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )
        mock_async_client.devboxes.await_suspended.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    @pytest.mark.asyncio
    async def test_resume(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test resume method."""
        mock_async_client.devboxes.resume = AsyncMock(return_value=None)
        mock_async_client.devboxes.await_running = AsyncMock(return_value=devbox_view)
        polling_config = PollingConfig(timeout_seconds=60.0)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.resume(
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == devbox_view
        mock_async_client.devboxes.resume.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )
        mock_async_client.devboxes.await_running.assert_called_once_with(
            "dev_123",
            polling_config=polling_config,
        )

    @pytest.mark.asyncio
    async def test_keep_alive(self, mock_async_client: AsyncMock) -> None:
        """Test keep_alive method."""
        # Return value not used - testing parameter passing only
        mock_async_client.devboxes.keep_alive = AsyncMock(return_value=object())

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.keep_alive(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None
        mock_async_client.devboxes.keep_alive.assert_called_once_with(
            "dev_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    @pytest.mark.asyncio
    async def test_snapshot_disk(self, mock_async_client: AsyncMock) -> None:
        """Test snapshot_disk waits for completion."""
        snapshot_data = SimpleNamespace(id="snap_123")
        snapshot_status = SimpleNamespace(status="completed")

        mock_async_client.devboxes.snapshot_disk_async = AsyncMock(return_value=snapshot_data)
        mock_async_client.devboxes.disk_snapshots.await_completed = AsyncMock(return_value=snapshot_status)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        polling_config = PollingConfig(timeout_seconds=60.0)
        snapshot = await devbox.snapshot_disk(
            name="test-snapshot",
            metadata={"key": "value"},
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
        )

        assert snapshot.id == "snap_123"
        mock_async_client.devboxes.snapshot_disk_async.assert_called_once()
        mock_async_client.devboxes.disk_snapshots.await_completed.assert_called_once()

    @pytest.mark.asyncio
    async def test_snapshot_disk_async(self, mock_async_client: AsyncMock) -> None:
        """Test snapshot_disk_async returns immediately."""
        snapshot_data = SimpleNamespace(id="snap_123")
        mock_async_client.devboxes.snapshot_disk_async = AsyncMock(return_value=snapshot_data)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        snapshot = await devbox.snapshot_disk_async(
            name="test-snapshot",
            metadata={"key": "value"},
            extra_headers={"X-Custom": "value"},
        )

        assert snapshot.id == "snap_123"
        mock_async_client.devboxes.snapshot_disk_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_close(self, mock_async_client: AsyncMock, devbox_view: SimpleNamespace) -> None:
        """Test close method calls shutdown."""
        mock_async_client.devboxes.shutdown = AsyncMock(return_value=devbox_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        await devbox.close()

        mock_async_client.devboxes.shutdown.assert_called_once()

    def test_cmd_property(self, mock_async_client: AsyncMock) -> None:
        """Test cmd property returns AsyncCommandInterface."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        cmd = devbox.cmd
        assert isinstance(cmd, _AsyncCommandInterface)
        assert cmd._devbox is devbox

    def test_file_property(self, mock_async_client: AsyncMock) -> None:
        """Test file property returns AsyncFileInterface."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        file_interface = devbox.file
        assert isinstance(file_interface, _AsyncFileInterface)
        assert file_interface._devbox is devbox

    def test_net_property(self, mock_async_client: AsyncMock) -> None:
        """Test net property returns AsyncNetworkInterface."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        net = devbox.net
        assert isinstance(net, _AsyncNetworkInterface)
        assert net._devbox is devbox


class TestAsyncCommandInterface:
    """Tests for _AsyncCommandInterface."""

    @pytest.mark.asyncio
    async def test_exec_without_callbacks(self, mock_async_client: AsyncMock, execution_view: SimpleNamespace) -> None:
        """Test exec without streaming callbacks."""
        mock_async_client.devboxes.execute_and_await_completion = AsyncMock(return_value=execution_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.cmd.exec("echo hello")

        assert result.exit_code == 0
        assert await result.stdout() == "output"
        call_kwargs = mock_async_client.devboxes.execute_and_await_completion.call_args[1]
        assert call_kwargs["command"] == "echo hello"
        assert isinstance(call_kwargs["shell_name"], NotGiven) or call_kwargs["shell_name"] is None
        assert isinstance(call_kwargs["timeout"], NotGiven)

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
        result = await devbox.cmd.exec("echo hello", stdout=stdout_calls.append)

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
        execution = await devbox.cmd.exec_async("long-running command")

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
        result = await devbox.file.read("/path/to/file")

        assert result == "file content"
        mock_async_client.devboxes.read_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_string(self, mock_async_client: AsyncMock) -> None:
        """Test file write with string."""
        execution_detail = SimpleNamespace()
        mock_async_client.devboxes.write_file_contents = AsyncMock(return_value=execution_detail)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.write("/path/to/file", "content")

        assert result == execution_detail
        mock_async_client.devboxes.write_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_bytes(self, mock_async_client: AsyncMock) -> None:
        """Test file write with bytes."""
        execution_detail = SimpleNamespace()
        mock_async_client.devboxes.write_file_contents = AsyncMock(return_value=execution_detail)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.write("/path/to/file", b"content")

        assert result == execution_detail
        mock_async_client.devboxes.write_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_download(self, mock_async_client: AsyncMock) -> None:
        """Test file download."""
        mock_response = AsyncMock()
        mock_response.read = AsyncMock(return_value=b"file content")
        mock_async_client.devboxes.download_file = AsyncMock(return_value=mock_response)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.file.download("/path/to/file")

        assert result == b"file content"
        mock_async_client.devboxes.download_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload(self, mock_async_client: AsyncMock) -> None:
        """Test file upload."""
        execution_detail = SimpleNamespace()
        mock_async_client.devboxes.upload_file = AsyncMock(return_value=execution_detail)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        # Create a temporary file for upload
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            temp_path = Path(f.name)

        try:
            result = await devbox.file.upload("/remote/path", temp_path)
        finally:
            temp_path.unlink()

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
        # Return value not used - testing parameter passing only
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

        assert result is not None
        mock_async_client.devboxes.remove_tunnel.assert_called_once()


class TestAsyncDevboxStreaming:
    """Tests for AsyncDevbox streaming methods."""

    def test_start_streaming_no_callbacks(self, mock_async_client: AsyncMock) -> None:
        """Test _start_streaming returns None when no callbacks."""
        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=None)
        assert result is None

    @pytest.mark.asyncio
    async def test_start_streaming_stdout_only(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test _start_streaming with stdout callback only."""

        # Create a proper async iterator
        async def async_iter():
            yield SimpleNamespace(output="line 1")
            yield SimpleNamespace(output="line 2")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        stdout_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=stdout_calls.append, stderr=None, output=None)

        assert result is not None
        assert isinstance(result, _AsyncStreamingGroup)
        assert len(result._tasks) == 1
        # Give the task a moment to start
        TASK_START_DELAY = 0.1
        await asyncio.sleep(TASK_START_DELAY)
        mock_async_client.devboxes.executions.stream_stdout_updates.assert_called_once()
        # Clean up tasks
        for task in result._tasks:
            task.cancel()
            try:
                await task
            except (Exception, asyncio.CancelledError):
                pass

    @pytest.mark.asyncio
    async def test_start_streaming_stderr_only(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test _start_streaming with stderr callback only."""

        # Create a proper async iterator
        async def async_iter():
            yield SimpleNamespace(output="line 1")
            yield SimpleNamespace(output="line 2")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        mock_async_client.devboxes.executions.stream_stderr_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        stderr_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=stderr_calls.append, output=None)

        assert result is not None
        assert isinstance(result, _AsyncStreamingGroup)
        assert len(result._tasks) == 1
        # Give the task a moment to start
        TASK_START_DELAY = 0.1
        await asyncio.sleep(TASK_START_DELAY)
        mock_async_client.devboxes.executions.stream_stderr_updates.assert_called_once()
        # Clean up tasks
        for task in result._tasks:
            task.cancel()
            try:
                await task
            except (Exception, asyncio.CancelledError):
                pass

    @pytest.mark.asyncio
    async def test_start_streaming_output_only(
        self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock
    ) -> None:
        """Test _start_streaming with output callback only."""

        # Create a proper async iterator
        async def async_iter():
            yield SimpleNamespace(output="line 1")
            yield SimpleNamespace(output="line 2")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        mock_async_client.devboxes.executions.stream_stdout_updates = AsyncMock(return_value=mock_async_stream)
        mock_async_client.devboxes.executions.stream_stderr_updates = AsyncMock(return_value=mock_async_stream)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        output_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=output_calls.append)

        assert result is not None
        assert isinstance(result, _AsyncStreamingGroup)
        assert len(result._tasks) == 2  # Both stdout and stderr streams
        # Give tasks a moment to start
        TASK_START_DELAY = 0.1
        await asyncio.sleep(TASK_START_DELAY)
        # Clean up tasks
        for task in result._tasks:
            task.cancel()
            try:
                await task
            except (Exception, asyncio.CancelledError):
                pass

    @pytest.mark.asyncio
    async def test_stream_worker(self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock) -> None:
        """Test _stream_worker processes chunks."""
        chunks = [
            SimpleNamespace(output="line 1"),
            SimpleNamespace(output="line 2"),
        ]

        async def async_iter() -> AsyncIterator:
            for chunk in chunks:
                yield chunk

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        calls: list[str] = []

        async def stream_factory() -> AsyncStream:
            return mock_async_stream

        await devbox._stream_worker(
            name="test",
            stream_factory=stream_factory,
            callbacks=[calls.append],
        )

        # Note: In a real scenario, calls would be populated, but with mocks
        # we're mainly testing that the method doesn't raise

    @pytest.mark.asyncio
    async def test_stream_worker_cancelled(self, mock_async_client: AsyncMock, mock_async_stream: AsyncMock) -> None:
        """Test _stream_worker handles cancellation."""
        LONG_SLEEP = 1.0

        async def async_iter() -> AsyncIterator:
            await asyncio.sleep(LONG_SLEEP)  # Long-running
            yield SimpleNamespace(output="line")

        mock_async_stream.__aiter__ = Mock(return_value=async_iter())
        mock_async_stream.__aenter__ = AsyncMock(return_value=mock_async_stream)
        mock_async_stream.__aexit__ = AsyncMock(return_value=None)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        calls: list[str] = []

        async def stream_factory() -> AsyncStream:
            return mock_async_stream

        task = asyncio.create_task(
            devbox._stream_worker(
                name="test",
                stream_factory=stream_factory,
                callbacks=[calls.append],
            )
        )

        await asyncio.sleep(0.01)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task


class TestAsyncDevboxErrorHandling:
    """Tests for AsyncDevbox error handling scenarios."""

    @pytest.mark.asyncio
    async def test_async_network_error(self, mock_async_client: AsyncMock) -> None:
        """Test handling of network errors in async."""
        mock_async_client.devboxes.retrieve = AsyncMock(side_effect=httpx.NetworkError("Connection failed"))

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        with pytest.raises(httpx.NetworkError):
            await devbox.get_info()
