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


class DevboxOps:
    """High-level manager for creating and managing Devbox instances.

    Accessed via ``runloop.devbox`` from :class:`RunloopSDK`, provides methods to
    create devboxes from scratch, blueprints, or snapshots, and to list
    existing devboxes.

    Example:
        >>> runloop = RunloopSDK()
        >>> devbox = runloop.devbox.create(name="my-devbox")
        >>> devboxes = runloop.devbox.list(limit=10)
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize the manager.

        Args:
            client: Generated Runloop client to wrap.
        """
        self._client = client

    def create(
        self,
        **params: Unpack[SDKDevboxCreateParams],
    ) -> Devbox:
        """Provision a new devbox and wait until it reaches ``running`` state.

        Args:
            **params: Keyword arguments forwarded to the devbox creation API.

        Returns:
            Devbox: Wrapper bound to the newly created devbox.
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_id(
        self,
        blueprint_id: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> Devbox:
        """Create a devbox from an existing blueprint by identifier.

        Args:
            blueprint_id: Blueprint ID to create from.
            **params: Additional creation parameters (metadata, launch parameters, etc.).

        Returns:
            Devbox: Wrapper bound to the newly created devbox.
        """
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
        """Create a devbox from the latest blueprint with the given name.

        Args:
            blueprint_name: Blueprint name to create from.
            **params: Additional creation parameters (metadata, launch parameters, etc.).

        Returns:
            Devbox: Wrapper bound to the newly created devbox.
        """
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
        """Create a devbox initialized from a snapshot.

        Args:
            snapshot_id: Snapshot ID to create from.
            **params: Additional creation parameters (metadata, launch parameters, etc.).

        Returns:
            Devbox: Wrapper bound to the newly created devbox.
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> Devbox:
        """Attach to an existing devbox by ID.

        Args:
            devbox_id: Existing devbox ID.

        Returns:
            Devbox: Wrapper bound to the requested devbox.
        """
        self._client.devboxes.await_running(devbox_id)
        return Devbox(self._client, devbox_id)

    def list(
        self,
        **params: Unpack[SDKDevboxListParams],
    ) -> list[Devbox]:
        """List devboxes accessible to the caller.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[Devbox]: Collection of devbox wrappers.
        """
        page = self._client.devboxes.list(
            **params,
        )
        return [Devbox(self._client, item.id) for item in page.devboxes]


class SnapshotOps:
    """High-level manager for working with disk snapshots.

    Accessed via ``runloop.snapshot`` from :class:`RunloopSDK`, provides methods
    to list snapshots and access snapshot details.

    Example:
        >>> runloop = RunloopSDK()
        >>> snapshots = runloop.snapshot.list(devbox_id="dev-123")
        >>> snapshot = runloop.snapshot.from_id("snap-123")
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize the manager with the generated Runloop client."""
        self._client = client

    def list(
        self,
        **params: Unpack[SDKDiskSnapshotListParams],
    ) -> list[Snapshot]:
        """List snapshots created from devboxes.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[Snapshot]: Snapshot wrappers for each record.
        """
        page = self._client.devboxes.disk_snapshots.list(
            **params,
        )
        return [Snapshot(self._client, item.id) for item in page.snapshots]

    def from_id(self, snapshot_id: str) -> Snapshot:
        """Return a snapshot wrapper for the given ID.

        Args:
            snapshot_id: Snapshot ID to wrap.

        Returns:
            Snapshot: Wrapper for the snapshot resource.
        """
        return Snapshot(self._client, snapshot_id)


class BlueprintOps:
    """High-level manager for creating and managing blueprints.

    Accessed via ``runloop.blueprint`` from :class:`RunloopSDK`, provides methods
    to create blueprints with Dockerfiles and system setup commands, and to
    list existing blueprints.

    Example:
        >>> runloop = RunloopSDK()
        >>> blueprint = runloop.blueprint.create(
        ...     name="my-blueprint", dockerfile="FROM ubuntu:22.04\\nRUN apt-get update"
        ... )
        >>> blueprints = runloop.blueprint.list()
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize the manager.

        Args:
            client: Generated Runloop client to wrap.
        """
        self._client = client

    def create(
        self,
        **params: Unpack[SDKBlueprintCreateParams],
    ) -> Blueprint:
        """Create a blueprint and wait for the build to finish.

        Args:
            **params: Blueprint definition (Dockerfile, metadata, etc.).

        Returns:
            Blueprint: Wrapper bound to the finished blueprint.
        """
        blueprint = self._client.blueprints.create_and_await_build_complete(
            **params,
        )
        return Blueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> Blueprint:
        """Return a blueprint wrapper for the given ID.

        Args:
            blueprint_id: Blueprint ID to wrap.

        Returns:
            Blueprint: Wrapper for the blueprint resource.
        """
        return Blueprint(self._client, blueprint_id)

    def list(
        self,
        **params: Unpack[SDKBlueprintListParams],
    ) -> list[Blueprint]:
        """List available blueprints.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[Blueprint]: Blueprint wrappers for each record.
        """
        page = self._client.blueprints.list(
            **params,
        )
        return [Blueprint(self._client, item.id) for item in page.blueprints]


