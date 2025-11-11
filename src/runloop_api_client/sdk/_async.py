from __future__ import annotations

from typing import Any, Dict, Literal, Mapping, Iterable, Optional
from pathlib import Path

import httpx

from .._types import NOT_GIVEN, Body, Omit, Query, Headers, Timeout, NotGiven, SequenceNotStr, omit, not_given
from .._client import AsyncRunloop
from ._helpers import ContentType, detect_content_type
from ..lib.polling import PollingConfig
from .async_devbox import AsyncDevbox
from .async_snapshot import AsyncSnapshot
from .async_blueprint import AsyncBlueprint
from .async_storage_object import AsyncStorageObject
from ..types.shared_params.launch_parameters import LaunchParameters
from ..types.shared_params.code_mount_parameters import CodeMountParameters


class AsyncDevboxClient:
    """Async manager for :class:`AsyncDevbox` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        *,
        blueprint_id: Optional[str] | NotGiven = NOT_GIVEN,
        blueprint_name: Optional[str] | NotGiven = NOT_GIVEN,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        entrypoint: Optional[str] | NotGiven = NOT_GIVEN,
        environment_variables: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        repo_connection_id: Optional[str] | NotGiven = NOT_GIVEN,
        secrets: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        snapshot_id: Optional[str] | NotGiven = NOT_GIVEN,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncDevbox:
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
            blueprint_name=blueprint_name,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            snapshot_id=snapshot_id,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_id(
        self,
        blueprint_id: str,
        *,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        entrypoint: Optional[str] | NotGiven = NOT_GIVEN,
        environment_variables: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        repo_connection_id: Optional[str] | NotGiven = NOT_GIVEN,
        secrets: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
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
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        entrypoint: Optional[str] | NotGiven = NOT_GIVEN,
        environment_variables: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        repo_connection_id: Optional[str] | NotGiven = NOT_GIVEN,
        secrets: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
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
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        entrypoint: Optional[str] | NotGiven = NOT_GIVEN,
        environment_variables: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        repo_connection_id: Optional[str] | NotGiven = NOT_GIVEN,
        secrets: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
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
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        status: Literal[
            "provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"
        ]
        | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> list[AsyncDevbox]:
        page = await self._client.devboxes.list(
            limit=limit,
            starting_after=starting_after,
            status=status,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return [AsyncDevbox(self._client, item.id) for item in getattr(page, "devboxes", [])]


class AsyncSnapshotClient:
    """Async manager for :class:`AsyncSnapshot` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def list(
        self,
        *,
        devbox_id: str | Omit = omit,
        limit: int | Omit = omit,
        metadata_key: str | Omit = omit,
        metadata_key_in: str | Omit = omit,
        starting_after: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> list[AsyncSnapshot]:
        page = await self._client.devboxes.disk_snapshots.list(
            devbox_id=devbox_id,
            limit=limit,
            metadata_key=metadata_key,
            metadata_key_in=metadata_key_in,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return [AsyncSnapshot(self._client, item.id) for item in getattr(page, "disk_snapshots", [])]

    def from_id(self, snapshot_id: str) -> AsyncSnapshot:
        return AsyncSnapshot(self._client, snapshot_id)


class AsyncBlueprintClient:
    """Async manager for :class:`AsyncBlueprint` wrappers."""

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        *,
        name: str,
        base_blueprint_id: Optional[str] | NotGiven = NOT_GIVEN,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        dockerfile: Optional[str] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        services: Optional[Iterable[Any]] | NotGiven = NOT_GIVEN,
        system_setup_commands: Optional[SequenceNotStr[str]] | NotGiven = NOT_GIVEN,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncBlueprint:
        blueprint = await self._client.blueprints.create_and_await_build_complete(
            name=name,
            base_blueprint_id=base_blueprint_id,
            code_mounts=code_mounts,
            dockerfile=dockerfile,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            services=services,
            system_setup_commands=system_setup_commands,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return AsyncBlueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> AsyncBlueprint:
        return AsyncBlueprint(self._client, blueprint_id)

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> list[AsyncBlueprint]:
        page = await self._client.blueprints.list(
            limit=limit,
            name=name,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return [AsyncBlueprint(self._client, item.id) for item in getattr(page, "blueprints", [])]


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
        content_type: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        state: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> list[AsyncStorageObject]:
        page = await self._client.objects.list(
            content_type=content_type,
            limit=limit,
            name=name,
            search=search,
            starting_after=starting_after,
            state=state,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return [AsyncStorageObject(self._client, item.id, upload_url=None) for item in getattr(page, "objects", [])]

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
