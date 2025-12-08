"""Comprehensive tests for async client classes."""

from __future__ import annotations

import io
import tarfile
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import (
    MockAgentView,
    MockDevboxView,
    MockObjectView,
    MockScorerView,
    MockScenarioView,
    MockSnapshotView,
    MockBlueprintView,
    create_mock_httpx_response,
)
from runloop_api_client.sdk import (
    AsyncAgent,
    AsyncDevbox,
    AsyncScorer,
    AsyncSnapshot,
    AsyncBlueprint,
    AsyncStorageObject,
)
from runloop_api_client.sdk.async_ import (
    AsyncAgentOps,
    AsyncDevboxOps,
    AsyncScorerOps,
    AsyncRunloopSDK,
    AsyncSnapshotOps,
    AsyncBlueprintOps,
    AsyncStorageObjectOps,
)
from runloop_api_client.lib.polling import PollingConfig


class TestAsyncDevboxOps:
    """Tests for AsyncDevboxOps class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        ops = AsyncDevboxOps(mock_async_client)
        devbox = await ops.create(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(devbox, AsyncDevbox)
        assert devbox.id == "dev_123"
        mock_async_client.devboxes.create_and_await_running.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_from_blueprint_id(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_id method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        ops = AsyncDevboxOps(mock_async_client)
        devbox = await ops.create_from_blueprint_id(
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

        ops = AsyncDevboxOps(mock_async_client)
        devbox = await ops.create_from_blueprint_name(
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

        ops = AsyncDevboxOps(mock_async_client)
        devbox = await ops.create_from_snapshot(
            "snap_123",
            name="test-devbox",
        )

        assert isinstance(devbox, AsyncDevbox)
        call_kwargs = mock_async_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["snapshot_id"] == "snap_123"

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        ops = AsyncDevboxOps(mock_async_client)
        devbox = ops.from_id("dev_123")

        assert isinstance(devbox, AsyncDevbox)
        assert devbox.id == "dev_123"
        # Verify from_id does not wait for running status
        if hasattr(mock_async_client.devboxes, "await_running"):
            assert not mock_async_client.devboxes.await_running.called

    @pytest.mark.asyncio
    async def test_list_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(devboxes=[])
        mock_async_client.devboxes.list = AsyncMock(return_value=page)

        ops = AsyncDevboxOps(mock_async_client)
        devboxes = await ops.list(limit=10, status="running")

        assert len(devboxes) == 0
        mock_async_client.devboxes.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_single(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(devboxes=[devbox_view])
        mock_async_client.devboxes.list = AsyncMock(return_value=page)

        ops = AsyncDevboxOps(mock_async_client)
        devboxes = await ops.list(
            limit=10,
            status="running",
            starting_after="dev_000",
        )

        assert len(devboxes) == 1
        assert isinstance(devboxes[0], AsyncDevbox)
        assert devboxes[0].id == "dev_123"
        mock_async_client.devboxes.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list method with multiple results."""
        devbox_view1 = MockDevboxView(id="dev_001", name="devbox-1")
        devbox_view2 = MockDevboxView(id="dev_002", name="devbox-2")
        page = SimpleNamespace(devboxes=[devbox_view1, devbox_view2])
        mock_async_client.devboxes.list = AsyncMock(return_value=page)

        ops = AsyncDevboxOps(mock_async_client)
        devboxes = await ops.list(limit=10, status="running")

        assert len(devboxes) == 2
        assert isinstance(devboxes[0], AsyncDevbox)
        assert isinstance(devboxes[1], AsyncDevbox)
        assert devboxes[0].id == "dev_001"
        assert devboxes[1].id == "dev_002"
        mock_async_client.devboxes.list.assert_awaited_once()


