"""Comprehensive tests for async client classes."""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import (
    MockDevboxView,
    MockObjectView,
    MockSnapshotView,
    MockBlueprintView,
    create_mock_httpx_response,
)
from runloop_api_client.sdk import AsyncDevbox, AsyncSnapshot, AsyncBlueprint, AsyncStorageObject
from runloop_api_client.sdk.async_ import (
    AsyncDevboxOps,
    AsyncRunloopSDK,
    AsyncSnapshotOps,
    AsyncBlueprintOps,
    AsyncStorageObjectOps,
)
from runloop_api_client.lib.polling import PollingConfig


class TestAsyncDevboxClient:
    """Tests for AsyncDevboxClient class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        client = AsyncDevboxOps(mock_async_client)
        devbox = await client.create(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(devbox, AsyncDevbox)
        assert devbox.id == "dev_123"
        mock_async_client.devboxes.create_and_await_running.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_from_blueprint_id(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_id method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        client = AsyncDevboxOps(mock_async_client)
        devbox = await client.create_from_blueprint_id(
            "bp_123",
            name="test-devbox",
        )

        assert isinstance(devbox, AsyncDevbox)
        call_kwargs = mock_async_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_id"] == "bp_123"

    @pytest.mark.asyncio
    async def test_create_from_blueprint_name(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_name method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        client = AsyncDevboxOps(mock_async_client)
        devbox = await client.create_from_blueprint_name(
            "my-blueprint",
            name="test-devbox",
        )

        assert isinstance(devbox, AsyncDevbox)
        call_kwargs = mock_async_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_name"] == "my-blueprint"

    @pytest.mark.asyncio
    async def test_create_from_snapshot(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create_from_snapshot method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        client = AsyncDevboxOps(mock_async_client)
        devbox = await client.create_from_snapshot(
            "snap_123",
            name="test-devbox",
        )

        assert isinstance(devbox, AsyncDevbox)
        call_kwargs = mock_async_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["snapshot_id"] == "snap_123"

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        client = AsyncDevboxOps(mock_async_client)
        devbox = client.from_id("dev_123")

        assert isinstance(devbox, AsyncDevbox)
        assert devbox.id == "dev_123"
        # Verify from_id does not wait for running status
        if hasattr(mock_async_client.devboxes, "await_running"):
            assert not mock_async_client.devboxes.await_running.called

    @pytest.mark.asyncio
    async def test_list(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test list method."""
        page = SimpleNamespace(devboxes=[devbox_view])
        mock_async_client.devboxes.list = AsyncMock(return_value=page)

        client = AsyncDevboxOps(mock_async_client)
        devboxes = await client.list(
            limit=10,
            status="running",
            starting_after="dev_000",
        )

        assert len(devboxes) == 1
        assert isinstance(devboxes[0], AsyncDevbox)
        assert devboxes[0].id == "dev_123"
        mock_async_client.devboxes.list.assert_called_once()


class TestAsyncSnapshotClient:
    """Tests for AsyncSnapshotClient class."""

    @pytest.mark.asyncio
    async def test_list(self, mock_async_client: AsyncMock, snapshot_view: MockSnapshotView) -> None:
        """Test list method."""
        page = SimpleNamespace(snapshots=[snapshot_view])
        mock_async_client.devboxes.disk_snapshots.list = AsyncMock(return_value=page)

        client = AsyncSnapshotOps(mock_async_client)
        snapshots = await client.list(
            devbox_id="dev_123",
            limit=10,
            starting_after="snap_000",
        )

        assert len(snapshots) == 1
        assert isinstance(snapshots[0], AsyncSnapshot)
        assert snapshots[0].id == "snap_123"
        mock_async_client.devboxes.disk_snapshots.list.assert_called_once()

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        client = AsyncSnapshotOps(mock_async_client)
        snapshot = client.from_id("snap_123")

        assert isinstance(snapshot, AsyncSnapshot)
        assert snapshot.id == "snap_123"


