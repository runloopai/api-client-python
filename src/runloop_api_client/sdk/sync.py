"""Synchronous SDK entry points and management interfaces."""

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
from .devbox import Devbox
from .._types import Timeout, NotGiven, not_given
from .._client import DEFAULT_MAX_RETRIES, Runloop
from ._helpers import detect_content_type
from .snapshot import Snapshot
from .blueprint import Blueprint
from .storage_object import StorageObject
from ..types.object_create_params import ContentType


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
        **params: Unpack[SDKDevboxCreateParams],
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_id(
        self,
        blueprint_id: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_name(
        self,
        blueprint_name: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_name=blueprint_name,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_snapshot(
        self,
        snapshot_id: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> Devbox:
        devbox_view = self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> Devbox:
        self._client.devboxes.await_running(devbox_id)
        return Devbox(self._client, devbox_id)

    def list(
        self,
        **params: Unpack[SDKDevboxListParams],
    ) -> list[Devbox]:
        page = self._client.devboxes.list(
            **params,
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
        **params: Unpack[SDKDiskSnapshotListParams],
    ) -> list[Snapshot]:
        page = self._client.devboxes.disk_snapshots.list(
            **params,
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
        >>> blueprint = sdk.blueprint.create(name="my-blueprint", dockerfile="FROM ubuntu:22.04\\nRUN apt-get update")
        >>> blueprints = sdk.blueprint.list()
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def create(
        self,
        **params: Unpack[SDKBlueprintCreateParams],
    ) -> Blueprint:
        blueprint = self._client.blueprints.create_and_await_build_complete(
            **params,
        )
        return Blueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> Blueprint:
        return Blueprint(self._client, blueprint_id)

    def list(
        self,
        **params: Unpack[SDKBlueprintListParams],
    ) -> list[Blueprint]:
        page = self._client.blueprints.list(
            **params,
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
        **params: Unpack[SDKObjectCreateParams],
    ) -> StorageObject:
        obj = self._client.objects.create(**params)
        return StorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> StorageObject:
        return StorageObject(self._client, object_id, upload_url=None)

    def list(
        self,
        **params: Unpack[SDKObjectListParams],
    ) -> list[StorageObject]:
        page = self._client.objects.list(
            **params,
        )
        return [StorageObject(self._client, item.id, upload_url=item.upload_url) for item in page.objects]

    def upload_from_file(
        self,
        file_path: str | Path,
        name: str | None = None,
        *,
        content_type: ContentType | None = None,
        metadata: Optional[Dict[str, str]] = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
        path = Path(file_path)

        try:
            content = path.read_bytes()
        except OSError as error:
            raise OSError(f"Failed to read file {path}: {error}") from error

        name = name or path.name
        content_type = content_type or detect_content_type(str(file_path))
        obj = self.create(name=name, content_type=content_type, metadata=metadata, **options)
        obj.upload_content(content)
        obj.complete()
        return obj

    def upload_from_text(
        self,
        text: str,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
        obj = self.create(name=name, content_type="text", metadata=metadata, **options)
        obj.upload_content(text)
        obj.complete()
        return obj

    def upload_from_bytes(
        self,
        data: bytes,
        name: str,
        *,
        content_type: ContentType,
        metadata: Optional[Dict[str, str]] = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
        obj = self.create(name=name, content_type=content_type, metadata=metadata, **options)
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
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
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
