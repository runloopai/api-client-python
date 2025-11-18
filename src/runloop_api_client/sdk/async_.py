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


class AsyncDevboxOps:
    """High-level async manager for creating and managing AsyncDevbox instances.

    Accessed via ``runloop.devbox`` from :class:`AsyncRunloopSDK`, provides
    coroutines to create devboxes from scratch, blueprints, or snapshots, and to
    list existing devboxes.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> devbox = await runloop.devbox.create(name="my-devbox")
        >>> devboxes = await runloop.devbox.list(limit=10)
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize the manager.

        Args:
            client: Generated AsyncRunloop client to wrap.
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKDevboxCreateParams],
    ) -> AsyncDevbox:
        """Provision a new devbox and wait until it reaches ``running`` state.

        Args:
            **params: Keyword arguments forwarded to the devbox creation API.

        Returns:
            AsyncDevbox: Wrapper bound to the newly created devbox.
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_id(
        self,
        blueprint_id: str,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> AsyncDevbox:
        """Create a devbox from an existing blueprint by identifier.

        Args:
            blueprint_id: Blueprint ID to create from.
            **params: Additional creation parameters (metadata, launch parameters, etc.).

        Returns:
            AsyncDevbox: Wrapper bound to the newly created devbox.
        """
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
        """Create a devbox from the latest blueprint with the given name.

        Args:
            blueprint_name: Blueprint name to create from.
            **params: Additional creation parameters (metadata, launch parameters, etc.).

        Returns:
            AsyncDevbox: Wrapper bound to the newly created devbox.
        """
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
        """Create a devbox initialized from a snapshot.

        Args:
            snapshot_id: Snapshot ID to create from.
            **params: Additional creation parameters (metadata, launch parameters, etc.).

        Returns:
            AsyncDevbox: Wrapper bound to the newly created devbox.
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> AsyncDevbox:
        """Attach to an existing devbox by ID.

        Args:
            devbox_id: Existing devbox ID.

        Returns:
            AsyncDevbox: Wrapper bound to the requested devbox.
        """
        return AsyncDevbox(self._client, devbox_id)

    async def list(
        self,
        **params: Unpack[SDKDevboxListParams],
    ) -> list[AsyncDevbox]:
        """List devboxes accessible to the caller.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[AsyncDevbox]: Collection of devbox wrappers.
        """
        page = await self._client.devboxes.list(
            **params,
        )
        return [AsyncDevbox(self._client, item.id) for item in page.devboxes]


class AsyncSnapshotOps:
    """High-level async manager for working with disk snapshots.

    Accessed via ``runloop.snapshot`` from :class:`AsyncRunloopSDK`, provides
    coroutines to list snapshots and access snapshot details.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> snapshots = await runloop.snapshot.list(devbox_id="dev-123")
        >>> snapshot = await runloop.snapshot.from_id("snap-123")
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize the manager.

        Args:
            client: Generated AsyncRunloop client to wrap.
        """
        self._client = client

    async def list(
        self,
        **params: Unpack[SDKDiskSnapshotListParams],
    ) -> list[AsyncSnapshot]:
        """List snapshots created from devboxes.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[AsyncSnapshot]: Snapshot wrappers for each record.
        """
        page = await self._client.devboxes.disk_snapshots.list(
            **params,
        )
        return [AsyncSnapshot(self._client, item.id) for item in page.snapshots]

    def from_id(self, snapshot_id: str) -> AsyncSnapshot:
        """Return a snapshot wrapper for the given ID.

        Args:
            snapshot_id: Snapshot ID to wrap.

        Returns:
            AsyncSnapshot: Wrapper for the snapshot resource.
        """
        return AsyncSnapshot(self._client, snapshot_id)


class AsyncBlueprintOps:
    """High-level async manager for creating and managing blueprints.

    Accessed via ``runloop.blueprint`` from :class:`AsyncRunloopSDK`, provides
    coroutines to create Dockerfile-based blueprints, inspect build logs,
    and list existing blueprints.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> blueprint = await runloop.blueprint.create(
        ...     name="my-blueprint",
        ...     dockerfile="FROM ubuntu:22.04\\nRUN apt-get update",
        ... )
        >>> blueprints = await runloop.blueprint.list()
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize the manager.

        Args:
            client: Generated AsyncRunloop client to wrap.
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKBlueprintCreateParams],
    ) -> AsyncBlueprint:
        """Create a blueprint and wait for the build to finish.

        Args:
            **params: Blueprint definition (Dockerfile, metadata, etc.).

        Returns:
            AsyncBlueprint: Wrapper bound to the finished blueprint.
        """
        blueprint = await self._client.blueprints.create_and_await_build_complete(
            **params,
        )
        return AsyncBlueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> AsyncBlueprint:
        """Return a blueprint wrapper for the given ID.

        Args:
            blueprint_id: Blueprint ID to wrap.

        Returns:
            AsyncBlueprint: Wrapper for the blueprint resource.
        """
        return AsyncBlueprint(self._client, blueprint_id)

    async def list(
        self,
        **params: Unpack[SDKBlueprintListParams],
    ) -> list[AsyncBlueprint]:
        """List available blueprints.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[AsyncBlueprint]: Blueprint wrappers for each record.
        """
        page = await self._client.blueprints.list(
            **params,
        )
        return [AsyncBlueprint(self._client, item.id) for item in page.blueprints]


