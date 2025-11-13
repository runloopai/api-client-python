from __future__ import annotations

from typing import Dict, Mapping, Iterable, Optional
from pathlib import Path
from typing_extensions import Unpack

import httpx

from .._types import Body, Omit, Query, Headers, Timeout, NotGiven, omit, not_given
from .._client import AsyncRunloop
from ._helpers import ContentType, detect_content_type
from ..lib.polling import PollingConfig
from .async_devbox import AsyncDevbox
from .async_snapshot import AsyncSnapshot
from .async_blueprint import AsyncBlueprint
from .async_storage_object import AsyncStorageObject
from ..types.devbox_list_params import DevboxListParams
from ..types.object_list_params import ObjectListParams
from ..types.shared_params.mount import Mount
from ..types.devbox_create_params import DevboxCreateParams
from ..types.blueprint_list_params import BlueprintListParams
from ..types.blueprint_create_params import BlueprintCreateParams
from ..types.shared_params.launch_parameters import LaunchParameters
from ..types.devboxes.disk_snapshot_list_params import DiskSnapshotListParams
from ..types.shared_params.code_mount_parameters import CodeMountParameters


class AsyncDevboxClient:
    """Async manager for :class:`AsyncDevbox` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
        **params: Unpack[DevboxCreateParams],
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_id(
        self,
        blueprint_id: str,
        *,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            mounts=mounts,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_name(
        self,
        blueprint_name: str,
        *,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_name=blueprint_name,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            mounts=mounts,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_snapshot(
        self,
        snapshot_id: str,
        *,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            mounts=mounts,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> AsyncDevbox:
        return AsyncDevbox(self._client, devbox_id)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        **params: Unpack[DevboxListParams],
    ) -> list[AsyncDevbox]:
        page = await self._client.devboxes.list(
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            **params,
        )
        return [AsyncDevbox(self._client, item.id) for item in page.devboxes]


class AsyncSnapshotClient:
    """Async manager for :class:`AsyncSnapshot` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        **params: Unpack[DiskSnapshotListParams],
    ) -> list[AsyncSnapshot]:
        page = await self._client.devboxes.disk_snapshots.list(
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
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
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
        **params: Unpack[BlueprintCreateParams],
    ) -> AsyncBlueprint:
        blueprint = await self._client.blueprints.create_and_await_build_complete(
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
            **params,
        )
        return AsyncBlueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> AsyncBlueprint:
        return AsyncBlueprint(self._client, blueprint_id)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        **params: Unpack[BlueprintListParams],
    ) -> list[AsyncBlueprint]:
        page = await self._client.blueprints.list(
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            **params,
        )
        return [AsyncBlueprint(self._client, item.id) for item in page.blueprints]


class AsyncStorageObjectClient:
    """Async manager for :class:`AsyncStorageObject` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        name: str,
        *,
        content_type: ContentType | None = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> AsyncStorageObject:
        content_type = content_type or detect_content_type(name)
        obj = await self._client.objects.create(name=name, content_type=content_type, metadata=metadata)
        return AsyncStorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> AsyncStorageObject:
        return AsyncStorageObject(self._client, object_id, upload_url=None)

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        **params: Unpack[ObjectListParams],
    ) -> list[AsyncStorageObject]:
        page = await self._client.objects.list(
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            **params,
        )
        return [AsyncStorageObject(self._client, item.id, upload_url=item.upload_url) for item in page.objects]

    async def upload_from_file(
        self,
        path: str | Path,
        name: str | None = None,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> AsyncStorageObject:
        file_path = Path(path)
        object_name = name or file_path.name
        obj = await self.create(object_name, content_type=content_type, metadata=metadata)
        await obj.upload_content(file_path)
        await obj.complete()
        return obj

    async def upload_from_text(
        self,
        text: str,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> AsyncStorageObject:
        obj = await self.create(name, content_type="text", metadata=metadata)
        await obj.upload_content(text)
        await obj.complete()
        return obj

    async def upload_from_bytes(
        self,
        data: bytes,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> AsyncStorageObject:
        obj = await self.create(name, content_type=content_type or detect_content_type(name), metadata=metadata)
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
        max_retries: int | None = None,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if max_retries is None:
            self.api = AsyncRunloop(
                bearer_token=bearer_token,
                base_url=base_url,
                timeout=timeout,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
            )
        else:
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
