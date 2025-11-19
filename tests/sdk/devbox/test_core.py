"""Tests for core Devbox functionality.

Tests the primary Devbox class including initialization, CRUD operations,
snapshot creation, blueprint launching, and execution methods.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from tests.sdk.conftest import (
    MockDevboxView,
)
from runloop_api_client.sdk import Devbox
from runloop_api_client._types import omit
from runloop_api_client.sdk.devbox import (
    _FileInterface,
    _CommandInterface,
    _NetworkInterface,
)
from runloop_api_client.lib.polling import PollingConfig


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

    def test_context_manager_enter_exit(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test context manager behavior with successful shutdown."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        with Devbox(mock_client, "dev_123") as devbox:
            assert devbox.id == "dev_123"

        call_kwargs = mock_client.devboxes.shutdown.call_args[1]
        assert "timeout" not in call_kwargs

    def test_context_manager_exception_handling(self, mock_client: Mock) -> None:
        """Test context manager handles exceptions during shutdown."""
        mock_client.devboxes.shutdown.side_effect = RuntimeError("Shutdown failed")

        with pytest.raises(ValueError, match="Test error"):
            with Devbox(mock_client, "dev_123"):
                raise ValueError("Test error")

        # Shutdown should be called even when body raises exception
        mock_client.devboxes.shutdown.assert_called_once()

    def test_get_info(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
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

    def test_await_running(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
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

    def test_await_suspended(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
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

    def test_shutdown(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
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

    def test_suspend(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
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

    def test_resume(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
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
        mock_client.devboxes.keep_alive.return_value = object()

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.keep_alive(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None  # Verify return value is propagated
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
        assert "commit_message" not in call_kwargs or call_kwargs["commit_message"] in (omit, None)
        assert call_kwargs["metadata"] == {"key": "value"}
        assert call_kwargs["name"] == "test-snapshot"
        assert call_kwargs["extra_headers"] == {"X-Custom": "value"}
        assert "polling_config" not in call_kwargs
        assert "timeout" not in call_kwargs
        call_kwargs2 = mock_client.devboxes.disk_snapshots.await_completed.call_args[1]
        assert call_kwargs2["polling_config"] == polling_config
        assert "timeout" not in call_kwargs2

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
        assert "commit_message" not in call_kwargs or call_kwargs["commit_message"] in (omit, None)
        assert call_kwargs["metadata"] == {"key": "value"}
        assert call_kwargs["name"] == "test-snapshot"
        assert call_kwargs["extra_headers"] == {"X-Custom": "value"}
        assert "polling_config" not in call_kwargs
        assert "timeout" not in call_kwargs
        # Verify async method does not wait for completion
        if hasattr(mock_client.devboxes.disk_snapshots, "await_completed"):
            assert not mock_client.devboxes.disk_snapshots.await_completed.called

    def test_close(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test close method calls shutdown."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        devbox = Devbox(mock_client, "dev_123")
        devbox.close()

        call_kwargs = mock_client.devboxes.shutdown.call_args[1]
        assert "timeout" not in call_kwargs

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