class AsyncStorageObjectOps:
    """High-level async manager for creating and managing storage objects.

    Accessed via ``runloop.storage_object`` from :class:`AsyncRunloopSDK`, provides
    coroutines to create, upload, download, and list storage objects with convenient
    helpers for file and text uploads.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> obj = await runloop.storage_object.upload_from_text("Hello!", "greeting.txt")
        >>> content = await obj.download_as_text()
        >>> objects = await runloop.storage_object.list()
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize the manager.

        Args:
            client: Generated AsyncRunloop client to wrap.
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKObjectCreateParams],
    ) -> AsyncStorageObject:
        """Create a storage object and obtain an upload URL.

        Args:
            **params: Object creation parameters (name, content type, metadata).

        Returns:
            AsyncStorageObject: Wrapper with upload URL set for immediate uploads.
        """
        obj = await self._client.objects.create(**params)
        return AsyncStorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> AsyncStorageObject:
        """Return a storage object wrapper by identifier.

        Args:
            object_id: Storage object identifier to wrap.

        Returns:
            AsyncStorageObject: Wrapper for the storage object resource.
        """
        return AsyncStorageObject(self._client, object_id, upload_url=None)

    async def list(
        self,
        **params: Unpack[SDKObjectListParams],
    ) -> list[AsyncStorageObject]:
        """List storage objects owned by the caller.

        Args:
            **params: Filtering and pagination parameters.

        Returns:
            list[AsyncStorageObject]: Storage object wrappers for each record.
        """
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
        """Create and upload an object from a local file path.

        Args:
            file_path: Local filesystem path to read.
            name: Optional object name; defaults to the file name.
            content_type: Optional MIME type to apply to the object.
            metadata: Optional key-value metadata.
            **options: Additional request configuration.

        Returns:
            AsyncStorageObject: Wrapper for the uploaded object.

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
        """Create and upload an object from a text payload.

        Args:
            text: Text content to upload.
            name: Object display name.
            metadata: Optional key-value metadata.
            **options: Additional request configuration.

        Returns:
            AsyncStorageObject: Wrapper for the uploaded object.
        """
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
        """Create and upload an object from a bytes payload.

        Args:
            data: Binary payload to upload.
            name: Object display name.
            content_type: MIME type describing the payload.
            metadata: Optional key-value metadata.
            **options: Additional request configuration.

        Returns:
            AsyncStorageObject: Wrapper for the uploaded object.
        """
        obj = await self.create(name=name, content_type=content_type, metadata=metadata, **options)
        await obj.upload_content(data)
        await obj.complete()
        return obj


class AsyncRunloopSDK:
    """High-level asynchronous entry point for the Runloop SDK.

    Provides a Pythonic, object-oriented interface for managing devboxes,
    blueprints, snapshots, and storage objects. Exposes the generated async REST
    client via the ``api`` attribute for advanced use cases.

    Attributes:
        api: Direct access to the generated async REST API client.
        devbox: High-level async interface for devbox management.
        blueprint: High-level async interface for blueprint management.
        snapshot: High-level async interface for snapshot management.
        storage_object: High-level async interface for storage object management.

    Example:
        >>> runloop = AsyncRunloopSDK()  # Uses RUNLOOP_API_KEY env var
        >>> devbox = await runloop.devbox.create(name="my-devbox")
        >>> result = await devbox.cmd.exec(command="echo 'hello'")
        >>> print(await result.stdout())
        >>> await devbox.shutdown()
    """

    api: AsyncRunloop
    devbox: AsyncDevboxOps
    blueprint: AsyncBlueprintOps
    snapshot: AsyncSnapshotOps
    storage_object: AsyncStorageObjectOps

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
        """Configure the asynchronous SDK wrapper.

        Args:
            bearer_token: API token; falls back to ``RUNLOOP_API_KEY`` env var.
            base_url: Override the API base URL.
            timeout: Request timeout (seconds) or ``Timeout`` object.
            max_retries: Maximum automatic retry attempts.
            default_headers: Headers merged into every request.
            default_query: Default query parameters merged into every request.
            http_client: Custom ``httpx.AsyncClient`` instance to reuse.
        """
        self.api = AsyncRunloop(
            bearer_token=bearer_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
        )

        self.devbox = AsyncDevboxOps(self.api)
        self.blueprint = AsyncBlueprintOps(self.api)
        self.snapshot = AsyncSnapshotOps(self.api)
        self.storage_object = AsyncStorageObjectOps(self.api)

    async def aclose(self) -> None:
        """Close the underlying HTTP client and release resources."""
        await self.api.close()

    async def __aenter__(self) -> "AsyncRunloopSDK":
        """Allow ``async with AsyncRunloopSDK() as runloop`` usage.

        Returns:
            AsyncRunloopSDK: The active SDK instance.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Ensure the API client closes when leaving the context manager."""
        await self.aclose()
