"""Asynchronous SDK smoke tests for Snapshot operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.lib.polling import PollingConfig

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

TWO_MINUTE_TIMEOUT = 120
FOUR_MINUTE_TIMEOUT = 240


class TestAsyncSnapshotLifecycle:
    """Test basic async snapshot lifecycle operations."""

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_snapshot_create_and_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a snapshot from devbox."""
        # Create a devbox
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-for-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create a file to verify snapshot captures state
            await devbox.file.write(
                file_path="/tmp/async_snapshot_marker.txt", contents="This file should be in snapshot"
            )

            # Create snapshot
            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot"),
            )

            try:
                assert snapshot is not None
                assert snapshot.id is not None
                assert len(snapshot.id) > 0

                # Get snapshot info
                info = await snapshot.get_info()
                assert info.status == "complete"
                assert info.snapshot is not None and info.snapshot.id == snapshot.id
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_snapshot_with_commit_message(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a snapshot with commit message."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-snapshot-commit"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-commit"),
                commit_message="Test async commit message from SDK",
            )

            try:
                assert snapshot.id is not None
                info = await snapshot.get_info()
                assert info.status == "complete"
                # Check if commit message is preserved
                assert (
                    info.snapshot is not None and info.snapshot.commit_message == "Test async commit message from SDK"
                )
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_snapshot_with_metadata(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a snapshot with metadata."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-snapshot-metadata"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            metadata = {
                "purpose": "sdk-async-testing",
                "version": "1.0",
            }

            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-metadata"),
                metadata=metadata,
            )

            try:
                assert snapshot.id is not None
                info = await snapshot.get_info()
                assert info.status == "complete"
                assert info.snapshot is not None and info.snapshot.metadata == metadata
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_snapshot_delete(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test deleting a snapshot."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-snapshot-delete"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-delete"),
            )

            snapshot_id = snapshot.id
            assert snapshot_id is not None

            # Delete should succeed without error
            result = await snapshot.delete()
            assert result is not None

            # Verify it's deleted by checking the status
            info = await snapshot.get_info()
            # After deletion, the snapshot should have a status indicating it's deleted
            assert info.status == "deleted"
        finally:
            await devbox.shutdown()


class TestAsyncSnapshotCompletion:
    """Test async snapshot completion and status tracking."""

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_snapshot_await_completed(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test waiting for snapshot completion."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-await-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot asynchronously
            snapshot = await devbox.snapshot_disk_async(
                name=unique_name("sdk-async-snapshot-await"),
            )

            try:
                # Wait for completion
                completed_info = await snapshot.await_completed(
                    polling_config=PollingConfig(timeout_seconds=120, interval_seconds=5)
                )

                assert completed_info.status == "complete"
                assert completed_info.snapshot is not None and completed_info.snapshot.id == snapshot.id
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_snapshot_status_tracking(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test tracking snapshot status through lifecycle."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-status"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot asynchronously to see status progression
            snapshot = await devbox.snapshot_disk_async(
                name=unique_name("sdk-async-snapshot-status"),
            )

            try:
                # Check initial status (might be in_progress or complete)
                info = await snapshot.get_info()
                assert info.status in ["in_progress", "complete"]

                # Wait for completion
                await snapshot.await_completed()

                # Check final status
                final_info = await snapshot.get_info()
                assert final_info.status == "complete"
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()


class TestAsyncSnapshotDevboxRestoration:
    """Test creating devboxes from snapshots asynchronously."""

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_restore_devbox_from_snapshot(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a devbox from a snapshot and verifying state is restored."""
        # Create source devbox
        source_devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-source-devbox"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create unique content in source devbox
            test_content = f"Async unique content: {unique_name('content')}"
            await source_devbox.file.write(file_path="/tmp/test_async_restore.txt", contents=test_content)

            # Create snapshot
            snapshot = await source_devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-restore"),
            )

            try:
                # Create new devbox from snapshot
                restored_devbox = await snapshot.create_devbox(
                    name=unique_name("sdk-async-restored-devbox"),
                    launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                )

                try:
                    # Verify devbox is running
                    assert restored_devbox.id is not None
                    info = await restored_devbox.get_info()
                    assert info.status == "running"

                    # Verify content from snapshot is present
                    restored_content = await restored_devbox.file.read(file_path="/tmp/test_async_restore.txt")
                    assert restored_content == test_content
                finally:
                    await restored_devbox.shutdown()
            finally:
                await snapshot.delete()
        finally:
            await source_devbox.shutdown()


class TestAsyncSnapshotListing:
    """Test async snapshot listing and retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_list_snapshots(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing snapshots."""
        snapshots = await async_sdk_client.snapshot.list(limit=10)

        assert isinstance(snapshots, list)
        # List might be empty, that's okay
        assert len(snapshots) >= 0

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_get_snapshot_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving snapshot by ID."""
        # Create a devbox and snapshot
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-retrieve-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-retrieve"),
            )

            try:
                # Retrieve it by ID
                retrieved = async_sdk_client.snapshot.from_id(snapshot.id)
                assert retrieved.id == snapshot.id

                # Verify it's the same snapshot
                info = await retrieved.get_info()
                assert info.snapshot is not None and info.snapshot.id == snapshot.id
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_list_snapshots_by_devbox(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing snapshots filtered by devbox."""
        # Create a devbox
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-list-snapshots"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot
            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-list"),
            )

            try:
                # List snapshots for this devbox
                snapshots = await async_sdk_client.snapshot.list(devbox_id=devbox.id)

                assert isinstance(snapshots, list)
                assert len(snapshots) >= 1

                # Should find our snapshot
                snapshot_ids = [s.id for s in snapshots]
                assert snapshot.id in snapshot_ids
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()
