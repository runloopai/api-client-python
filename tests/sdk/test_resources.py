from __future__ import annotations

from types import SimpleNamespace
from typing import List

import httpx
import pytest

from runloop_api_client import RunloopSDK
from runloop_api_client.sdk import Blueprint, StorageObject


@pytest.fixture()
def sdk() -> RunloopSDK:
    return RunloopSDK(bearer_token="test-token")


def test_blueprint_create_and_devbox(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    blueprints_resource = sdk.api.blueprints
    created: List[str] = []

    def fake_create_and_await_build_complete(**kwargs):
        created.append(kwargs["name"])
        return SimpleNamespace(id="bp-001")

    monkeypatch.setattr(blueprints_resource, "create_and_await_build_complete", fake_create_and_await_build_complete)

    devbox_calls: List[dict[str, object]] = []

    monkeypatch.setattr(
        sdk.devbox,
        "create",
        lambda **kwargs: (devbox_calls.append(kwargs), SimpleNamespace(id="dev-123"))[1],
    )

    blueprint = sdk.blueprint.create(name="my-blueprint")
    assert isinstance(blueprint, Blueprint)
    blueprint.create_devbox()

    assert created == ["my-blueprint"]
    assert devbox_calls[0]["blueprint_id"] == "bp-001"


def test_snapshot_list_and_devbox(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    disk_snapshots_resource = sdk.api.devboxes.disk_snapshots

    page = SimpleNamespace(disk_snapshots=[SimpleNamespace(id="snap-1"), SimpleNamespace(id="snap-2")])
    monkeypatch.setattr(disk_snapshots_resource, "list", lambda **kwargs: page)

    devbox_calls: List[dict[str, object]] = []
    monkeypatch.setattr(
        sdk.devbox,
        "create",
        lambda **kwargs: (devbox_calls.append(kwargs), SimpleNamespace(id="dev-from-snap"))[1],
    )

    snapshots = sdk.snapshot.list()
    assert [snap.id for snap in snapshots] == ["snap-1", "snap-2"]
    snapshots[0].create_devbox()

    assert devbox_calls[0]["snapshot_id"] == "snap-1"


def test_storage_object_upload_and_download(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    objects_resource = sdk.api.objects

    created_objects: List[dict[str, object]] = []

    def fake_create(**kwargs):
        created_objects.append(kwargs)
        return SimpleNamespace(id="obj-1", upload_url="https://upload.example.com")

    completed_ids: List[str] = []

    def fake_complete(object_id: str, **_kwargs):
        completed_ids.append(object_id)
        return SimpleNamespace(id=object_id, upload_url=None)

    download_urls: List[str] = []

    def fake_download(object_id: str, **kwargs):
        url = f"https://download.example.com/{object_id}"
        download_urls.append(url)
        return SimpleNamespace(download_url=url)

    monkeypatch.setattr(objects_resource, "create", fake_create)
    monkeypatch.setattr(objects_resource, "complete", fake_complete)
    monkeypatch.setattr(objects_resource, "download", fake_download)

    put_calls: List[tuple[str, bytes]] = []
    get_calls: List[str] = []

    def fake_put(url: str, *, content: bytes, **_kwargs):
        put_calls.append((url, content))
        return SimpleNamespace(raise_for_status=lambda: None)

    def fake_get(url: str, **_kwargs):
        get_calls.append(url)
        return SimpleNamespace(raise_for_status=lambda: None, content=b"hello", text="hello", encoding="utf-8")

    monkeypatch.setattr(httpx, "put", fake_put)
    monkeypatch.setattr(httpx, "get", fake_get)

    obj = sdk.storage_object.upload_from_text("hello", name="greeting.txt")
    assert isinstance(obj, StorageObject)
    assert put_calls == [("https://upload.example.com", b"hello")]
    assert completed_ids == ["obj-1"]

    data = obj.download_as_text()
    assert data == "hello"
    assert get_calls == ["https://download.example.com/obj-1"]