class TestAsyncSnapshotOps:
    """Tests for AsyncSnapshotOps class."""

    @pytest.mark.asyncio
    async def test_list_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(snapshots=[])
        mock_async_client.devboxes.disk_snapshots.list = AsyncMock(return_value=page)

        ops = AsyncSnapshotOps(mock_async_client)
        snapshots = await ops.list(devbox_id="dev_123", limit=10)

        assert len(snapshots) == 0
        mock_async_client.devboxes.disk_snapshots.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_single(self, mock_async_client: AsyncMock, snapshot_view: MockSnapshotView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(snapshots=[snapshot_view])
        mock_async_client.devboxes.disk_snapshots.list = AsyncMock(return_value=page)

        ops = AsyncSnapshotOps(mock_async_client)
        snapshots = await ops.list(
            devbox_id="dev_123",
            limit=10,
            starting_after="snap_000",
        )

        assert len(snapshots) == 1
        assert isinstance(snapshots[0], AsyncSnapshot)
        assert snapshots[0].id == "snap_123"
        mock_async_client.devboxes.disk_snapshots.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list method with multiple results."""
        snapshot_view1 = MockSnapshotView(id="snap_001", name="snapshot-1")
        snapshot_view2 = MockSnapshotView(id="snap_002", name="snapshot-2")
        page = SimpleNamespace(snapshots=[snapshot_view1, snapshot_view2])
        mock_async_client.devboxes.disk_snapshots.list = AsyncMock(return_value=page)

        ops = AsyncSnapshotOps(mock_async_client)
        snapshots = await ops.list(devbox_id="dev_123", limit=10)

        assert len(snapshots) == 2
        assert isinstance(snapshots[0], AsyncSnapshot)
        assert isinstance(snapshots[1], AsyncSnapshot)
        assert snapshots[0].id == "snap_001"
        assert snapshots[1].id == "snap_002"
        mock_async_client.devboxes.disk_snapshots.list.assert_awaited_once()

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        ops = AsyncSnapshotOps(mock_async_client)
        snapshot = ops.from_id("snap_123")

        assert isinstance(snapshot, AsyncSnapshot)
        assert snapshot.id == "snap_123"


class TestAsyncBlueprintOps:
    """Tests for AsyncBlueprintOps class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, blueprint_view: MockBlueprintView) -> None:
        """Test create method."""
        mock_async_client.blueprints.create_and_await_build_complete = AsyncMock(return_value=blueprint_view)

        ops = AsyncBlueprintOps(mock_async_client)
        blueprint = await ops.create(
            name="test-blueprint",
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(blueprint, AsyncBlueprint)
        assert blueprint.id == "bp_123"
        mock_async_client.blueprints.create_and_await_build_complete.assert_awaited_once()

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        ops = AsyncBlueprintOps(mock_async_client)
        blueprint = ops.from_id("bp_123")

        assert isinstance(blueprint, AsyncBlueprint)
        assert blueprint.id == "bp_123"

    @pytest.mark.asyncio
    async def test_list_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(blueprints=[])
        mock_async_client.blueprints.list = AsyncMock(return_value=page)

        ops = AsyncBlueprintOps(mock_async_client)
        blueprints = await ops.list(limit=10)

        assert len(blueprints) == 0
        mock_async_client.blueprints.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_single(self, mock_async_client: AsyncMock, blueprint_view: MockBlueprintView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(blueprints=[blueprint_view])
        mock_async_client.blueprints.list = AsyncMock(return_value=page)

        ops = AsyncBlueprintOps(mock_async_client)
        blueprints = await ops.list(
            limit=10,
            name="test",
            starting_after="bp_000",
        )

        assert len(blueprints) == 1
        assert isinstance(blueprints[0], AsyncBlueprint)
        assert blueprints[0].id == "bp_123"
        mock_async_client.blueprints.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list method with multiple results."""
        blueprint_view1 = MockBlueprintView(id="bp_001", name="blueprint-1")
        blueprint_view2 = MockBlueprintView(id="bp_002", name="blueprint-2")
        page = SimpleNamespace(blueprints=[blueprint_view1, blueprint_view2])
        mock_async_client.blueprints.list = AsyncMock(return_value=page)

        ops = AsyncBlueprintOps(mock_async_client)
        blueprints = await ops.list(limit=10)

        assert len(blueprints) == 2
        assert isinstance(blueprints[0], AsyncBlueprint)
        assert isinstance(blueprints[1], AsyncBlueprint)
        assert blueprints[0].id == "bp_001"
        assert blueprints[1].id == "bp_002"
        mock_async_client.blueprints.list.assert_awaited_once()


class TestAsyncStorageObjectOps:
    """Tests for AsyncStorageObjectOps class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test create method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.create(name="test.txt", content_type="text", metadata={"key": "value"})

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
        ops = AsyncStorageObjectOps(mock_async_client)
        obj = ops.from_id("obj_123")

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url is None

    @pytest.mark.asyncio
    async def test_list_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(objects=[])
        mock_async_client.objects.list = AsyncMock(return_value=page)

        ops = AsyncStorageObjectOps(mock_async_client)
        objects = await ops.list(limit=10)

        assert len(objects) == 0
        mock_async_client.objects.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_single(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(objects=[object_view])
        mock_async_client.objects.list = AsyncMock(return_value=page)

        ops = AsyncStorageObjectOps(mock_async_client)
        objects = await ops.list(
            content_type="text",
            limit=10,
            name="test",
            search="query",
            starting_after="obj_000",
            state="READ_ONLY",
        )

        assert len(objects) == 1
        assert isinstance(objects[0], AsyncStorageObject)
        assert objects[0].id == "obj_123"
        mock_async_client.objects.list.assert_awaited_once_with(
            content_type="text",
            limit=10,
            name="test",
            search="query",
            starting_after="obj_000",
            state="READ_ONLY",
        )

    @pytest.mark.asyncio
    async def test_list_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list method with multiple results."""
        object_view1 = MockObjectView(id="obj_001", name="object-1")
        object_view2 = MockObjectView(id="obj_002", name="object-2")
        page = SimpleNamespace(objects=[object_view1, object_view2])
        mock_async_client.objects.list = AsyncMock(return_value=page)

        ops = AsyncStorageObjectOps(mock_async_client)
        objects = await ops.list(limit=10)

        assert len(objects) == 2
        assert isinstance(objects[0], AsyncStorageObject)
        assert isinstance(objects[1], AsyncStorageObject)
        assert objects[0].id == "obj_001"
        assert objects[1].id == "obj_002"
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

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_file(temp_file, name="test.txt")

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="test.txt",
            content_type="text",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_awaited_once_with(object_view.upload_url, content=b"test content")
        mock_async_client.objects.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_text(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """Test upload_from_text method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_text("test content", name="test.txt", metadata={"key": "value"})

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="test.txt",
            content_type="text",
            metadata={"key": "value"},
            ttl_ms=None,
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

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_bytes(b"test content", name="test.bin", content_type="binary")

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="test.bin",
            content_type="binary",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_awaited_once_with(object_view.upload_url, content=b"test content")
        mock_async_client.objects.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_file_missing_path(self, mock_async_client: AsyncMock, tmp_path: Path) -> None:
        """upload_from_file should raise when file cannot be read."""
        ops = AsyncStorageObjectOps(mock_async_client)
        missing_file = tmp_path / "missing.txt"

        with pytest.raises(OSError, match="Failed to read file"):
            await ops.upload_from_file(missing_file)

    def test_as_build_context(self, mock_async_client: AsyncMock, object_view: MockObjectView) -> None:
        """as_build_context should return the correct dict shape."""
        obj = AsyncStorageObject(mock_async_client, object_view.id, upload_url=None)

        assert obj.as_build_context() == {
            "object_id": object_view.id,
            "type": "object",
        }

    @pytest.mark.asyncio
    async def test_upload_from_dir(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir method."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        # Create a temporary directory with some files
        test_dir = tmp_path / "test_directory"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")
        subdir = test_dir / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("content3")

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_dir(test_dir, name="archive.tar.gz", metadata={"key": "value"})

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="archive.tar.gz",
            content_type="tgz",
            metadata={"key": "value"},
            ttl_ms=None,
        )
        # Verify that put was called with tarball content
        http_client.put.assert_awaited_once()
        call_args = http_client.put.call_args
        assert call_args[0][0] == object_view.upload_url

        # Verify it's a valid gzipped tarball
        uploaded_content = call_args[1]["content"]
        with tarfile.open(fileobj=io.BytesIO(uploaded_content), mode="r:gz") as tar:
            members = tar.getmembers()
            member_names = [m.name for m in members]
            # Should contain our test files (may include directory entries)
            assert any("file1.txt" in name for name in member_names)
            assert any("file2.txt" in name for name in member_names)
            assert any("file3.txt" in name for name in member_names)

        mock_async_client.objects.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_dir_with_inline_ignore_patterns(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """upload_from_dir should respect inline ignore patterns."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        test_dir = tmp_path / "ctx"
        test_dir.mkdir()
        (test_dir / "keep.txt").write_text("keep", encoding="utf-8")
        (test_dir / "ignore.log").write_text("ignore", encoding="utf-8")
        build_dir = test_dir / "build"
        build_dir.mkdir()
        (build_dir / "ignored.txt").write_text("ignored", encoding="utf-8")

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        client = AsyncStorageObjectOps(mock_async_client)

        # Tar filter: drop logs and anything under build/
        def ignore_logs_and_build(ti: tarfile.TarInfo) -> tarfile.TarInfo | None:
            if ti.name.endswith(".log") or ti.name.startswith("build/"):
                return None
            return ti

        obj = await client.upload_from_dir(test_dir, ignore=ignore_logs_and_build)

        assert isinstance(obj, AsyncStorageObject)
        uploaded_content = http_client.put.call_args[1]["content"]

        with tarfile.open(fileobj=io.BytesIO(uploaded_content), mode="r:gz") as tar:
            names = {m.name for m in tar.getmembers()}

        assert "keep.txt" in names
        assert "ignore.log" not in names
        assert not any(name.startswith("build/") for name in names)

    @pytest.mark.asyncio
    async def test_upload_from_dir_default_name(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir uses directory name by default."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        test_dir = tmp_path / "my_folder"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_dir(test_dir)

        assert isinstance(obj, AsyncStorageObject)
        # Name should be directory name + .tar.gz
        mock_async_client.objects.create.assert_awaited_once_with(
            name="my_folder.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=None,
        )

    @pytest.mark.asyncio
    async def test_upload_from_dir_with_ttl(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir with TTL."""
        from datetime import timedelta

        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        test_dir = tmp_path / "temp_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("temporary content")

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_dir(test_dir, ttl=timedelta(hours=2))

        assert isinstance(obj, AsyncStorageObject)
        mock_async_client.objects.create.assert_awaited_once_with(
            name="temp_dir.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=7200000,  # 2 hours = 7200 seconds = 7200000 milliseconds
        )

    @pytest.mark.asyncio
    async def test_upload_from_dir_empty_directory(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir with empty directory."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        test_dir = tmp_path / "empty_dir"
        test_dir.mkdir()

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        ops = AsyncStorageObjectOps(mock_async_client)
        obj = await ops.upload_from_dir(test_dir)

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="empty_dir.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_awaited_once()
        mock_async_client.objects.complete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_upload_from_dir_with_string_path(
        self, mock_async_client: AsyncMock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir with string path instead of Path object."""
        mock_async_client.objects.create = AsyncMock(return_value=object_view)
        mock_async_client.objects.complete = AsyncMock(return_value=object_view)

        test_dir = tmp_path / "string_path_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        http_client = AsyncMock()
        mock_response = create_mock_httpx_response()
        http_client.put = AsyncMock(return_value=mock_response)
        mock_async_client._client = http_client

        ops = AsyncStorageObjectOps(mock_async_client)
        # Pass string path instead of Path object
        obj = await ops.upload_from_dir(str(test_dir))

        assert isinstance(obj, AsyncStorageObject)
        assert obj.id == "obj_123"
        mock_async_client.objects.create.assert_awaited_once_with(
            name="string_path_dir.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_awaited_once()
        mock_async_client.objects.complete.assert_awaited_once()


class TestAsyncScorerOps:
    """Tests for AsyncScorerOps class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, scorer_view: MockScorerView) -> None:
        """Test create method."""
        mock_async_client.scenarios.scorers.create = AsyncMock(return_value=scorer_view)

        ops = AsyncScorerOps(mock_async_client)
        scorer = await ops.create(
            bash_script="echo 'score=1.0'",
            type="test_scorer",
        )

        assert isinstance(scorer, AsyncScorer)
        assert scorer.id == "scorer_123"
        mock_async_client.scenarios.scorers.create.assert_awaited_once()

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        ops = AsyncScorerOps(mock_async_client)
        scorer = ops.from_id("scorer_123")

        assert isinstance(scorer, AsyncScorer)
        assert scorer.id == "scorer_123"

    @pytest.mark.asyncio
    async def test_list_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list method with empty results."""

        async def async_iter():
            return
            yield  # Make this a generator

        mock_async_client.scenarios.scorers.list = AsyncMock(return_value=async_iter())

        ops = AsyncScorerOps(mock_async_client)
        scorers = await ops.list(limit=10)

        assert len(scorers) == 0
        mock_async_client.scenarios.scorers.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_single(self, mock_async_client: AsyncMock, scorer_view: MockScorerView) -> None:
        """Test list method with single result."""

        async def async_iter():
            yield scorer_view

        mock_async_client.scenarios.scorers.list = AsyncMock(return_value=async_iter())

        ops = AsyncScorerOps(mock_async_client)
        scorers = await ops.list(
            limit=10,
            starting_after="scorer_000",
        )

        assert len(scorers) == 1
        assert isinstance(scorers[0], AsyncScorer)
        assert scorers[0].id == "scorer_123"
        mock_async_client.scenarios.scorers.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list method with multiple results."""
        scorer_view1 = MockScorerView(id="scorer_001", type="scorer-1")
        scorer_view2 = MockScorerView(id="scorer_002", type="scorer-2")

        async def async_iter():
            yield scorer_view1
            yield scorer_view2

        mock_async_client.scenarios.scorers.list = AsyncMock(return_value=async_iter())

        ops = AsyncScorerOps(mock_async_client)
        scorers = await ops.list(limit=10)

        assert len(scorers) == 2
        assert isinstance(scorers[0], AsyncScorer)
        assert isinstance(scorers[1], AsyncScorer)
        assert scorers[0].id == "scorer_001"
        assert scorers[1].id == "scorer_002"
        mock_async_client.scenarios.scorers.list.assert_awaited_once()


class TestAsyncAgentClient:
    """Tests for AsyncAgentClient class."""

    @pytest.mark.asyncio
    async def test_create(self, mock_async_client: AsyncMock, agent_view: MockAgentView) -> None:
        """Test create method."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create(
            name="test-agent",
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_called_once()

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        client = AsyncAgentOps(mock_async_client)
        agent = client.from_id("agent_123")

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"

    @pytest.mark.asyncio
    async def test_list(self, mock_async_client: AsyncMock) -> None:
        """Test list method."""
        # Create three agent views with different data
        agent_view_1 = MockAgentView(
            id="agent_001",
            name="first-agent",
            create_time_ms=1234567890000,
            is_public=False,
            source=None,
        )
        agent_view_2 = MockAgentView(
            id="agent_002",
            name="second-agent",
            create_time_ms=1234567891000,
            is_public=True,
            source={"type": "git", "git": {"repository": "https://github.com/example/repo"}},
        )
        agent_view_3 = MockAgentView(
            id="agent_003",
            name="third-agent",
            create_time_ms=1234567892000,
            is_public=False,
            source={"type": "npm", "npm": {"package_name": "example-package"}},
        )

        page = SimpleNamespace(agents=[agent_view_1, agent_view_2, agent_view_3])
        mock_async_client.agents.list = AsyncMock(return_value=page)

        # Mock retrieve to return the corresponding agent_view when called
        async def mock_retrieve(agent_id: str):
            if agent_id == "agent_001":
                return agent_view_1
            elif agent_id == "agent_002":
                return agent_view_2
            elif agent_id == "agent_003":
                return agent_view_3
            return None

        mock_async_client.agents.retrieve = AsyncMock(side_effect=mock_retrieve)

        client = AsyncAgentOps(mock_async_client)
        agents = await client.list(
            limit=10,
            starting_after="agent_000",
        )

        # Verify we got three agents
        assert len(agents) == 3
        assert all(isinstance(agent, AsyncAgent) for agent in agents)

        # Verify the agent IDs
        assert agents[0].id == "agent_001"
        assert agents[1].id == "agent_002"
        assert agents[2].id == "agent_003"

        # Test that get_info() retrieves the AgentView for the first agent
        info = await agents[0].get_info()
        assert info.id == "agent_001"
        assert info.name == "first-agent"
        assert info.create_time_ms == 1234567890000
        assert info.is_public is False
        assert info.source is None

        # Test that get_info() retrieves the AgentView for the second agent
        info = await agents[1].get_info()
        assert info.id == "agent_002"
        assert info.name == "second-agent"
        assert info.create_time_ms == 1234567891000
        assert info.is_public is True
        assert info.source == {"type": "git", "git": {"repository": "https://github.com/example/repo"}}

        # Test that get_info() retrieves the AgentView for the third agent
        info = await agents[2].get_info()
        assert info.id == "agent_003"
        assert info.name == "third-agent"
        assert info.create_time_ms == 1234567892000
        assert info.is_public is False
        assert info.source == {"type": "npm", "npm": {"package_name": "example-package"}}

        # Verify that agents.retrieve was called three times (once for each get_info)
        assert mock_async_client.agents.retrieve.call_count == 3

        mock_async_client.agents.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_from_npm(self, mock_async_client: AsyncMock, agent_view: MockAgentView) -> None:
        """Test create_from_npm factory method."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_npm(
            name="test-agent",
            package_name="@runloop/example-agent",
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/example-agent",
                },
            },
            name="test-agent",
        )

    @pytest.mark.asyncio
    async def test_create_from_npm_with_all_options(
        self, mock_async_client: AsyncMock, agent_view: MockAgentView
    ) -> None:
        """Test create_from_npm factory method with all optional parameters."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_npm(
            name="test-agent",
            package_name="@runloop/example-agent",
            npm_version="1.2.3",
            registry_url="https://registry.example.com",
            agent_setup=["npm install", "npm run setup"],
            extra_headers={"X-Custom": "header"},
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/example-agent",
                    "npm_version": "1.2.3",
                    "registry_url": "https://registry.example.com",
                    "agent_setup": ["npm install", "npm run setup"],
                },
            },
            name="test-agent",
            extra_headers={"X-Custom": "header"},
        )

    @pytest.mark.asyncio
    async def test_create_from_npm_raises_when_source_provided(self, mock_async_client: AsyncMock) -> None:
        """Test create_from_npm raises ValueError when source is provided in params."""
        client = AsyncAgentOps(mock_async_client)

        with pytest.raises(ValueError, match="Cannot specify 'source' when using create_from_npm"):
            await client.create_from_npm(
                name="test-agent",
                package_name="@runloop/example-agent",
                source={"type": "git", "git": {"repository": "https://github.com/example/repo"}},
            )

    @pytest.mark.asyncio
    async def test_create_from_pip(self, mock_async_client: AsyncMock, agent_view: MockAgentView) -> None:
        """Test create_from_pip factory method."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_pip(
            name="test-agent",
            package_name="runloop-example-agent",
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "pip",
                "pip": {
                    "package_name": "runloop-example-agent",
                },
            },
            name="test-agent",
        )

    @pytest.mark.asyncio
    async def test_create_from_pip_with_all_options(
        self, mock_async_client: AsyncMock, agent_view: MockAgentView
    ) -> None:
        """Test create_from_pip factory method with all optional parameters."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_pip(
            name="test-agent",
            package_name="runloop-example-agent",
            pip_version="1.2.3",
            registry_url="https://pypi.example.com",
            agent_setup=["pip install extra-deps"],
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "pip",
                "pip": {
                    "package_name": "runloop-example-agent",
                    "pip_version": "1.2.3",
                    "registry_url": "https://pypi.example.com",
                    "agent_setup": ["pip install extra-deps"],
                },
            },
            name="test-agent",
        )

    @pytest.mark.asyncio
    async def test_create_from_git(self, mock_async_client: AsyncMock, agent_view: MockAgentView) -> None:
        """Test create_from_git factory method."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_git(
            name="test-agent",
            repository="https://github.com/example/agent-repo",
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "git",
                "git": {
                    "repository": "https://github.com/example/agent-repo",
                },
            },
            name="test-agent",
        )

    @pytest.mark.asyncio
    async def test_create_from_git_with_all_options(
        self, mock_async_client: AsyncMock, agent_view: MockAgentView
    ) -> None:
        """Test create_from_git factory method with all optional parameters."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_git(
            name="test-agent",
            repository="https://github.com/example/agent-repo",
            ref="develop",
            agent_setup=["npm install", "npm run build"],
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "git",
                "git": {
                    "repository": "https://github.com/example/agent-repo",
                    "ref": "develop",
                    "agent_setup": ["npm install", "npm run build"],
                },
            },
            name="test-agent",
        )

    @pytest.mark.asyncio
    async def test_create_from_object(self, mock_async_client: AsyncMock, agent_view: MockAgentView) -> None:
        """Test create_from_object factory method."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_object(
            name="test-agent",
            object_id="obj_123",
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "object",
                "object": {
                    "object_id": "obj_123",
                },
            },
            name="test-agent",
        )

    @pytest.mark.asyncio
    async def test_create_from_object_with_agent_setup(
        self, mock_async_client: AsyncMock, agent_view: MockAgentView
    ) -> None:
        """Test create_from_object factory method with agent_setup."""
        mock_async_client.agents.create = AsyncMock(return_value=agent_view)

        client = AsyncAgentOps(mock_async_client)
        agent = await client.create_from_object(
            name="test-agent",
            object_id="obj_123",
            agent_setup=["chmod +x setup.sh", "./setup.sh"],
        )

        assert isinstance(agent, AsyncAgent)
        assert agent.id == "agent_123"
        mock_async_client.agents.create.assert_awaited_once_with(
            source={
                "type": "object",
                "object": {
                    "object_id": "obj_123",
                    "agent_setup": ["chmod +x setup.sh", "./setup.sh"],
                },
            },
            name="test-agent",
        )


