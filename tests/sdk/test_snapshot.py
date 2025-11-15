"""Comprehensive tests for sync Snapshot class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import MockDevboxView, MockSnapshotView
from runloop_api_client.sdk import Snapshot
from runloop_api_client.lib.polling import PollingConfig


class TestSnapshot:
    """Tests for Snapshot class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Snapshot initialization."""
        snapshot = Snapshot(mock_client, "snap_123")
        assert snapshot.id == "snap_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Snapshot string representation."""
        snapshot = Snapshot(mock_client, "snap_123")
        assert repr(snapshot) == "<Snapshot id='snap_123'>"

    def test_get_info(self, mock_client: Mock, snapshot_view: MockSnapshotView) -> None:
        """Test get_info method."""
        mock_client.devboxes.disk_snapshots.query_status.return_value = snapshot_view

        snapshot = Snapshot(mock_client, "snap_123")
        result = snapshot.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == snapshot_view
        mock_client.devboxes.disk_snapshots.query_status.assert_called_once_with(
            "snap_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_update(self, mock_client: Mock) -> None:
        """Test update method."""
        updated_snapshot = SimpleNamespace(id="snap_123", name="updated-name")
        mock_client.devboxes.disk_snapshots.update.return_value = updated_snapshot

        snapshot = Snapshot(mock_client, "snap_123")
        result = snapshot.update(
            commit_message="Update message",
            metadata={"key": "value"},
            name="updated-name",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == updated_snapshot
        mock_client.devboxes.disk_snapshots.update.assert_called_once_with(
            "snap_123",
            commit_message="Update message",
            metadata={"key": "value"},
            name="updated-name",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_delete(self, mock_client: Mock) -> None:
        """Test delete method."""
        mock_client.devboxes.disk_snapshots.delete.return_value = object()

        snapshot = Snapshot(mock_client, "snap_123")
        result = snapshot.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None  # Verify return value is propagated
        mock_client.devboxes.disk_snapshots.delete.assert_called_once_with(
            "snap_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_await_completed(self, mock_client: Mock, snapshot_view: MockSnapshotView) -> None:
        """Test await_completed method."""
        mock_client.devboxes.disk_snapshots.await_completed.return_value = snapshot_view
        polling_config = PollingConfig(timeout_seconds=60.0)

        snapshot = Snapshot(mock_client, "snap_123")
        result = snapshot.await_completed(
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == snapshot_view
        mock_client.devboxes.disk_snapshots.await_completed.assert_called_once_with(
            "snap_123",
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_create_devbox(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_devbox method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        snapshot = Snapshot(mock_client, "snap_123")
        devbox = snapshot.create_devbox(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=PollingConfig(timeout_seconds=60.0),
            extra_headers={"X-Custom": "value"},
        )

        assert devbox.id == "dev_123"
        mock_client.devboxes.create_and_await_running.assert_called_once()
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["snapshot_id"] == "snap_123"
        assert call_kwargs["name"] == "test-devbox"
        assert call_kwargs["metadata"] == {"key": "value"}
