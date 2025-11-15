"""Asynchronous SDK entry points and management interfaces."""

from __future__ import annotations

from typing import Dict, Mapping, Optional
from pathlib import Path
from typing_extensions import Unpack

import httpx

from ._types import (
    LongRequestOptions,
    SDKDevboxListParams,
    SDKObjectListParams,
    SDKDevboxCreateParams,
    SDKObjectCreateParams,
    SDKBlueprintListParams,
    SDKBlueprintCreateParams,
    SDKDiskSnapshotListParams,
    SDKDevboxExtraCreateParams,
)
from .._types import Timeout, NotGiven, not_given
from .._client import DEFAULT_MAX_RETRIES, AsyncRunloop
from ._helpers import detect_content_type
from .async_devbox import AsyncDevbox
from .async_snapshot import AsyncSnapshot
from .async_blueprint import AsyncBlueprint
from .async_storage_object import AsyncStorageObject
from ..types.object_create_params import ContentType


class AsyncDevboxClient:
    """Async manager for :class:`AsyncDevbox` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKDevboxCreateParams],
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_id(
        self,
        blueprint_id: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_name(
        self,
        blueprint_name: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_name=blueprint_name,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_snapshot(
        self,
        snapshot_id: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> AsyncDevbox:
        return AsyncDevbox(self._client, devbox_id)

    async def list(
        self,
        **params: Unpack[SDKDevboxListParams],
    ) -> list[AsyncDevbox]:
        page = await self._client.devboxes.list(
            **params,
        )
        return [AsyncDevbox(self._client, item.id) for item in page.devboxes]


class AsyncSnapshotClient:
    """Async manager for :class:`AsyncSnapshot` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def list(
        self,
        **params: Unpack[SDKDiskSnapshotListParams],
    ) -> list[AsyncSnapshot]:
        page = await self._client.devboxes.disk_snapshots.list(
            **params,
        )
        return [AsyncSnapshot(self._client, item.id) for item in page.snapshots]

    def from_id(self, snapshot_id: str) -> AsyncSnapshot:
        return AsyncSnapshot(self._client, snapshot_id)


class AsyncBlueprintClient:
    """Async manager for :class:`AsyncBlueprint` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKBlueprintCreateParams],
    ) -> AsyncBlueprint:
        blueprint = await self._client.blueprints.create_and_await_build_complete(
            **params,
        )
        return AsyncBlueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> AsyncBlueprint:
        return AsyncBlueprint(self._client, blueprint_id)

    async def list(
        self,
        **params: Unpack[SDKBlueprintListParams],
    ) -> list[AsyncBlueprint]:
        page = await self._client.blueprints.list(
            **params,
        )
        return [AsyncBlueprint(self._client, item.id) for item in page.blueprints]


class AsyncStorageObjectClient:
    """Async manager for :class:`AsyncStorageObject` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKObjectCreateParams],
    ) -> AsyncStorageObject:
        obj = await self._client.objects.create(**params)
        return AsyncStorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> AsyncStorageObject:
        return AsyncStorageObject(self._client, object_id, upload_url=None)

    async def list(
        self,
        **params: Unpack[SDKObjectListParams],
    ) -> list[AsyncStorageObject]:
        page = await self._client.objects.list(
            **params,
        )
        return [AsyncStorageObject(self._client, item.id, upload_url=item.upload_url) for item in page.objects]

    async def upload_from_file(
        self,
        file_path: str | Path,
        name: str | None = None,
        *,
        content_type: ContentType | None = None,
        metadata: Optional[Dict[str, str]] = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        path = Path(file_path)

        try:
            content = path.read_bytes()
        except OSError as error:
            raise OSError(f"Failed to read file {path}: {error}") from error

        name = name or path.name
        content_type = content_type or detect_content_type(str(file_path))
        obj = await self.create(name=name, content_type=content_type, metadata=metadata, **options)
        await obj.upload_content(content)
        await obj.complete()
        return obj

    async def upload_from_text(
        self,
        text: str,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        obj = await self.create(name=name, content_type="text", metadata=metadata, **options)
        await obj.upload_content(text)
        await obj.complete()
        return obj

    async def upload_from_bytes(
        self,
        data: bytes,
        name: str,
        *,
        content_type: ContentType,
        metadata: Optional[Dict[str, str]] = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        obj = await self.create(name=name, content_type=content_type, metadata=metadata, **options)
        await obj.upload_content(data)
        await obj.complete()
        return obj


class AsyncRunloopSDK:
    """
    High-level asynchronous entry point for the Runloop SDK.

    The generated async REST client remains available via the ``api`` attribute.
    Higher-level helpers will be introduced incrementally.
    """

    api: AsyncRunloop
    devbox: AsyncDevboxClient
    blueprint: AsyncBlueprintClient
    snapshot: AsyncSnapshotClient
    storage_object: AsyncStorageObjectClient

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api = AsyncRunloop(
            bearer_token=bearer_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
        )

        self.devbox = AsyncDevboxClient(self.api)
        self.blueprint = AsyncBlueprintClient(self.api)
        self.snapshot = AsyncSnapshotClient(self.api)
        self.storage_object = AsyncStorageObjectClient(self.api)

    async def aclose(self) -> None:
        await self.api.close()

    async def __aenter__(self) -> "AsyncRunloopSDK":
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()