class TestAsyncScenarioOps:
    """Tests for AsyncScenarioOps class."""

    def test_from_id(self, mock_async_client: AsyncMock) -> None:
        """Test from_id method."""
        from runloop_api_client.sdk import AsyncScenario
        from runloop_api_client.sdk.async_ import AsyncScenarioOps

        ops = AsyncScenarioOps(mock_async_client)
        scenario = ops.from_id("scn_123")

        assert isinstance(scenario, AsyncScenario)
        assert scenario.id == "scn_123"

    @pytest.mark.asyncio
    async def test_list_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list method with empty results."""
        from runloop_api_client.sdk.async_ import AsyncScenarioOps

        async def async_iter():
            return
            yield  # Make this a generator

        mock_async_client.scenarios.list = AsyncMock(return_value=async_iter())

        ops = AsyncScenarioOps(mock_async_client)
        scenarios = await ops.list(limit=10)

        assert len(scenarios) == 0
        mock_async_client.scenarios.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_single(self, mock_async_client: AsyncMock, scenario_view: MockScenarioView) -> None:
        """Test list method with single result."""
        from runloop_api_client.sdk import AsyncScenario
        from runloop_api_client.sdk.async_ import AsyncScenarioOps

        async def async_iter():
            yield scenario_view

        mock_async_client.scenarios.list = AsyncMock(return_value=async_iter())

        ops = AsyncScenarioOps(mock_async_client)
        scenarios = await ops.list(limit=10)

        assert len(scenarios) == 1
        assert isinstance(scenarios[0], AsyncScenario)
        assert scenarios[0].id == "scn_123"
        mock_async_client.scenarios.list.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_list_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list method with multiple results."""
        from runloop_api_client.sdk import AsyncScenario
        from runloop_api_client.sdk.async_ import AsyncScenarioOps

        scenario_view1 = MockScenarioView(id="scn_001", name="scenario-1")
        scenario_view2 = MockScenarioView(id="scn_002", name="scenario-2")

        async def async_iter():
            yield scenario_view1
            yield scenario_view2

        mock_async_client.scenarios.list = AsyncMock(return_value=async_iter())

        ops = AsyncScenarioOps(mock_async_client)
        scenarios = await ops.list(limit=10)

        assert len(scenarios) == 2
        assert isinstance(scenarios[0], AsyncScenario)
        assert isinstance(scenarios[1], AsyncScenario)
        assert scenarios[0].id == "scn_001"
        assert scenarios[1].id == "scn_002"
        mock_async_client.scenarios.list.assert_awaited_once()


class TestAsyncRunloopSDK:
    """Tests for AsyncRunloopSDK class."""

    def test_init(self) -> None:
        """Test AsyncRunloopSDK initialization."""
        sdk = AsyncRunloopSDK(bearer_token="test-token")
        assert sdk.api is not None
        assert isinstance(sdk.agent, AsyncAgentOps)
        assert isinstance(sdk.devbox, AsyncDevboxOps)
        assert isinstance(sdk.scorer, AsyncScorerOps)
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
