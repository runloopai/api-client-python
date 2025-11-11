"""Comprehensive tests for sync client classes."""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

from tests.sdk.conftest import (
    MockDevboxView,
    MockObjectView,
    MockSnapshotView,
    MockBlueprintView,
    create_mock_httpx_response,
)
from runloop_api_client.sdk import Devbox, Snapshot, Blueprint, StorageObject
from runloop_api_client.sdk._sync import (
    RunloopSDK,
    DevboxClient,
    SnapshotClient,
    BlueprintClient,
    StorageObjectClient,
)
from runloop_api_client.lib.polling import PollingConfig


class TestDevboxClient:
    """Tests for DevboxClient class."""

    def test_create(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        client = DevboxClient(mock_client)
        devbox = client.create(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(devbox, Devbox)
        assert devbox.id == "dev_123"
        mock_client.devboxes.create_and_await_running.assert_called_once()

    def test_create_from_blueprint_id(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_id method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        client = DevboxClient(mock_client)
        devbox = client.create_from_blueprint_id(
            "bp_123",
            name="test-devbox",
            metadata={"key": "value"},
        )

        assert isinstance(devbox, Devbox)
        assert devbox.id == "dev_123"
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_id"] == "bp_123"

    def test_create_from_blueprint_name(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_name method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        client = DevboxClient(mock_client)
        devbox = client.create_from_blueprint_name(
            "my-blueprint",
            name="test-devbox",
        )

        assert isinstance(devbox, Devbox)
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_name"] == "my-blueprint"

    def test_create_from_snapshot(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_from_snapshot method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        client = DevboxClient(mock_client)
        devbox = client.create_from_snapshot(
            "snap_123",
            name="test-devbox",
        )

        assert isinstance(devbox, Devbox)
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["snapshot_id"] == "snap_123"

    def test_from_id(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test from_id method waits for running."""
        mock_client.devboxes.await_running.return_value = devbox_view

        client = DevboxClient(mock_client)
        devbox = client.from_id("dev_123")

        assert isinstance(devbox, Devbox)
        assert devbox.id == "dev_123"
        mock_client.devboxes.await_running.assert_called_once_with("dev_123")

    def test_list(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test list method."""
        page = SimpleNamespace(devboxes=[devbox_view])
        mock_client.devboxes.list.return_value = page

        client = DevboxClient(mock_client)
        devboxes = client.list(
            limit=10,
            status="running",
            starting_after="dev_000",
        )

        assert len(devboxes) == 1
        assert isinstance(devboxes[0], Devbox)
        assert devboxes[0].id == "dev_123"
        mock_client.devboxes.list.assert_called_once()


class TestSnapshotClient:
    """Tests for SnapshotClient class."""

    def test_list(self, mock_client: Mock, snapshot_view: MockSnapshotView) -> None:
        """Test list method."""
        page = SimpleNamespace(disk_snapshots=[snapshot_view])
        mock_client.devboxes.disk_snapshots.list.return_value = page

        client = SnapshotClient(mock_client)
        snapshots = client.list(
            devbox_id="dev_123",
            limit=10,
            starting_after="snap_000",
        )

        assert len(snapshots) == 1
        assert isinstance(snapshots[0], Snapshot)
        assert snapshots[0].id == "snap_123"
        mock_client.devboxes.disk_snapshots.list.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        client = SnapshotClient(mock_client)
        snapshot = client.from_id("snap_123")

        assert isinstance(snapshot, Snapshot)
        assert snapshot.id == "snap_123"


class TestBlueprintClient:
    """Tests for BlueprintClient class."""

    def test_create(self, mock_client: Mock, blueprint_view: MockBlueprintView) -> None:
        """Test create method."""
        mock_client.blueprints.create_and_await_build_complete.return_value = blueprint_view

        client = BlueprintClient(mock_client)
        blueprint = client.create(
            name="test-blueprint",
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(blueprint, Blueprint)
        assert blueprint.id == "bp_123"
        mock_client.blueprints.create_and_await_build_complete.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        client = BlueprintClient(mock_client)
        blueprint = client.from_id("bp_123")

        assert isinstance(blueprint, Blueprint)
        assert blueprint.id == "bp_123"

    def test_list(self, mock_client: Mock, blueprint_view: MockBlueprintView) -> None:
        """Test list method."""
        page = SimpleNamespace(blueprints=[blueprint_view])
        mock_client.blueprints.list.return_value = page

        client = BlueprintClient(mock_client)
        blueprints = client.list(
            limit=10,
            name="test",
            starting_after="bp_000",
        )

        assert len(blueprints) == 1
        assert isinstance(blueprints[0], Blueprint)
        assert blueprints[0].id == "bp_123"
        mock_client.blueprints.list.assert_called_once()


class TestStorageObjectClient:
    """Tests for StorageObjectClient class."""

    def test_create(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test create method."""
        mock_client.objects.create.return_value = object_view

        client = StorageObjectClient(mock_client)
        obj = client.create("test.txt", content_type="text", metadata={"key": "value"})

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url == "https://upload.example.com/obj_123"
        mock_client.objects.create.assert_called_once()

    def test_create_auto_detect_content_type(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test create auto-detects content type."""
        mock_client.objects.create.return_value = object_view

        client = StorageObjectClient(mock_client)
        obj = client.create("test.txt")

        assert isinstance(obj, StorageObject)
        # Should detect "text" from .txt extension
        call_kwargs = mock_client.objects.create.call_args[1]
        assert call_kwargs["content_type"] == "text"

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        client = StorageObjectClient(mock_client)
        obj = client.from_id("obj_123")

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url is None

    def test_list(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test list method."""
        page = SimpleNamespace(objects=[object_view])
        mock_client.objects.list.return_value = page

        client = StorageObjectClient(mock_client)
        objects = client.list(
            content_type="text",
            limit=10,
            name="test",
            search="query",
            starting_after="obj_000",
            state="ready",
        )

        assert len(objects) == 1
        assert isinstance(objects[0], StorageObject)
        assert objects[0].id == "obj_123"
        mock_client.objects.list.assert_called_once()

    def test_upload_from_file(self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path) -> None:
        """Test upload_from_file method."""
        mock_client.objects.create.return_value = object_view

        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test content")

        with patch("httpx.put") as mock_put:
            mock_response = create_mock_httpx_response()
            mock_put.return_value = mock_response

            client = StorageObjectClient(mock_client)
            obj = client.upload_from_file(temp_file, name="test.txt")

            assert isinstance(obj, StorageObject)
            assert obj.id == "obj_123"
            mock_client.objects.create.assert_called_once()
            mock_client.objects.complete.assert_called_once()
            mock_put.assert_called_once()

    def test_upload_from_text(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test upload_from_text method."""
        mock_client.objects.create.return_value = object_view

        with patch("httpx.put") as mock_put:
            mock_response = create_mock_httpx_response()
            mock_put.return_value = mock_response

            client = StorageObjectClient(mock_client)
            obj = client.upload_from_text("test content", "test.txt", metadata={"key": "value"})

            assert isinstance(obj, StorageObject)
            assert obj.id == "obj_123"
            mock_client.objects.create.assert_called_once()
            call_kwargs = mock_client.objects.create.call_args[1]
            assert call_kwargs["content_type"] == "text"
            assert call_kwargs["metadata"] == {"key": "value"}
            mock_client.objects.complete.assert_called_once()

    def test_upload_from_bytes(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test upload_from_bytes method."""
        mock_client.objects.create.return_value = object_view

        with patch("httpx.put") as mock_put:
            mock_response = create_mock_httpx_response()
            mock_put.return_value = mock_response

            client = StorageObjectClient(mock_client)
            obj = client.upload_from_bytes(b"test content", "test.bin", content_type="binary")

            assert isinstance(obj, StorageObject)
            assert obj.id == "obj_123"
            mock_client.objects.create.assert_called_once()
            call_kwargs = mock_client.objects.create.call_args[1]
            assert call_kwargs["content_type"] == "binary"
            mock_client.objects.complete.assert_called_once()


class TestRunloopSDK:
    """Tests for RunloopSDK class."""

    def test_init(self) -> None:
        """Test RunloopSDK initialization."""
        sdk = RunloopSDK(bearer_token="test-token")
        assert sdk.api is not None
        assert isinstance(sdk.devbox, DevboxClient)
        assert isinstance(sdk.snapshot, SnapshotClient)
        assert isinstance(sdk.blueprint, BlueprintClient)
        assert isinstance(sdk.storage_object, StorageObjectClient)

    def test_init_with_max_retries(self) -> None:
        """Test RunloopSDK initialization with max_retries."""
        sdk = RunloopSDK(bearer_token="test-token", max_retries=3)
        assert sdk.api is not None

    def test_close(self) -> None:
        """Test close method."""
        sdk = RunloopSDK(bearer_token="test-token")
        # Verify close doesn't raise
        sdk.close()

    def test_context_manager(self) -> None:
        """Test context manager behavior."""
        with RunloopSDK(bearer_token="test-token") as sdk:
            assert sdk.api is not None
        # Verify context manager properly closes (implementation detail of context manager protocol)

    def test_api_property(self) -> None:
        """Test api property access."""
        sdk = RunloopSDK(bearer_token="test-token")
        assert sdk.api is not None
        assert hasattr(sdk.api, "devboxes")
        assert hasattr(sdk.api, "blueprints")
        assert hasattr(sdk.api, "objects")