class TestAsyncBlueprintClient:
    """Tests for AsyncBlueprintClient class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, blueprint_view: MockBlueprintView) -> None:
        """Test create method."""
        mock_async_client.blueprints.create_and_await_build_complete = AsyncMock(return_value=blueprint_view)

        client = AsyncBlueprintOps(mock_async_client)
        blueprint = await client.create(
            name="test-blueprint",
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(blueprint, AsyncBlueprint)
        assert blueprint.id == "bp_123"
        mock_async_client.blueprints.create_and_await_build_complete.assert_called_once()

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        client = AsyncBlueprintOps(mock_async_client)
        blueprint = client.from_id("bp_123")

        assert isinstance(blueprint, AsyncBlueprint)
        assert blueprint.id == "bp_123"

    @pytest.mark.asyncio
    async def test_list(self, mock_async_client: AsyncMock, blueprint_view: MockBlueprintView) -> None:
        """Test list method."""
        page = SimpleNamespace(blueprints=[blueprint_view])
        mock_async_client.blueprints.list = AsyncMock(return_value=page)

        client = AsyncBlueprintOps(mock_async_client)
        blueprints = await client.list(
            limit=10,
            name="test",
            starting_after="bp_000",
        )

        assert len(blueprints) == 1
        assert isinstance(blueprints[0], AsyncBlueprint)
        assert blueprints[0].id == "bp_123"
        mock_async_client.blueprints.list.assert_called_once()


class TestAsyncStorageObjectClient:
    """Tests for AsyncStorageObjectClient class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test create method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)

        client = AsyncStorageObjectOps(mock_async_client)
        obj = await client.create(name="test.txt", content_type="text", metadata={"key": "value"})

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url == "https://upload.example.com/obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="test.txt",
            content_type="text",
            metadata={"key": "value"},
        )

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        client = AsyncStorageObjectOps(mock_async_client)
        obj = client.from_id("obj_123")

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url is None

    @pytest.mark.asyncio
    async def test_list(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test list method."""
        page = SimpleNamespace(objects=[object_view])
        mock_async_client.objects.list = AsyncMock(return_value=page)

        client = AsyncStorageObjectOps(mock_async_client)
        objects = await client.list(
            content_type="text",
            limit=10,
            name="test",
            search="query",
            starting_after="obj_000",
            state="ready",
        )

        assert len(objects) == 1
        assert isinstance(objects[0], AsyncStorageObject)
        assert objects[0].id == "obj_123"
        mock_async_client.objects.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_file(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_file method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test content")

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        client = AsyncStorageObjectOps(mock_async_client)
        obj = await client.upload_from_file(temp_file, name="test.txt")

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once()
        mock_async_client.objects.complete.assert_awaited_once()
        http_client.put.assert_awaited_once_with(object_view.upload_url, content=b"test content")

    @pytest.mark.asyncio
    async def test_upload_from_text(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test upload_from_text method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        client = AsyncStorageObjectOps(mock_async_client)
        obj = await client.upload_from_text("test content", "test.txt", metadata={"key": "value"})

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="test.txt",
            content_type="text",
            metadata={"key": "value"},
        )
        http_client.put.assert_awaited_once_with(object_view.upload_url, content="test content")
        mock_async_client.objects.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_bytes(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test upload_from_bytes method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        client = AsyncStorageObjectOps(mock_async_client)
        obj = await client.upload_from_bytes(b"test content", "test.bin", content_type="binary")

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="test.bin",
            content_type="binary",
            metadata=None,
        )
        http_client.put.assert_awaited_once_with(object_view.upload_url, content=b"test content")
        mock_async_client.objects.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_file_missing_path(self, mock_async_client: AsyncMock, tmp_path: Path) -> None:
        """upload_from_file should raise when file cannot be read."""
        client = AsyncStorageObjectOps(mock_async_client)
        missing_file = tmp_path / "missing.txt"

        with pytest.raises(OSError, match="Failed to read file"):
            await client.upload_from_file(missing_file)


class TestAsyncRunloopSDK:
    """Tests for AsyncRunloopSDK class."""

    def test_init(self) -> None:
        """Test AsyncRunloopSDK initialization."""
        sdk = AsyncRunloopSDK(bearer_token="test-token")
        assert sdk.api is not None
        assert isinstance(sdk.devbox, AsyncDevboxOps)
        assert isinstance(sdk.snapshot, AsyncSnapshotOps)
        assert isinstance(sdk.blueprint, AsyncBlueprintOps)
        assert isinstance(sdk.storage_object, AsyncStorageObjectOps)

    @pytest.mark.asyncio
    async def test_aclose(self) -> None:
        """Test aclose method."""
        sdk = AsyncRunloopSDK(bearer_token="test-token")
        # Verify aclose doesn't raise
        await sdk.aclose()

    @pytest.mark.asyncio
    async def test_context_manager(self) -> None:
        """Test context manager behavior."""
        async with AsyncRunloopSDK(bearer_token="test-token") as sdk:
            assert sdk.api is not None
        # Verify context manager properly closes (implementation detail of context manager protocol)

    def test_api_property(self) -> None:
        """Test api property access."""
        sdk = AsyncRunloopSDK(bearer_token="test-token")
        assert sdk.api is not None
        assert hasattr(sdk.api, "devboxes")
        assert hasattr(sdk.api, "blueprints")
        assert hasattr(sdk.api, "objects")
