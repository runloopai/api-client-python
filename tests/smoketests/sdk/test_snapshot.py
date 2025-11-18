"""Synchronous SDK smoke tests for Snapshot operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.lib.polling import PollingConfig

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestSnapshotLifecycle:
    """Test basic snapshot lifecycle operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_snapshot_create_and_info(self, sdk_client: RunloopSDK) -> None:
        """Test creating a snapshot from devbox."""
        # Create a devbox
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-for-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create a file to verify snapshot captures state
            devbox.file.write(file_path="/tmp/snapshot_marker.txt", contents="This file should be in snapshot")

            # Create snapshot
            snapshot = devbox.snapshot_disk(
                name=unique_name("sdk-snapshot"),
            )

            try:
                assert snapshot is not None
                assert snapshot.id is not None
                assert len(snapshot.id) > 0

                # Get snapshot info
                info = snapshot.get_info()
                assert info.snapshot is not None and info.snapshot.id == snapshot.id
                assert info.status == "complete"
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_snapshot_with_commit_message(self, sdk_client: RunloopSDK) -> None:
        """Test creating a snapshot with commit message."""
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-snapshot-commit"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            snapshot = devbox.snapshot_disk(
                name=unique_name("sdk-snapshot-commit"),
                commit_message="Test commit message from SDK",
            )

            try:
                assert snapshot.id is not None
                info = snapshot.get_info()
                assert info.status == "complete"
                # Check if commit message is preserved
                assert info.snapshot is not None and info.snapshot.commit_message == "Test commit message from SDK"
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_snapshot_with_metadata(self, sdk_client: RunloopSDK) -> None:
        """Test creating a snapshot with metadata."""
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-snapshot-metadata"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            metadata = {
                "purpose": "sdk-testing",
                "version": "1.0",
            }

            snapshot = devbox.snapshot_disk(
                name=unique_name("sdk-snapshot-metadata"),
                metadata=metadata,
            )

            try:
                assert snapshot.id is not None
                info = snapshot.get_info()
                assert info.status == "complete"
                assert info.snapshot is not None and info.snapshot.metadata == metadata
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_snapshot_delete(self, sdk_client: RunloopSDK) -> None:
        """Test deleting a snapshot."""
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-snapshot-delete"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            snapshot = devbox.snapshot_disk(
                name=unique_name("sdk-snapshot-delete"),
            )

            snapshot_id = snapshot.id
            assert snapshot_id is not None

            # Delete should succeed without error
            result = snapshot.delete()
            assert result is not None

            # Verify it's deleted by checking the status
            info = snapshot.get_info()
            # After deletion, the snapshot should have a status indicating it's deleted
            assert info.status == "deleted"
            print(info.status)
            print(info.error_message)
            print(info.snapshot)
        finally:
            devbox.shutdown()


class TestSnapshotCompletion:
    """Test snapshot completion and status tracking."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_snapshot_await_completed(self, sdk_client: RunloopSDK) -> None:
        """Test waiting for snapshot completion."""
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-await-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot asynchronously
            snapshot = devbox.snapshot_disk_async(
                name=unique_name("sdk-snapshot-await"),
            )

            try:
                # Wait for completion
                completed_info = snapshot.await_completed(
                    polling_config=PollingConfig(timeout_seconds=120, interval_seconds=5)
                )

                assert completed_info.status == "complete"
                assert completed_info.snapshot is not None and completed_info.snapshot.id == snapshot.id
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_snapshot_status_tracking(self, sdk_client: RunloopSDK) -> None:
        """Test tracking snapshot status through lifecycle."""
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-status"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot asynchronously to see status progression
            snapshot = devbox.snapshot_disk_async(
                name=unique_name("sdk-snapshot-status"),
            )

            try:
                # Check initial status (might be in_progress or complete)
                info = snapshot.get_info()
                assert info.status in ["in_progress", "complete"]

                # Wait for completion
                snapshot.await_completed()

                # Check final status
                final_info = snapshot.get_info()
                assert final_info.status == "complete"
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()


class TestSnapshotDevboxRestoration:
    """Test creating devboxes from snapshots."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT * 2)
    def test_restore_devbox_from_snapshot(self, sdk_client: RunloopSDK) -> None:
        """Test creating a devbox from a snapshot and verifying state is restored."""
        # Create source devbox
        source_devbox = sdk_client.devbox.create(
            name=unique_name("sdk-source-devbox"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create unique content in source devbox
            test_content = f"Unique content: {unique_name('content')}"
            source_devbox.file.write(file_path="/tmp/test_restore.txt", contents=test_content)

            # Create snapshot
            snapshot = source_devbox.snapshot_disk(
                name=unique_name("sdk-snapshot-restore"),
            )

            try:
                # Create new devbox from snapshot
                restored_devbox = snapshot.create_devbox(
                    name=unique_name("sdk-restored-devbox"),
                    launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                )

                try:
                    # Verify devbox is running
                    assert restored_devbox.id is not None
                    info = restored_devbox.get_info()
                    assert info.status == "running"

                    # Verify content from snapshot is present
                    restored_content = restored_devbox.file.read(file_path="/tmp/test_restore.txt")
                    assert restored_content == test_content
                finally:
                    restored_devbox.shutdown()
            finally:
                snapshot.delete()
        finally:
            source_devbox.shutdown()


class TestSnapshotListing:
    """Test snapshot listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_snapshots(self, sdk_client: RunloopSDK) -> None:
        """Test listing snapshots."""
        snapshots = sdk_client.snapshot.list(limit=10)

        assert isinstance(snapshots, list)
        # List might be empty, that's okay
        assert len(snapshots) >= 0

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_get_snapshot_by_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving snapshot by ID."""
        # Create a devbox and snapshot
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-retrieve-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            snapshot = devbox.snapshot_disk(
                name=unique_name("sdk-snapshot-retrieve"),
            )

            try:
                # Retrieve it by ID
                retrieved = sdk_client.snapshot.from_id(snapshot.id)
                assert retrieved.id == snapshot.id

                # Verify it's the same snapshot
                info = retrieved.get_info()
                assert info.snapshot is not None and info.snapshot.id == snapshot.id
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_list_snapshots_by_devbox(self, sdk_client: RunloopSDK) -> None:
        """Test listing snapshots filtered by devbox."""
        # Create a devbox
        devbox = sdk_client.devbox.create(
            name=unique_name("sdk-devbox-list-snapshots"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot
            snapshot = devbox.snapshot_disk(
                name=unique_name("sdk-snapshot-list"),
            )

            try:
                # List snapshots for this devbox
                snapshots = sdk_client.snapshot.list(devbox_id=devbox.id)

                assert isinstance(snapshots, list)
                assert len(snapshots) >= 1

                # Should find our snapshot
                snapshot_ids = [s.id for s in snapshots]
                assert snapshot.id in snapshot_ids
            finally:
                snapshot.delete()
        finally:
            devbox.shutdown()
