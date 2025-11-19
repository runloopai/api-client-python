"""Comprehensive tests for async Snapshot class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockDevboxView, MockSnapshotView
from runloop_api_client.sdk import AsyncSnapshot
from runloop_api_client.lib.polling import PollingConfig


class TestAsyncSnapshot:
    """Tests for AsyncSnapshot class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncSnapshot initialization."""
        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        assert snapshot.id == "snap_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncSnapshot string representation."""
        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        assert repr(snapshot) == "<AsyncSnapshot id='snap_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, snapshot_view: MockSnapshotView) -> None:
        """Test get_info method."""
        mock_async_client.devboxes.disk_snapshots.query_status = AsyncMock(return_value=snapshot_view)

        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        result = await snapshot.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == snapshot_view
        mock_async_client.devboxes.disk_snapshots.query_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_update(self, mock_async_client: AsyncMock) -> None:
        """Test update method."""
        updated_snapshot = SimpleNamespace(id="snap_123", name="updated-name")
        mock_async_client.devboxes.disk_snapshots.update = AsyncMock(return_value=updated_snapshot)

        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        result = await snapshot.update(
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
        mock_async_client.devboxes.disk_snapshots.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete(self, mock_async_client: AsyncMock) -> None:
        """Test delete method."""
        mock_async_client.devboxes.disk_snapshots.delete = AsyncMock(return_value=object())

        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        result = await snapshot.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result is not None  # Verify return value is propagated
        mock_async_client.devboxes.disk_snapshots.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_await_completed(self, mock_async_client: AsyncMock, snapshot_view: MockSnapshotView) -> None:
        """Test await_completed method."""
        mock_async_client.devboxes.disk_snapshots.await_completed = AsyncMock(return_value=snapshot_view)
        polling_config = PollingConfig(timeout_seconds=60.0)

        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        result = await snapshot.await_completed(
            polling_config=polling_config,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == snapshot_view
        mock_async_client.devboxes.disk_snapshots.await_completed.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_devbox(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create_devbox method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        snapshot = AsyncSnapshot(mock_async_client, "snap_123")
        devbox = await snapshot.create_devbox(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=PollingConfig(timeout_seconds=60.0),
            extra_headers={"X-Custom": "value"},
        )

        assert devbox.id == "dev_123"
        mock_async_client.devboxes.create_and_await_running.assert_called_once()
