"""Asynchronous SDK smoke tests for Storage Object operations."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestAsyncStorageObjectLifecycle:
    """Test basic async storage object lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_create(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a storage object."""
        obj = await async_sdk_client.storage_object.create(
            name=unique_name("sdk-async-storage-object"),
            content_type="text",
            metadata={"test": "sdk-async-smoketest"},
        )

        try:
            assert obj is not None
            assert obj.id is not None
            assert len(obj.id) > 0
            assert obj.upload_url is not None
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving storage object information."""
        obj = await async_sdk_client.storage_object.create(
            name=unique_name("sdk-async-storage-object-info"),
            content_type="text",
        )

        try:
            info = await obj.refresh()

            assert info.id == obj.id
            assert info.name is not None
            assert info.content_type == "text"
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_upload_and_complete(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading content and completing object."""
        obj = await async_sdk_client.storage_object.create(
            name=unique_name("sdk-async-storage-upload"),
            content_type="text",
        )

        try:
            # Upload content
            await obj.upload_content("Hello from async SDK storage!")

            # Complete the object
            result = await obj.complete()
            assert result is not None
            assert result.state == "READ_ONLY"
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_delete(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test deleting a storage object."""
        obj = await async_sdk_client.storage_object.create(
            name=unique_name("sdk-async-storage-delete"),
            content_type="text",
        )

        obj_id = obj.id
        result = await obj.delete()

        assert result is not None
        # Verify it's deleted
        info = await async_sdk_client.api.objects.retrieve(obj_id)
        assert info.state == "DELETED"


class TestAsyncStorageObjectUploadMethods:
    """Test various async storage object upload methods."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_upload_from_text(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading from text."""
        text_content = "Hello from async upload_from_text!"
        obj = await async_sdk_client.storage_object.upload_from_text(
            text_content,
            unique_name("sdk-async-text-upload"),
            metadata={"source": "upload_from_text"},
        )

        try:
            assert obj.id is not None

            # Verify content
            downloaded = await obj.download_as_text(duration_seconds=120)
            assert downloaded == text_content
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_upload_from_bytes(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading from bytes."""
        bytes_content = b"Binary content from async SDK"
        obj = await async_sdk_client.storage_object.upload_from_bytes(
            bytes_content,
            unique_name("sdk-async-bytes-upload"),
            content_type="text",
            metadata={"source": "upload_from_bytes"},
        )

        try:
            assert obj.id is not None

            # Verify content
            downloaded = await obj.download_as_bytes(duration_seconds=120)
            assert downloaded == bytes_content
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_upload_from_file(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading from file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
            tmp_file.write("Content from async file upload")
            tmp_path = tmp_file.name

        try:
            obj = await async_sdk_client.storage_object.upload_from_file(
                tmp_path,
                unique_name("sdk-async-file-upload"),
                metadata={"source": "upload_from_file"},
            )

            try:
                assert obj.id is not None

                # Verify content
                downloaded = await obj.download_as_text(duration_seconds=150)
                assert downloaded == "Content from async file upload"
            finally:
                await obj.delete()
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestAsyncStorageObjectDownloadMethods:
    """Test async storage object download methods."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_download_as_text(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test downloading content as text."""
        content = "Async text content to download"
        obj = await async_sdk_client.storage_object.upload_from_text(
            content,
            unique_name("sdk-async-download-text"),
        )

        try:
            downloaded = await obj.download_as_text(duration_seconds=90)
            assert downloaded == content
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_download_as_bytes(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test downloading content as bytes."""
        content = b"Async bytes content to download"
        obj = await async_sdk_client.storage_object.upload_from_bytes(
            content,
            unique_name("sdk-async-download-bytes"),
            content_type="text",
        )

        try:
            downloaded = await obj.download_as_bytes(duration_seconds=120)
            assert downloaded == content
            assert isinstance(downloaded, bytes)
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_get_download_url(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test getting download URL."""
        obj = await async_sdk_client.storage_object.upload_from_text(
            "Content for async URL",
            unique_name("sdk-async-download-url"),
        )

        try:
            url_info = await obj.get_download_url(duration_seconds=3600)
            assert url_info.download_url is not None
            assert "http" in url_info.download_url
        finally:
            await obj.delete()


class TestAsyncStorageObjectListing:
    """Test async storage object listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_storage_objects(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing storage objects."""
        objects = await async_sdk_client.storage_object.list(limit=10)

        assert isinstance(objects, list)
        # List might be empty, that's okay
        assert len(objects) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_get_storage_object_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving storage object by ID."""
        # Create an object
        created = await async_sdk_client.storage_object.upload_from_text(
            "Content for async retrieval",
            unique_name("sdk-async-storage-retrieve"),
        )

        try:
            # Retrieve it by ID
            retrieved = async_sdk_client.storage_object.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same object
            info = await retrieved.refresh()
            assert info.id == created.id
        finally:
            await created.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_storage_objects_by_content_type(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing storage objects filtered by content type."""
        # Create object with specific content type
        obj = await async_sdk_client.storage_object.upload_from_text(
            "Text content",
            unique_name("sdk-async-storage-list-type"),
        )

        try:
            # List objects with text content type
            objects = await async_sdk_client.storage_object.list(content_type="text", limit=10)

            assert isinstance(objects, list)
            # Should find our object
            object_ids = [o.id for o in objects]
            assert obj.id in object_ids
        finally:
            await obj.delete()


class TestAsyncStorageObjectDevboxIntegration:
    """Test async storage object integration with devboxes."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_mount_storage_object_to_devbox(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test mounting storage object to devbox."""
        # Create storage object with content
        obj = await async_sdk_client.storage_object.upload_from_text(
            "Async mounted content from SDK",
            unique_name("sdk-async-mount-object"),
        )

        try:
            # Create devbox with mounted storage object
            devbox = await async_sdk_client.devbox.create(
                name=unique_name("sdk-async-devbox-mount"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                mounts=[
                    {
                        "type": "object_mount",
                        "object_id": obj.id,
                        "object_path": "/home/user/async-mounted-data",
                    }
                ],
            )

            try:
                assert devbox.id is not None
                info = await devbox.get_info()
                assert info.status == "running"
            finally:
                await devbox.shutdown()
        finally:
            await obj.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_access_mounted_storage_object(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test accessing mounted storage object content in devbox."""
        # Create storage object
        obj = await async_sdk_client.storage_object.upload_from_text(
            "Async content to mount and access",
            unique_name("sdk-async-mount-access"),
        )

        try:
            # Create devbox with mounted storage object
            devbox = await async_sdk_client.devbox.create(
                name=unique_name("sdk-async-devbox-mount-access"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                mounts=[
                    {
                        "type": "object_mount",
                        "object_id": obj.id,
                        "object_path": "/home/user/async-mounted-file",
                    }
                ],
            )

            try:
                # Read the mounted file
                content = await devbox.file.read(file_path="/home/user/async-mounted-file")
                assert content == "Async content to mount and access"

                # Verify file exists via command
                result = await devbox.cmd.exec(command="test -f /home/user/async-mounted-file && echo 'exists'")
                stdout = await result.stdout(num_lines=1)
                assert "exists" in stdout
            finally:
                await devbox.shutdown()
        finally:
            await obj.delete()


class TestAsyncStorageObjectEdgeCases:
    """Test async storage object edge cases and special scenarios."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_large_content(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading larger content."""
        # Create 1MB of content
        large_content = "x" * (1024 * 1024)

        obj = await async_sdk_client.storage_object.upload_from_text(
            large_content,
            unique_name("sdk-async-storage-large"),
        )

        try:
            # Verify content
            downloaded = await obj.download_as_text(duration_seconds=120)
            assert len(downloaded) == len(large_content)
            assert downloaded == large_content
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_binary_content(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading binary content."""
        # Create some binary data
        binary_content = bytes(range(256))

        obj = await async_sdk_client.storage_object.upload_from_bytes(
            binary_content,
            unique_name("sdk-async-storage-binary"),
            content_type="binary",
        )

        try:
            # Verify content
            downloaded = await obj.download_as_bytes(duration_seconds=120)
            assert downloaded == binary_content
        finally:
            await obj.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_empty_content(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test uploading empty content."""
        obj = await async_sdk_client.storage_object.upload_from_text(
            "",
            unique_name("sdk-async-storage-empty"),
        )

        try:
            # Verify content
            downloaded = await obj.download_as_text(duration_seconds=60)
            assert downloaded == ""
        finally:
            await obj.delete()


class TestAsyncStorageObjectWorkflows:
    """Test complete async storage object workflows."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_complete_upload_download_workflow(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test complete workflow: create, upload, complete, download, delete."""
        # Create object
        obj = await async_sdk_client.storage_object.create(
            name=unique_name("sdk-async-storage-workflow"),
            content_type="text",
            metadata={"workflow": "async-test"},
        )

        try:
            # Upload content
            original_content = "Async workflow test content"
            await obj.upload_content(original_content)

            # Complete
            result = await obj.complete()
            assert result.state == "READ_ONLY"

            # Download and verify
            downloaded = await obj.download_as_text(duration_seconds=120)
            assert downloaded == original_content

            # Refresh info
            info = await obj.refresh()
            assert info.state == "READ_ONLY"
        finally:
            # Delete
            await obj.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_storage_object_in_devbox_workflow(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test workflow: create storage object, write from devbox, download."""
        # Create empty storage object
        obj = await async_sdk_client.storage_object.create(
            name=unique_name("sdk-async-storage-devbox-workflow"),
            content_type="text",
        )

        try:
            # Upload initial content
            await obj.upload_content("Async initial content")
            await obj.complete()

            # Create devbox with mounted object
            devbox = await async_sdk_client.devbox.create(
                name=unique_name("sdk-async-devbox-workflow"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                mounts=[
                    {
                        "type": "object_mount",
                        "object_id": obj.id,
                        "object_path": "/home/user/async-workflow-data",
                    }
                ],
            )

            try:
                # Read mounted content in devbox
                content = await devbox.file.read(file_path="/home/user/async-workflow-data")
                assert content == "Async initial content"

                # Verify we can work with the file
                result = await devbox.cmd.exec(command="cat /home/user/async-workflow-data")
                stdout = await result.stdout(num_lines=1)
                assert "Async initial content" in stdout
            finally:
                await devbox.shutdown()
        finally:
            await obj.delete()
