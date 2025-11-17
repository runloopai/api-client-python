"""Tests for core AsyncDevbox functionality.

Tests the primary AsyncDevbox class including initialization, async CRUD
operations, snapshot creation, blueprint launching, and async execution methods.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockDevboxView
from runloop_api_client.sdk import AsyncDevbox
from runloop_api_client.lib.polling import PollingConfig
from runloop_api_client.sdk.async_devbox import (
    _AsyncFileInterface,
    _AsyncCommandInterface,
    _AsyncNetworkInterface,
)


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
    async def test_context_manager_enter_exit(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test context manager behavior with successful shutdown."""
        mock_async_client.devboxes.shutdown = AsyncMock(return_value=devbox_view)

        async with AsyncDevbox(mock_async_client, "dev_123") as devbox:
            assert devbox.id == "dev_123"

        call_kwargs = mock_async_client.devboxes.shutdown.call_args[1]
        assert "timeout" not in call_kwargs

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
    async def test_get_info(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
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
    async def test_await_running(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
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
    async def test_await_suspended(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
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
    async def test_shutdown(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
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
    async def test_suspend(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test suspend method."""
        mock_async_client.devboxes.suspend = AsyncMock(return_value=devbox_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.suspend(
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

    @pytest.mark.asyncio
    async def test_resume(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test resume method."""
        mock_async_client.devboxes.resume = AsyncMock(return_value=devbox_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.resume(
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

    @pytest.mark.asyncio
    async def test_keep_alive(self, mock_async_client: AsyncMock) -> None:
        """Test keep_alive method."""
        mock_async_client.devboxes.keep_alive = AsyncMock(return_value=object())

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        result = await devbox.keep_alive(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None  # Verify return value is propagated
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
        call_kwargs = mock_async_client.devboxes.snapshot_disk_async.call_args[1]
        assert "commit_message" not in call_kwargs
        assert call_kwargs["metadata"] == {"key": "value"}
        assert call_kwargs["name"] == "test-snapshot"
        assert call_kwargs["extra_headers"] == {"X-Custom": "value"}
        assert "polling_config" not in call_kwargs
        assert "timeout" not in call_kwargs
        mock_async_client.devboxes.disk_snapshots.await_completed.assert_called_once()
        call_kwargs2 = mock_async_client.devboxes.disk_snapshots.await_completed.call_args[1]
        assert call_kwargs2["polling_config"] == polling_config
        assert "timeout" not in call_kwargs2

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
        call_kwargs = mock_async_client.devboxes.snapshot_disk_async.call_args[1]
        assert "commit_message" not in call_kwargs
        assert call_kwargs["metadata"] == {"key": "value"}
        assert call_kwargs["name"] == "test-snapshot"
        assert call_kwargs["extra_headers"] == {"X-Custom": "value"}
        assert "polling_config" not in call_kwargs
        assert "timeout" not in call_kwargs

    @pytest.mark.asyncio
    async def test_close(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test close method calls shutdown."""
        mock_async_client.devboxes.shutdown = AsyncMock(return_value=devbox_view)

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        await devbox.close()

        mock_async_client.devboxes.shutdown.assert_called_once()
        call_kwargs = mock_async_client.devboxes.shutdown.call_args[1]
        assert "timeout" not in call_kwargs

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