class StorageObjectOps:
    """High-level manager for creating and managing storage objects.

    Accessed via ``runloop.storage_object`` from :class:`RunloopSDK`, provides
    methods to create, upload, download, and list storage objects with convenient
    helpers for file and text uploads.

    Example:
        >>> runloop = RunloopSDK()
        >>> obj = runloop.storage_object.upload_from_text("Hello!", "greeting.txt")
        >>> content = obj.download_as_text()
        >>> objects = runloop.storage_object.list()
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize the manager with the generated Runloop client."""
        self._client = client

    def create(
        self,
        **params: Unpack[SDKObjectCreateParams],
    ) -> StorageObject:
        """Create a storage object and obtain an upload URL.

        Args:
            **params: Object creation parameters (name, content type, metadata).

        Returns:
            StorageObject: Wrapper with upload URL set for immediate uploads.
        """
        obj = self._client.objects.create(**params)
        return StorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> StorageObject:
        """Return a storage object wrapper by identifier.

        Args:
            object_id: Storage object identifier to wrap.

        Returns:
            StorageObject: Wrapper for the storage object resource.
        """
        return StorageObject(self._client, object_id, upload_url=None)

    def list(
        self,
        **params: Unpack[SDKObjectListParams],
    ) -> list[StorageObject]:
        """List storage objects owned by the caller.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[StorageObject]: Storage object wrappers for each record.
        """
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
        """Create and upload an object from a local file path.

        Args:
            file_path: Local filesystem path to read.
            name: Optional object name; defaults to the file name.
            content_type: Optional MIME type to apply to the object.
            metadata: Optional key-value metadata.
            **options: Additional request configuration.

        Returns:
            StorageObject: Wrapper for the uploaded object.

        Raises:
            OSError: If the local file cannot be read.
        """
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
        """Create and upload an object from a text payload.

        Args:
            text: Text content to upload.
            name: Object display name.
            metadata: Optional key-value metadata.
            **options: Additional request configuration.

        Returns:
            StorageObject: Wrapper for the uploaded object.
        """
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
        """Create and upload an object from a bytes payload.

        Args:
            data: Binary payload to upload.
            name: Object display name.
            content_type: MIME type describing the payload.
            metadata: Optional key-value metadata.
            **options: Additional request configuration.

        Returns:
            StorageObject: Wrapper for the uploaded object.
        """
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
        >>> runloop = RunloopSDK()  # Uses RUNLOOP_API_KEY env var
        >>> devbox = runloop.devbox.create(name="my-devbox")
        >>> result = devbox.cmd.exec(command="echo 'hello'")
        >>> print(result.stdout())
        >>> devbox.shutdown()
    """

    api: Runloop
    devbox: DevboxOps
    blueprint: BlueprintOps
    snapshot: SnapshotOps
    storage_object: StorageObjectOps

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
        """Configure the synchronous SDK wrapper.

        Args:
            bearer_token: API token; falls back to ``RUNLOOP_API_KEY`` env var.
            base_url: Override the API base URL.
            timeout: Request timeout (seconds) or ``Timeout`` object.
            max_retries: Maximum automatic retry attempts.
            default_headers: Headers merged into every request.
            default_query: Default query parameters merged into every request.
            http_client: Custom ``httpx.Client`` instance to reuse.
        """
        self.api = Runloop(
            bearer_token=bearer_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
        )

        self.devbox = DevboxOps(self.api)
        self.blueprint = BlueprintOps(self.api)
        self.snapshot = SnapshotOps(self.api)
        self.storage_object = StorageObjectOps(self.api)

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self.api.close()

    def __enter__(self) -> "RunloopSDK":
        """Allow ``with RunloopSDK() as runloop`` usage.

        Returns:
            RunloopSDK: The active SDK instance.
        """
        return self

    def __exit__(self, *_exc_info: object) -> None:
        """Ensure the API client closes when leaving the context manager."""
        self.close()
