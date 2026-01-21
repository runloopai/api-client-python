"""Comprehensive tests for sync client classes."""

from __future__ import annotations

import io
import tarfile
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock

import pytest

from tests.sdk.conftest import (
    MockAgentView,
    MockDevboxView,
    MockObjectView,
    MockScorerView,
    MockScenarioView,
    MockSnapshotView,
    MockBenchmarkView,
    MockBlueprintView,
    MockNetworkPolicyView,
    create_mock_httpx_response,
)
from runloop_api_client.sdk import (
    Agent,
    Devbox,
    Scorer,
    AgentOps,
    Scenario,
    Snapshot,
    Benchmark,
    Blueprint,
    DevboxOps,
    ScorerOps,
    RunloopSDK,
    ScenarioOps,
    SnapshotOps,
    BenchmarkOps,
    BlueprintOps,
    NetworkPolicy,
    StorageObject,
    NetworkPolicyOps,
    StorageObjectOps,
)
from runloop_api_client.lib.polling import PollingConfig


class TestDevboxOps:
    """Tests for DevboxOps class."""

    def test_create(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        ops = DevboxOps(mock_client)
        devbox = ops.create(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(devbox, Devbox)
        assert devbox.id == "dbx_123"
        mock_client.devboxes.create_and_await_running.assert_called_once()

    def test_create_from_blueprint_id(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_id method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        ops = DevboxOps(mock_client)
        devbox = ops.create_from_blueprint_id(
            "bpt_123",
            name="test-devbox",
            metadata={"key": "value"},
        )

        assert isinstance(devbox, Devbox)
        assert devbox.id == "dbx_123"
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_id"] == "bpt_123"

    def test_create_from_blueprint_name(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_from_blueprint_name method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        ops = DevboxOps(mock_client)
        devbox = ops.create_from_blueprint_name(
            "my-blueprint",
            name="test-devbox",
        )

        assert isinstance(devbox, Devbox)
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_name"] == "my-blueprint"

    def test_create_from_snapshot(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_from_snapshot method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        ops = DevboxOps(mock_client)
        devbox = ops.create_from_snapshot(
            "snp_123",
            name="test-devbox",
        )

        assert isinstance(devbox, Devbox)
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["snapshot_id"] == "snp_123"

    def test_from_id(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test from_id method waits for running."""
        mock_client.devboxes.await_running.return_value = devbox_view

        ops = DevboxOps(mock_client)
        devbox = ops.from_id("dbx_123")

        assert isinstance(devbox, Devbox)
        assert devbox.id == "dbx_123"
        mock_client.devboxes.await_running.assert_called_once_with("dbx_123")

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(devboxes=[])
        mock_client.devboxes.list.return_value = page

        ops = DevboxOps(mock_client)
        devboxes = ops.list(limit=10, status="running")

        assert len(devboxes) == 0
        mock_client.devboxes.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(devboxes=[devbox_view])
        mock_client.devboxes.list.return_value = page

        ops = DevboxOps(mock_client)
        devboxes = ops.list(
            limit=10,
            status="running",
            starting_after="dev_000",
        )

        assert len(devboxes) == 1
        assert isinstance(devboxes[0], Devbox)
        assert devboxes[0].id == "dbx_123"
        mock_client.devboxes.list.assert_called_once()

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        devbox_view1 = MockDevboxView(id="dev_001", name="devbox-1")
        devbox_view2 = MockDevboxView(id="dev_002", name="devbox-2")
        page = SimpleNamespace(devboxes=[devbox_view1, devbox_view2])
        mock_client.devboxes.list.return_value = page

        ops = DevboxOps(mock_client)
        devboxes = ops.list(limit=10, status="running")

        assert len(devboxes) == 2
        assert isinstance(devboxes[0], Devbox)
        assert isinstance(devboxes[1], Devbox)
        assert devboxes[0].id == "dev_001"
        assert devboxes[1].id == "dev_002"
        mock_client.devboxes.list.assert_called_once()


class TestSnapshotOps:
    """Tests for SnapshotOps class."""

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(snapshots=[])
        mock_client.devboxes.disk_snapshots.list.return_value = page

        ops = SnapshotOps(mock_client)
        snapshots = ops.list(devbox_id="dbx_123", limit=10)

        assert len(snapshots) == 0
        mock_client.devboxes.disk_snapshots.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, snapshot_view: MockSnapshotView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(snapshots=[snapshot_view])
        mock_client.devboxes.disk_snapshots.list.return_value = page

        ops = SnapshotOps(mock_client)
        snapshots = ops.list(
            devbox_id="dbx_123",
            limit=10,
            starting_after="snap_000",
        )

        assert len(snapshots) == 1
        assert isinstance(snapshots[0], Snapshot)
        assert snapshots[0].id == "snp_123"
        mock_client.devboxes.disk_snapshots.list.assert_called_once()

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        snapshot_view1 = MockSnapshotView(id="snap_001", name="snapshot-1")
        snapshot_view2 = MockSnapshotView(id="snap_002", name="snapshot-2")
        page = SimpleNamespace(snapshots=[snapshot_view1, snapshot_view2])
        mock_client.devboxes.disk_snapshots.list.return_value = page

        ops = SnapshotOps(mock_client)
        snapshots = ops.list(devbox_id="dbx_123", limit=10)

        assert len(snapshots) == 2
        assert isinstance(snapshots[0], Snapshot)
        assert isinstance(snapshots[1], Snapshot)
        assert snapshots[0].id == "snap_001"
        assert snapshots[1].id == "snap_002"
        mock_client.devboxes.disk_snapshots.list.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        ops = SnapshotOps(mock_client)
        snapshot = ops.from_id("snp_123")

        assert isinstance(snapshot, Snapshot)
        assert snapshot.id == "snp_123"


class TestBlueprintOps:
    """Tests for BlueprintOps class."""

    def test_create(self, mock_client: Mock, blueprint_view: MockBlueprintView) -> None:
        """Test create method."""
        mock_client.blueprints.create_and_await_build_complete.return_value = blueprint_view

        ops = BlueprintOps(mock_client)
        blueprint = ops.create(
            name="test-blueprint",
            polling_config=PollingConfig(timeout_seconds=60.0),
        )

        assert isinstance(blueprint, Blueprint)
        assert blueprint.id == "bpt_123"
        mock_client.blueprints.create_and_await_build_complete.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        ops = BlueprintOps(mock_client)
        blueprint = ops.from_id("bpt_123")

        assert isinstance(blueprint, Blueprint)
        assert blueprint.id == "bpt_123"

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(blueprints=[])
        mock_client.blueprints.list.return_value = page

        ops = BlueprintOps(mock_client)
        blueprints = ops.list(limit=10)

        assert len(blueprints) == 0
        mock_client.blueprints.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, blueprint_view: MockBlueprintView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(blueprints=[blueprint_view])
        mock_client.blueprints.list.return_value = page

        ops = BlueprintOps(mock_client)
        blueprints = ops.list(
            limit=10,
            name="test",
            starting_after="bp_000",
        )

        assert len(blueprints) == 1
        assert isinstance(blueprints[0], Blueprint)
        assert blueprints[0].id == "bpt_123"
        mock_client.blueprints.list.assert_called_once()

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        blueprint_view1 = MockBlueprintView(id="bp_001", name="blueprint-1")
        blueprint_view2 = MockBlueprintView(id="bp_002", name="blueprint-2")
        page = SimpleNamespace(blueprints=[blueprint_view1, blueprint_view2])
        mock_client.blueprints.list.return_value = page

        ops = BlueprintOps(mock_client)
        blueprints = ops.list(limit=10)

        assert len(blueprints) == 2
        assert isinstance(blueprints[0], Blueprint)
        assert isinstance(blueprints[1], Blueprint)
        assert blueprints[0].id == "bp_001"
        assert blueprints[1].id == "bp_002"
        mock_client.blueprints.list.assert_called_once()


class TestStorageObjectOps:
    """Tests for StorageObjectOps class."""

    def test_create(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test create method."""
        mock_client.objects.create.return_value = object_view

        ops = StorageObjectOps(mock_client)
        obj = ops.create(name="test.txt", content_type="text", metadata={"key": "value"})

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url == "https://upload.example.com/obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="test.txt",
            content_type="text",
            metadata={"key": "value"},
        )

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        ops = StorageObjectOps(mock_client)
        obj = ops.from_id("obj_123")

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        assert obj.upload_url is None

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""
        page = SimpleNamespace(objects=[])
        mock_client.objects.list.return_value = page

        ops = StorageObjectOps(mock_client)
        objects = ops.list(limit=10)

        assert len(objects) == 0
        mock_client.objects.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test list method with single result."""
        page = SimpleNamespace(objects=[object_view])
        mock_client.objects.list.return_value = page

        ops = StorageObjectOps(mock_client)
        objects = ops.list(
            content_type="text",
            limit=10,
            name="test",
            search="query",
            starting_after="obj_000",
            state="READ_ONLY",
        )

        assert len(objects) == 1
        assert isinstance(objects[0], StorageObject)
        assert objects[0].id == "obj_123"
        mock_client.objects.list.assert_called_once_with(
            content_type="text",
            limit=10,
            name="test",
            search="query",
            starting_after="obj_000",
            state="READ_ONLY",
        )

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        object_view1 = MockObjectView(id="obj_001", name="object-1")
        object_view2 = MockObjectView(id="obj_002", name="object-2")
        page = SimpleNamespace(objects=[object_view1, object_view2])
        mock_client.objects.list.return_value = page

        ops = StorageObjectOps(mock_client)
        objects = ops.list(limit=10)

        assert len(objects) == 2
        assert isinstance(objects[0], StorageObject)
        assert isinstance(objects[1], StorageObject)
        assert objects[0].id == "obj_001"
        assert objects[1].id == "obj_002"
        mock_client.objects.list.assert_called_once()

    def test_upload_from_file(self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path) -> None:
        """Test upload_from_file method."""
        mock_client.objects.create.return_value = object_view

        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test content")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_file(temp_file, name="test.txt")

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="test.txt",
            content_type="text",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_called_once_with(object_view.upload_url, content=b"test content")
        mock_client.objects.complete.assert_called_once()

    def test_upload_from_text(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test upload_from_text method."""
        mock_client.objects.create.return_value = object_view

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_text("test content", name="test.txt", metadata={"key": "value"})

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="test.txt",
            content_type="text",
            metadata={"key": "value"},
            ttl_ms=None,
        )
        http_client.put.assert_called_once_with(object_view.upload_url, content="test content")
        mock_client.objects.complete.assert_called_once()

    def test_upload_from_bytes(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test upload_from_bytes method."""
        mock_client.objects.create.return_value = object_view

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_bytes(b"test content", name="test.bin", content_type="binary")

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="test.bin",
            content_type="binary",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_called_once_with(object_view.upload_url, content=b"test content")
        mock_client.objects.complete.assert_called_once()

    def test_upload_from_file_missing_path(self, mock_client: Mock, tmp_path: Path) -> None:
        """upload_from_file should raise when file cannot be read."""
        ops = StorageObjectOps(mock_client)
        missing_file = tmp_path / "missing.txt"

        with pytest.raises(OSError, match="Failed to read file"):
            ops.upload_from_file(missing_file)

    def test_as_build_context(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """as_build_context should return the correct dict shape."""
        obj = StorageObject(mock_client, object_view.id, upload_url=None)

        assert obj.as_build_context() == {
            "object_id": object_view.id,
            "type": "object",
        }

    def test_upload_from_dir(self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path) -> None:
        """Test upload_from_dir method."""
        mock_client.objects.create.return_value = object_view

        # Create a temporary directory with some files
        test_dir = tmp_path / "test_directory"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")
        subdir = test_dir / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("content3")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_dir(test_dir, name="archive.tar.gz", metadata={"key": "value"})

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="archive.tar.gz",
            content_type="tgz",
            metadata={"key": "value"},
            ttl_ms=None,
        )
        # Verify that put was called with tarball content
        http_client.put.assert_called_once()
        call_args = http_client.put.call_args
        assert call_args[0][0] == object_view.upload_url
        uploaded_content = call_args[1]["content"]
        # Verify it is bytes representing a gzipped tar archive
        assert isinstance(uploaded_content, (bytes, bytearray))
        mock_client.objects.complete.assert_called_once()

    def test_upload_from_dir_default_name(self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path) -> None:
        """Test upload_from_dir uses directory name by default."""
        mock_client.objects.create.return_value = object_view

        test_dir = tmp_path / "my_folder"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_dir(test_dir)

        assert isinstance(obj, StorageObject)
        # Name should be directory name + .tar.gz
        mock_client.objects.create.assert_called_once_with(
            name="my_folder.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=None,
        )

    def test_upload_from_dir_with_ttl(self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path) -> None:
        """Test upload_from_dir with TTL."""
        from datetime import timedelta

        mock_client.objects.create.return_value = object_view

        test_dir = tmp_path / "temp_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("temporary content")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_dir(test_dir, ttl=timedelta(hours=2))

        assert isinstance(obj, StorageObject)
        mock_client.objects.create.assert_called_once_with(
            name="temp_dir.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=7200000,  # 2 hours = 7200 seconds = 7200000 milliseconds
        )

    def test_upload_from_dir_empty_directory(
        self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir with empty directory."""
        mock_client.objects.create.return_value = object_view

        test_dir = tmp_path / "empty_dir"
        test_dir.mkdir()

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        obj = ops.upload_from_dir(test_dir)

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="empty_dir.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_called_once()
        mock_client.objects.complete.assert_called_once()

    def test_upload_from_dir_with_string_path(
        self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """Test upload_from_dir with string path instead of Path object."""
        mock_client.objects.create.return_value = object_view

        test_dir = tmp_path / "string_path_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        ops = StorageObjectOps(mock_client)
        # Pass string path instead of Path object
        obj = ops.upload_from_dir(str(test_dir))

        assert isinstance(obj, StorageObject)
        assert obj.id == "obj_123"
        mock_client.objects.create.assert_called_once_with(
            name="string_path_dir.tar.gz",
            content_type="tgz",
            metadata=None,
            ttl_ms=None,
        )
        http_client.put.assert_called_once()
        mock_client.objects.complete.assert_called_once()

    def test_upload_from_dir_respects_filter(
        self, mock_client: Mock, object_view: MockObjectView, tmp_path: Path
    ) -> None:
        """upload_from_dir should respect a tar filter when provided."""
        mock_client.objects.create.return_value = object_view

        test_dir = tmp_path / "ctx"
        test_dir.mkdir()
        (test_dir / "keep.txt").write_text("keep", encoding="utf-8")
        (test_dir / "ignore.log").write_text("ignore", encoding="utf-8")
        build_dir = test_dir / "build"
        build_dir.mkdir()
        (build_dir / "ignored.txt").write_text("ignored", encoding="utf-8")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        client = StorageObjectOps(mock_client)

        # Tar filter: drop logs and anything under build/
        def ignore_logs_and_build(ti: tarfile.TarInfo) -> tarfile.TarInfo | None:
            if ti.name.endswith(".log") or ti.name.startswith("build/"):
                return None
            return ti

        obj = client.upload_from_dir(test_dir, ignore=ignore_logs_and_build)

        assert isinstance(obj, StorageObject)
        uploaded_content = http_client.put.call_args[1]["content"]

        with tarfile.open(fileobj=io.BytesIO(uploaded_content), mode="r:gz") as tar:
            names = {m.name for m in tar.getmembers()}

        assert "keep.txt" in names
        assert "ignore.log" not in names
        assert not any(name.startswith("build/") for name in names)


class TestScorerOps:
    """Tests for ScorerOps class."""

    def test_create(self, mock_client: Mock, scorer_view: MockScorerView) -> None:
        """Test create method."""
        mock_client.scenarios.scorers.create.return_value = scorer_view

        ops = ScorerOps(mock_client)
        scorer = ops.create(
            bash_script="echo 'score=1.0'",
            type="test_scorer",
        )

        assert isinstance(scorer, Scorer)
        assert scorer.id == "sco_123"
        mock_client.scenarios.scorers.create.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        ops = ScorerOps(mock_client)
        scorer = ops.from_id("sco_123")

        assert isinstance(scorer, Scorer)
        assert scorer.id == "sco_123"

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""
        mock_client.scenarios.scorers.list.return_value = []

        ops = ScorerOps(mock_client)
        scorers = ops.list(limit=10)

        assert len(scorers) == 0
        mock_client.scenarios.scorers.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, scorer_view: MockScorerView) -> None:
        """Test list method with single result."""
        mock_client.scenarios.scorers.list.return_value = [scorer_view]

        ops = ScorerOps(mock_client)
        scorers = ops.list(
            limit=10,
            starting_after="scorer_000",
        )

        assert len(scorers) == 1
        assert isinstance(scorers[0], Scorer)
        assert scorers[0].id == "sco_123"
        mock_client.scenarios.scorers.list.assert_called_once()

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        scorer_view1 = MockScorerView(id="scorer_001", type="scorer-1")
        scorer_view2 = MockScorerView(id="scorer_002", type="scorer-2")
        mock_client.scenarios.scorers.list.return_value = [scorer_view1, scorer_view2]

        ops = ScorerOps(mock_client)
        scorers = ops.list(limit=10)

        assert len(scorers) == 2
        assert isinstance(scorers[0], Scorer)
        assert isinstance(scorers[1], Scorer)
        assert scorers[0].id == "scorer_001"
        assert scorers[1].id == "scorer_002"
        mock_client.scenarios.scorers.list.assert_called_once()


class TestAgentClient:
    """Tests for AgentClient class."""

    def test_create(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create method."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create(
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        client = AgentOps(mock_client)
        agent = client.from_id("agt_123")

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"

    def test_list(self, mock_client: Mock) -> None:
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
        mock_client.agents.list.return_value = page

        # Mock retrieve to return the corresponding agent_view when called
        def mock_retrieve(agent_id: str, **_kwargs: object) -> MockAgentView:
            agent_views = {
                "agent_001": agent_view_1,
                "agent_002": agent_view_2,
                "agent_003": agent_view_3,
            }
            return agent_views[agent_id]

        mock_client.agents.retrieve.side_effect = mock_retrieve

        client = AgentOps(mock_client)
        agents = client.list(
            limit=10,
            starting_after="agent_000",
        )

        # Verify we got three agents
        assert len(agents) == 3
        assert all(isinstance(agent, Agent) for agent in agents)

        # Verify the agent IDs
        assert agents[0].id == "agent_001"
        assert agents[1].id == "agent_002"
        assert agents[2].id == "agent_003"

        # Test that get_info() retrieves the AgentView for the first agent
        info = agents[0].get_info()
        assert info.id == "agent_001"
        assert info.name == "first-agent"
        assert info.create_time_ms == 1234567890000
        assert info.is_public is False
        assert info.source is None

        # Test that get_info() retrieves the AgentView for the second agent
        info = agents[1].get_info()
        assert info.id == "agent_002"
        assert info.name == "second-agent"
        assert info.create_time_ms == 1234567891000
        assert info.is_public is True
        assert info.source == {"type": "git", "git": {"repository": "https://github.com/example/repo"}}

        # Test that get_info() retrieves the AgentView for the third agent
        info = agents[2].get_info()
        assert info.id == "agent_003"
        assert info.name == "third-agent"
        assert info.create_time_ms == 1234567892000
        assert info.is_public is False
        assert info.source == {"type": "npm", "npm": {"package_name": "example-package"}}

        # Verify that agents.retrieve was called for each agent
        assert mock_client.agents.retrieve.call_count == 3

        mock_client.agents.list.assert_called_once()

    def test_create_from_npm(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_npm factory method."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_npm(
            name="test-agent",
            package_name="@runloop/example-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/example-agent",
                },
            },
            name="test-agent",
            version="1.2.3",
        )

    def test_create_from_npm_with_all_options(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_npm factory method with all optional parameters."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_npm(
            package_name="@runloop/example-agent",
            registry_url="https://registry.example.com",
            agent_setup=["npm install", "npm run setup"],
            name="test-agent",
            version="1.2.3",
            extra_headers={"X-Custom": "header"},
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/example-agent",
                    "registry_url": "https://registry.example.com",
                    "agent_setup": ["npm install", "npm run setup"],
                },
            },
            name="test-agent",
            version="1.2.3",
            extra_headers={"X-Custom": "header"},
        )

    def test_create_from_npm_raises_when_source_provided(self, mock_client: Mock) -> None:
        """Test create_from_npm raises ValueError when source is provided in params."""
        client = AgentOps(mock_client)

        with pytest.raises(ValueError, match="Cannot specify 'source' when using create_from_npm"):
            client.create_from_npm(
                package_name="@runloop/example-agent",
                name="test-agent",
                version="1.2.3",
                source={"type": "git", "git": {"repository": "https://github.com/example/repo"}},
            )

    def test_create_from_pip(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_pip factory method."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_pip(
            package_name="runloop-example-agent",
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "pip",
                "pip": {
                    "package_name": "runloop-example-agent",
                },
            },
            name="test-agent",
            version="1.2.3",
        )

    def test_create_from_pip_with_all_options(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_pip factory method with all optional parameters."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_pip(
            package_name="runloop-example-agent",
            registry_url="https://pypi.example.com",
            agent_setup=["pip install extra-deps"],
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "pip",
                "pip": {
                    "package_name": "runloop-example-agent",
                    "registry_url": "https://pypi.example.com",
                    "agent_setup": ["pip install extra-deps"],
                },
            },
            name="test-agent",
            version="1.2.3",
        )

    def test_create_from_git(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_git factory method."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_git(
            repository="https://github.com/example/agent-repo",
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "git",
                "git": {
                    "repository": "https://github.com/example/agent-repo",
                },
            },
            name="test-agent",
            version="1.2.3",
        )

    def test_create_from_git_with_all_options(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_git factory method with all optional parameters."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_git(
            repository="https://github.com/example/agent-repo",
            ref="develop",
            agent_setup=["npm install", "npm run build"],
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "git",
                "git": {
                    "repository": "https://github.com/example/agent-repo",
                    "ref": "develop",
                    "agent_setup": ["npm install", "npm run build"],
                },
            },
            name="test-agent",
            version="1.2.3",
        )

    def test_create_from_object(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_object factory method."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_object(
            object_id="obj_123",
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "object",
                "object": {
                    "object_id": "obj_123",
                },
            },
            name="test-agent",
            version="1.2.3",
        )

    def test_create_from_object_with_agent_setup(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test create_from_object factory method with agent_setup."""
        mock_client.agents.create.return_value = agent_view

        client = AgentOps(mock_client)
        agent = client.create_from_object(
            object_id="obj_123",
            agent_setup=["chmod +x setup.sh", "./setup.sh"],
            name="test-agent",
            version="1.2.3",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agt_123"
        mock_client.agents.create.assert_called_once_with(
            source={
                "type": "object",
                "object": {
                    "object_id": "obj_123",
                    "agent_setup": ["chmod +x setup.sh", "./setup.sh"],
                },
            },
            name="test-agent",
            version="1.2.3",
        )


class TestScenarioOps:
    """Tests for ScenarioOps class."""

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""

        ops = ScenarioOps(mock_client)
        scenario = ops.from_id("scn_123")

        assert isinstance(scenario, Scenario)
        assert scenario.id == "scn_123"

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""

        mock_client.scenarios.list.return_value = []

        ops = ScenarioOps(mock_client)
        scenarios = ops.list(limit=10)

        assert len(scenarios) == 0
        mock_client.scenarios.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, scenario_view: MockScenarioView) -> None:
        """Test list method with single result."""

        mock_client.scenarios.list.return_value = [scenario_view]

        ops = ScenarioOps(mock_client)
        scenarios = ops.list(limit=10)

        assert len(scenarios) == 1
        assert isinstance(scenarios[0], Scenario)
        assert scenarios[0].id == "scn_123"
        mock_client.scenarios.list.assert_called_once()

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""

        scenario_view1 = MockScenarioView(id="scn_001", name="scenario-1")
        scenario_view2 = MockScenarioView(id="scn_002", name="scenario-2")
        mock_client.scenarios.list.return_value = [scenario_view1, scenario_view2]

        ops = ScenarioOps(mock_client)
        scenarios = ops.list(limit=10)

        assert len(scenarios) == 2
        assert isinstance(scenarios[0], Scenario)
        assert isinstance(scenarios[1], Scenario)
        assert scenarios[0].id == "scn_001"
        assert scenarios[1].id == "scn_002"
        mock_client.scenarios.list.assert_called_once()


class TestBenchmarkOps:
    """Tests for BenchmarkOps class."""

    def test_create(self, mock_client: Mock, benchmark_view: MockBenchmarkView) -> None:
        """Test create method."""
        mock_client.benchmarks.create.return_value = benchmark_view

        ops = BenchmarkOps(mock_client)
        benchmark = ops.create(name="test-benchmark", scenario_ids=["scn_001", "scn_002"])

        assert isinstance(benchmark, Benchmark)
        assert benchmark.id == "bmd_123"
        mock_client.benchmarks.create.assert_called_once_with(
            name="test-benchmark", scenario_ids=["scn_001", "scn_002"]
        )

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        ops = BenchmarkOps(mock_client)
        benchmark = ops.from_id("bmd_123")

        assert isinstance(benchmark, Benchmark)
        assert benchmark.id == "bmd_123"

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        benchmark_view1 = MockBenchmarkView(id="bmd_001", name="benchmark-1")
        benchmark_view2 = MockBenchmarkView(id="bmd_002", name="benchmark-2")
        page = SimpleNamespace(benchmarks=[benchmark_view1, benchmark_view2])
        mock_client.benchmarks.list.return_value = page

        ops = BenchmarkOps(mock_client)
        benchmarks = ops.list(limit=10)

        assert len(benchmarks) == 2
        assert isinstance(benchmarks[0], Benchmark)
        assert isinstance(benchmarks[1], Benchmark)
        assert benchmarks[0].id == "bmd_001"
        assert benchmarks[1].id == "bmd_002"
        mock_client.benchmarks.list.assert_called_once_with(limit=10)

    def test_list_with_name_filter(self, mock_client: Mock, benchmark_view: MockBenchmarkView) -> None:
        """Test list method with name filter."""
        page = SimpleNamespace(benchmarks=[benchmark_view])
        mock_client.benchmarks.list.return_value = page

        ops = BenchmarkOps(mock_client)
        benchmarks = ops.list(name="test-benchmark", limit=10)

        assert len(benchmarks) == 1
        mock_client.benchmarks.list.assert_called_once_with(name="test-benchmark", limit=10)


class TestNetworkPolicyOps:
    """Tests for NetworkPolicyOps class."""

    def test_create(self, mock_client: Mock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test create method."""
        mock_client.network_policies.create.return_value = network_policy_view

        ops = NetworkPolicyOps(mock_client)
        network_policy = ops.create(
            name="test-network-policy",
            allowed_hostnames=["github.com", "*.npmjs.org"],
        )

        assert isinstance(network_policy, NetworkPolicy)
        assert network_policy.id == "np_123"
        mock_client.network_policies.create.assert_called_once()

    def test_from_id(self, mock_client: Mock) -> None:
        """Test from_id method."""
        ops = NetworkPolicyOps(mock_client)
        network_policy = ops.from_id("np_123")

        assert isinstance(network_policy, NetworkPolicy)
        assert network_policy.id == "np_123"

    def test_list_empty(self, mock_client: Mock) -> None:
        """Test list method with empty results."""
        mock_client.network_policies.list.return_value = []

        ops = NetworkPolicyOps(mock_client)
        network_policies = ops.list(limit=10)

        assert len(network_policies) == 0
        mock_client.network_policies.list.assert_called_once()

    def test_list_single(self, mock_client: Mock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test list method with single result."""
        mock_client.network_policies.list.return_value = [network_policy_view]

        ops = NetworkPolicyOps(mock_client)
        network_policies = ops.list(
            limit=10,
            starting_after="np_000",
        )

        assert len(network_policies) == 1
        assert isinstance(network_policies[0], NetworkPolicy)
        assert network_policies[0].id == "np_123"
        mock_client.network_policies.list.assert_called_once()

    def test_list_multiple(self, mock_client: Mock) -> None:
        """Test list method with multiple results."""
        network_policy_view1 = MockNetworkPolicyView(id="np_001", name="policy-1")
        network_policy_view2 = MockNetworkPolicyView(id="np_002", name="policy-2")
        mock_client.network_policies.list.return_value = [network_policy_view1, network_policy_view2]

        ops = NetworkPolicyOps(mock_client)
        network_policies = ops.list(limit=10)

        assert len(network_policies) == 2
        assert isinstance(network_policies[0], NetworkPolicy)
        assert isinstance(network_policies[1], NetworkPolicy)
        assert network_policies[0].id == "np_001"
        assert network_policies[1].id == "np_002"
        mock_client.network_policies.list.assert_called_once()


class TestRunloopSDK:
    """Tests for RunloopSDK class."""

    def test_init(self) -> None:
        """Test RunloopSDK initialization."""
        runloop = RunloopSDK(bearer_token="test-token")
        assert runloop.api is not None
        assert isinstance(runloop.agent, AgentOps)
        assert isinstance(runloop.benchmark, BenchmarkOps)
        assert isinstance(runloop.devbox, DevboxOps)
        assert isinstance(runloop.network_policy, NetworkPolicyOps)
        assert isinstance(runloop.scorer, ScorerOps)
        assert isinstance(runloop.snapshot, SnapshotOps)
        assert isinstance(runloop.blueprint, BlueprintOps)
        assert isinstance(runloop.storage_object, StorageObjectOps)

    def test_init_with_max_retries(self) -> None:
        """Test RunloopSDK initialization with max_retries."""
        runloop = RunloopSDK(bearer_token="test-token", max_retries=3)
        assert runloop.api is not None

    def test_close(self) -> None:
        """Test close method."""
        runloop = RunloopSDK(bearer_token="test-token")
        # Verify close doesn't raise
        runloop.close()

    def test_context_manager(self) -> None:
        """Test context manager behavior."""
        with RunloopSDK(bearer_token="test-token") as runloop:
            assert runloop.api is not None
        # Verify context manager properly closes (implementation detail of context manager protocol)

    def test_api_property(self) -> None:
        """Test api property access."""
        runloop = RunloopSDK(bearer_token="test-token")
        assert runloop.api is not None
        assert hasattr(runloop.api, "devboxes")
        assert hasattr(runloop.api, "blueprints")
        assert hasattr(runloop.api, "objects")
