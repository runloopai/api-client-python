from __future__ import annotations

from typing import Dict, Literal, Mapping, Iterable, Optional
from pathlib import Path

import httpx

from .devbox import Devbox
from .._types import Body, Omit, Query, Headers, Timeout, NotGiven, SequenceNotStr, omit, not_given
from .._client import Runloop
from ._helpers import ContentType, detect_content_type
from .snapshot import Snapshot
from .blueprint import Blueprint
from ..lib.polling import PollingConfig
from .storage_object import StorageObject
from ..types.shared_params.mount import Mount
from ..types.blueprint_create_params import Service
from ..types.shared_params.launch_parameters import LaunchParameters
from ..types.shared_params.code_mount_parameters import CodeMountParameters


class DevboxClient:
    """High-level manager for creating and managing Devbox instances.
    
    Accessed via sdk.devbox, provides methods to create devboxes from scratch,
    blueprints, or snapshots, and to list existing devboxes.
    
    Example:
        >>> sdk = RunloopSDK()
        >>> devbox = sdk.devbox.create(name="my-devbox")
        >>> devboxes = sdk.devbox.list(limit=10)
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def create(
        self,
        *,
        blueprint_id: Optional[str] | Omit = omit,
        blueprint_name: Optional[str] | Omit = omit,
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
        snapshot_id: Optional[str] | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
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
            snapshot_id=snapshot_id,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_id(
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
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
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
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_name(
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
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
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
        return Devbox(self._client, devbox_view.id)

    def create_from_snapshot(
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
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
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
        return Devbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> Devbox:
        self._client.devboxes.await_running(devbox_id)
        return Devbox(self._client, devbox_id)

    def list(
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
    ) -> list[Devbox]:
        page = self._client.devboxes.list(
            limit=limit,
            starting_after=starting_after,
            status=status,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return [Devbox(self._client, item.id) for item in page.devboxes]


class SnapshotClient:
    """High-level manager for working with disk snapshots.
    
    Accessed via sdk.snapshot, provides methods to list snapshots and access
    snapshot details.
    
    Example:
        >>> sdk = RunloopSDK()
        >>> snapshots = sdk.snapshot.list(devbox_id="dev-123")
        >>> snapshot = sdk.snapshot.from_id("snap-123")
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def list(
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
    ) -> list[Snapshot]:
        page = self._client.devboxes.disk_snapshots.list(
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
        return [Snapshot(self._client, item.id) for item in page.snapshots]

    def from_id(self, snapshot_id: str) -> Snapshot:
        return Snapshot(self._client, snapshot_id)


class BlueprintClient:
    """High-level manager for creating and managing blueprints.
    
    Accessed via sdk.blueprint, provides methods to create blueprints with
    Dockerfiles and system setup commands, and to list existing blueprints.
    
    Example:
        >>> sdk = RunloopSDK()
        >>> blueprint = sdk.blueprint.create(
        ...     name="my-blueprint",
        ...     dockerfile="FROM ubuntu:22.04\\nRUN apt-get update"
        ... )
        >>> blueprints = sdk.blueprint.list()
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def create(
        self,
        *,
        name: str,
        base_blueprint_id: Optional[str] | Omit = omit,
        base_blueprint_name: Optional[str] | Omit = omit,
        build_args: Optional[Dict[str, str]] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        dockerfile: Optional[str] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        services: Optional[Iterable[Service]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Blueprint:
        blueprint = self._client.blueprints.create_and_await_build_complete(
            name=name,
            base_blueprint_id=base_blueprint_id,
            base_blueprint_name=base_blueprint_name,
            build_args=build_args,
            code_mounts=code_mounts,
            dockerfile=dockerfile,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            secrets=secrets,
            services=services,
            system_setup_commands=system_setup_commands,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return Blueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> Blueprint:
        return Blueprint(self._client, blueprint_id)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> list[Blueprint]:
        page = self._client.blueprints.list(
            limit=limit,
            name=name,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return [Blueprint(self._client, item.id) for item in page.blueprints]


class StorageObjectClient:
    """High-level manager for creating and managing storage objects.
    
    Accessed via sdk.storage_object, provides methods to create, upload, download,
    and list storage objects with convenient helpers for file and text uploads.
    
    Example:
        >>> sdk = RunloopSDK()
        >>> obj = sdk.storage_object.upload_from_text("Hello!", "greeting.txt")
        >>> content = obj.download_as_text()
        >>> objects = sdk.storage_object.list()
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def create(
        self,
        name: str,
        *,
        content_type: ContentType | None = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> StorageObject:
        content_type = content_type or detect_content_type(name)
        obj = self._client.objects.create(name=name, content_type=content_type, metadata=metadata)
        return StorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> StorageObject:
        return StorageObject(self._client, object_id, upload_url=None)

    def list(
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
    ) -> list[StorageObject]:
        page = self._client.objects.list(
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
        return [StorageObject(self._client, item.id, upload_url=item.upload_url) for item in page.objects]

    def upload_from_file(
        self,
        path: str | Path,
        name: str | None = None,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> StorageObject:
        file_path = Path(path)
        object_name = name or file_path.name
        obj = self.create(object_name, content_type=content_type, metadata=metadata)
        obj.upload_content(file_path)
        obj.complete()
        return obj

    def upload_from_text(
        self,
        text: str,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> StorageObject:
        obj = self.create(name, content_type="text", metadata=metadata)
        obj.upload_content(text)
        obj.complete()
        return obj

    def upload_from_bytes(
        self,
        data: bytes,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> StorageObject:
        obj = self.create(name, content_type=content_type or detect_content_type(name), metadata=metadata)
        obj.upload_content(data)
        obj.complete()
        return obj


class RunloopSDK:
    """High-level synchronous entry point for the Runloop SDK.
    
    Provides a Pythonic, object-oriented interface for managing devboxes, blueprints,
    snapshots, and storage objects. Exposes the generated REST client via the ``api``
    attribute for advanced use cases.
    
    Attributes:
        api: Direct access to the generated REST API client.
        devbox: High-level interface for devbox management.
        blueprint: High-level interface for blueprint management.
        snapshot: High-level interface for snapshot management.
        storage_object: High-level interface for storage object management.
        
    Example:
        >>> sdk = RunloopSDK()  # Uses RUNLOOP_API_KEY env var
        >>> with sdk.devbox.create(name="my-devbox") as devbox:
        ...     result = devbox.cmd.exec("echo 'hello'")
        ...     print(result.stdout())
    """

    api: Runloop
    devbox: DevboxClient
    blueprint: BlueprintClient
    snapshot: SnapshotClient
    storage_object: StorageObjectClient

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int | None = None,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        if max_retries is None:
            self.api = Runloop(
                bearer_token=bearer_token,
                base_url=base_url,
                timeout=timeout,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
            )
        else:
            self.api = Runloop(
                bearer_token=bearer_token,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
            )

        self.devbox = DevboxClient(self.api)
        self.blueprint = BlueprintClient(self.api)
        self.snapshot = SnapshotClient(self.api)
        self.storage_object = StorageObjectClient(self.api)

    def close(self) -> None:
        self.api.close()

    def __enter__(self) -> "RunloopSDK":
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()
