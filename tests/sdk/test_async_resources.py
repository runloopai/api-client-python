from __future__ import annotations

from types import SimpleNamespace
from typing import List

import httpx
import pytest

from runloop_api_client import AsyncRunloopSDK
from runloop_api_client.sdk import AsyncSnapshot, AsyncBlueprint, AsyncStorageObject


@pytest.fixture()
async def async_sdk() -> AsyncRunloopSDK:
    sdk = AsyncRunloopSDK(bearer_token="test-token")
    try:
        yield sdk
    finally:
        await sdk.aclose()


@pytest.mark.asyncio
async def test_async_blueprint_create(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    blueprints_resource = async_sdk.api.blueprints

    async def fake_create_and_await_build_complete(**kwargs):
        return SimpleNamespace(id="abp-1")

    monkeypatch.setattr(blueprints_resource, "create_and_await_build_complete", fake_create_and_await_build_complete)

    devbox_calls: List[dict[str, object]] = []

    async def fake_devbox_create(**kwargs):
        devbox_calls.append(kwargs)
        return SimpleNamespace(id="adev-1")

    monkeypatch.setattr(async_sdk.devbox, "create", fake_devbox_create)

    blueprint = await async_sdk.blueprint.create(name="async-blueprint")
    assert isinstance(blueprint, AsyncBlueprint)

    await blueprint.create_devbox()
    assert devbox_calls[0]["blueprint_id"] == "abp-1"


@pytest.mark.asyncio
async def test_async_snapshot_list(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    disk_snapshots_resource = async_sdk.api.devboxes.disk_snapshots

    async def fake_list(**kwargs):
        return SimpleNamespace(disk_snapshots=[SimpleNamespace(id="asnap-1")])

    monkeypatch.setattr(disk_snapshots_resource, "list", fake_list)

    snapshots = await async_sdk.snapshot.list()
    assert isinstance(snapshots[0], AsyncSnapshot)


@pytest.mark.asyncio
async def test_async_storage_object_upload(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    objects_resource = async_sdk.api.objects

    async def fake_create(**kwargs):
        return SimpleNamespace(id="aobj-1", upload_url="https://async-upload.example.com")

    async def fake_complete(object_id: str, **kwargs):
        return SimpleNamespace(id=object_id, upload_url=None)

    async def fake_download(object_id: str, **kwargs):
        return SimpleNamespace(download_url=f"https://async-download.example.com/{object_id}")

    monkeypatch.setattr(objects_resource, "create", fake_create)
    monkeypatch.setattr(objects_resource, "complete", fake_complete)
    monkeypatch.setattr(objects_resource, "download", fake_download)

    class DummyAsyncResponse:
        def __init__(self, content: bytes) -> None:
            self.content = content
            self.text = content.decode("utf-8")
            self.encoding = "utf-8"

        def raise_for_status(self) -> None:
            return None

    class DummyAsyncClient:
        def __init__(self, response: DummyAsyncResponse) -> None:
            self._response = response
            self.calls: List[tuple[str, bytes | None]] = []

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, *exc) -> None:
            return None

        async def put(self, url: str, *, content: bytes) -> DummyAsyncResponse:
            self.calls.append((url, content))
            return self._response

        async def get(self, url: str) -> DummyAsyncResponse:
            self.calls.append((url, None))
            return self._response

    dummy_response = DummyAsyncResponse(b"hello async")

    def client_factory(*args, **kwargs):
        return DummyAsyncClient(dummy_response)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)

    obj = await async_sdk.storage_object.upload_from_text("hello async", name="message.txt")
    assert isinstance(obj, AsyncStorageObject)

    content = await obj.download_as_text()
    assert content == "hello async"
