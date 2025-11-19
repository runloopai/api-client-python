"""Synchronous SDK smoke tests for Storage Object operations."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestStorageObjectLifecycle:
    """Test basic storage object lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_create(self, sdk_client: RunloopSDK) -> None:
        """Test creating a storage object."""
        obj = sdk_client.storage_object.create(
            name=unique_name("sdk-storage-object"),
            content_type="text",
            metadata={"test": "sdk-smoketest"},
        )

        try:
            assert obj is not None
            assert obj.id is not None
            assert len(obj.id) > 0
            assert obj.upload_url is not None
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_get_info(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving storage object information."""
        obj = sdk_client.storage_object.create(
            name=unique_name("sdk-storage-object-info"),
            content_type="text",
        )

        try:
            info = obj.refresh()

            assert info.id == obj.id
            assert info.name is not None
            assert info.content_type == "text"
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_upload_and_complete(self, sdk_client: RunloopSDK) -> None:
        """Test uploading content and completing object."""
        obj = sdk_client.storage_object.create(
            name=unique_name("sdk-storage-upload"),
            content_type="text",
        )

        try:
            # Upload content
            obj.upload_content("Hello from SDK storage!")

            # Complete the object
            result = obj.complete()
            assert result is not None
            assert result.state == "READ_ONLY"
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_delete(self, sdk_client: RunloopSDK) -> None:
        """Test deleting a storage object."""
        obj = sdk_client.storage_object.create(
            name=unique_name("sdk-storage-delete"),
            content_type="text",
        )

        obj_id = obj.id
        result = obj.delete()

        assert result is not None
        # Verify it's deleted
        info = sdk_client.api.objects.retrieve(obj_id)
        assert info.state == "DELETED"


class TestStorageObjectUploadMethods:
    """Test various storage object upload methods."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_upload_from_text(self, sdk_client: RunloopSDK) -> None:
        """Test uploading from text."""
        text_content = "Hello from upload_from_text!"
        obj = sdk_client.storage_object.upload_from_text(
            text_content,
            unique_name("sdk-text-upload"),
            metadata={"source": "upload_from_text"},
        )

        try:
            assert obj.id is not None

            # Verify content
            downloaded = obj.download_as_text(duration_seconds=120)
            assert downloaded == text_content
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_upload_from_bytes(self, sdk_client: RunloopSDK) -> None:
        """Test uploading from bytes."""
        bytes_content = b"Binary content from SDK"
        obj = sdk_client.storage_object.upload_from_bytes(
            bytes_content,
            unique_name("sdk-bytes-upload"),
            content_type="text",
            metadata={"source": "upload_from_bytes"},
        )

        try:
            assert obj.id is not None

            # Verify content
            downloaded = obj.download_as_bytes(duration_seconds=120)
            assert downloaded == bytes_content
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_upload_from_file(self, sdk_client: RunloopSDK) -> None:
        """Test uploading from file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
            tmp_file.write("Content from file upload")
            tmp_path = tmp_file.name

        try:
            obj = sdk_client.storage_object.upload_from_file(
                tmp_path,
                unique_name("sdk-file-upload"),
                metadata={"source": "upload_from_file"},
            )

            try:
                assert obj.id is not None

                # Verify content
                downloaded = obj.download_as_text(duration_seconds=150)
                assert downloaded == "Content from file upload"
            finally:
                obj.delete()
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestStorageObjectDownloadMethods:
    """Test storage object download methods."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_download_as_text(self, sdk_client: RunloopSDK) -> None:
        """Test downloading content as text."""
        content = "Text content to download"
        obj = sdk_client.storage_object.upload_from_text(
            content,
            unique_name("sdk-download-text"),
        )

        try:
            downloaded = obj.download_as_text(duration_seconds=120)
            assert downloaded == content
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_download_as_bytes(self, sdk_client: RunloopSDK) -> None:
        """Test downloading content as bytes."""
        content = b"Bytes content to download"
        obj = sdk_client.storage_object.upload_from_bytes(
            content,
            unique_name("sdk-download-bytes"),
            content_type="text",
        )

        try:
            downloaded = obj.download_as_bytes(duration_seconds=120)
            assert downloaded == content
            assert isinstance(downloaded, bytes)
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_get_download_url(self, sdk_client: RunloopSDK) -> None:
        """Test getting download URL."""
        obj = sdk_client.storage_object.upload_from_text(
            "Content for URL",
            unique_name("sdk-download-url"),
        )

        try:
            url_info = obj.get_download_url(duration_seconds=3600)
            assert url_info.download_url is not None
            assert "http" in url_info.download_url
        finally:
            obj.delete()


class TestStorageObjectListing:
    """Test storage object listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_storage_objects(self, sdk_client: RunloopSDK) -> None:
        """Test listing storage objects."""
        objects = sdk_client.storage_object.list(limit=10)

        assert isinstance(objects, list)
        # List might be empty, that's okay
        assert len(objects) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_get_storage_object_by_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving storage object by ID."""
        # Create an object
        created = sdk_client.storage_object.upload_from_text(
            "Content for retrieval",
            unique_name("sdk-storage-retrieve"),
        )

        try:
            # Retrieve it by ID
            retrieved = sdk_client.storage_object.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same object
            info = retrieved.refresh()
            assert info.id == created.id
        finally:
            created.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_storage_objects_by_content_type(self, sdk_client: RunloopSDK) -> None:
        """Test listing storage objects filtered by content type."""
        # Create object with specific content type
        obj = sdk_client.storage_object.upload_from_text(
            "Text content",
            unique_name("sdk-storage-list-type"),
        )

        try:
            # List objects with text content type
            objects = sdk_client.storage_object.list(content_type="text", limit=10)

            assert isinstance(objects, list)
            # Should find our object
            object_ids = [o.id for o in objects]
            assert obj.id in object_ids
        finally:
            obj.delete()


class TestStorageObjectDevboxIntegration:
    """Test storage object integration with devboxes."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_mount_storage_object_to_devbox(self, sdk_client: RunloopSDK) -> None:
        """Test mounting storage object to devbox."""
        # Create storage object with content
        obj = sdk_client.storage_object.upload_from_text(
            "Mounted content from SDK",
            unique_name("sdk-mount-object"),
        )

        try:
            # Create devbox with mounted storage object
            devbox = sdk_client.devbox.create(
                name=unique_name("sdk-devbox-mount"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                mounts=[
                    {
                        "type": "object_mount",
                        "object_id": obj.id,
                        "object_path": "/home/user/mounted-data",
                    }
                ],
            )

            try:
                assert devbox.id is not None
                info = devbox.get_info()
                assert info.status == "running"
            finally:
                devbox.shutdown()
        finally:
            obj.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_access_mounted_storage_object(self, sdk_client: RunloopSDK) -> None:
        """Test accessing mounted storage object content in devbox."""
        # Create storage object
        obj = sdk_client.storage_object.upload_from_text(
            "Content to mount and access",
            unique_name("sdk-mount-access"),
        )

        try:
            # Create devbox with mounted storage object
            devbox = sdk_client.devbox.create(
                name=unique_name("sdk-devbox-mount-access"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                mounts=[
                    {
                        "type": "object_mount",
                        "object_id": obj.id,
                        "object_path": "/home/user/mounted-file",
                    }
                ],
            )

            try:
                # Read the mounted file
                content = devbox.file.read(file_path="/home/user/mounted-file")
                assert content == "Content to mount and access"

                # Verify file exists via command
                result = devbox.cmd.exec(command="test -f /home/user/mounted-file && echo 'exists'")
                assert "exists" in result.stdout(num_lines=1)
            finally:
                devbox.shutdown()
        finally:
            obj.delete()


class TestStorageObjectEdgeCases:
    """Test storage object edge cases and special scenarios."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_large_content(self, sdk_client: RunloopSDK) -> None:
        """Test uploading larger content."""
        # Create 1MB of content
        large_content = "x" * (1024 * 1024)

        obj = sdk_client.storage_object.upload_from_text(
            large_content,
            unique_name("sdk-storage-large"),
        )

        try:
            # Verify content
            downloaded = obj.download_as_text(duration_seconds=120)
            assert len(downloaded) == len(large_content)
            assert downloaded == large_content
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_binary_content(self, sdk_client: RunloopSDK) -> None:
        """Test uploading binary content."""
        # Create some binary data
        binary_content = bytes(range(256))

        obj = sdk_client.storage_object.upload_from_bytes(
            binary_content,
            unique_name("sdk-storage-binary"),
            content_type="binary",
        )

        try:
            # Verify content
            downloaded = obj.download_as_bytes(duration_seconds=120)
            assert downloaded == binary_content
        finally:
            obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_empty_content(self, sdk_client: RunloopSDK) -> None:
        """Test uploading empty content."""
        obj = sdk_client.storage_object.upload_from_text(
            "",
            unique_name("sdk-storage-empty"),
        )

        try:
            # Verify content
            downloaded = obj.download_as_text(duration_seconds=90)
            assert downloaded == ""
        finally:
            obj.delete()


class TestStorageObjectWorkflows:
    """Test complete storage object workflows."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_complete_upload_download_workflow(self, sdk_client: RunloopSDK) -> None:
        """Test complete workflow: create, upload, complete, download, delete."""
        # Create object
        obj = sdk_client.storage_object.create(
            name=unique_name("sdk-storage-workflow"),
            content_type="text",
            metadata={"workflow": "test"},
        )

        try:
            # Upload content
            original_content = "Workflow test content"
            obj.upload_content(original_content)

            # Complete
            result = obj.complete()
            assert result.state == "READ_ONLY"

            # Download and verify
            downloaded = obj.download_as_text(duration_seconds=120)
            assert downloaded == original_content

            # Refresh info
            info = obj.refresh()
            assert info.state == "READ_ONLY"
        finally:
            # Delete
            obj.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_storage_object_in_devbox_workflow(self, sdk_client: RunloopSDK) -> None:
        """Test workflow: create storage object, write from devbox, download."""
        # Create empty storage object
        obj = sdk_client.storage_object.create(
            name=unique_name("sdk-storage-devbox-workflow"),
            content_type="text",
        )

        try:
            # Upload initial content
            obj.upload_content("Initial content")
            obj.complete()

            # Create devbox with mounted object
            devbox = sdk_client.devbox.create(
                name=unique_name("sdk-devbox-workflow"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                mounts=[
                    {
                        "type": "object_mount",
                        "object_id": obj.id,
                        "object_path": "/home/user/workflow-data",
                    }
                ],
            )

            try:
                # Read mounted content in devbox
                content = devbox.file.read(file_path="/home/user/workflow-data")
                assert content == "Initial content"

                # Verify we can work with the file
                result = devbox.cmd.exec(command="cat /home/user/workflow-data")
                assert "Initial content" in result.stdout(num_lines=1)
            finally:
                devbox.shutdown()
        finally:
            obj.delete()
