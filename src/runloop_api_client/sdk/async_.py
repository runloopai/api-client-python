"""Asynchronous SDK entry points and management interfaces."""

from __future__ import annotations

import asyncio
from typing import Dict, Mapping, Optional, Sequence
from pathlib import Path
from datetime import timedelta
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
    SDKDevboxCreateFromImageParams,
)
from .._types import Timeout, NotGiven, not_given
from .._client import DEFAULT_MAX_RETRIES, AsyncRunloop
from ._helpers import detect_content_type
from ..lib._ignore import IgnoreMatcher, TarFilterMatcher, FilePatternMatcher
from .async_devbox import AsyncDevbox
from .async_snapshot import AsyncSnapshot
from .async_blueprint import AsyncBlueprint
from ..lib.context_loader import build_directory_tar
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

        :param client: Generated AsyncRunloop client to wrap
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKDevboxCreateParams],
    ) -> AsyncDevbox:
        """Provision a new devbox and wait until it reaches ``running`` state.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: AsyncDevbox
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_id(
        self,
        blueprint_id: str,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> AsyncDevbox:
        """Create a devbox from an existing blueprint by identifier.

        :param blueprint_id: Blueprint ID to create from
        :type blueprint_id: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: AsyncDevbox
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_name(
        self,
        blueprint_name: str,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> AsyncDevbox:
        """Create a devbox from the latest blueprint with the given name.

        :param blueprint_name: Blueprint name to create from
        :type blueprint_name: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: AsyncDevbox
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_name=blueprint_name,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_snapshot(
        self,
        snapshot_id: str,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> AsyncDevbox:
        """Create a devbox initialized from a snapshot.

        :param snapshot_id: Snapshot ID to create from
        :type snapshot_id: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: AsyncDevbox
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> AsyncDevbox:
        """Attach to an existing devbox by ID.

        Returns immediately without waiting for the devbox to reach ``running``
        state. Call ``await_running()`` on the returned :class:`AsyncDevbox` if
        you need to wait for readiness (contrast with the synchronous SDK, which blocks).

        :param devbox_id: Existing devbox ID
        :type devbox_id: str
        :return: Wrapper bound to the requested devbox
        :rtype: AsyncDevbox
        """
        return AsyncDevbox(self._client, devbox_id)

    async def list(
        self,
        **params: Unpack[SDKDevboxListParams],
    ) -> list[AsyncDevbox]:
        """List devboxes accessible to the caller.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxListParams` for available parameters
        :return: Collection of devbox wrappers
        :rtype: list[AsyncDevbox]
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

        :param client: Generated AsyncRunloop client to wrap
        :type client: AsyncRunloop
        """
        self._client = client

    async def list(
        self,
        **params: Unpack[SDKDiskSnapshotListParams],
    ) -> list[AsyncSnapshot]:
        """List snapshots created from devboxes.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDiskSnapshotListParams` for available parameters
        :return: Snapshot wrappers for each record
        :rtype: list[AsyncSnapshot]
        """
        page = await self._client.devboxes.disk_snapshots.list(
            **params,
        )
        return [AsyncSnapshot(self._client, item.id) for item in page.snapshots]

    def from_id(self, snapshot_id: str) -> AsyncSnapshot:
        """Return a snapshot wrapper for the given ID.

        :param snapshot_id: Snapshot ID to wrap
        :type snapshot_id: str
        :return: Wrapper for the snapshot resource
        :rtype: AsyncSnapshot
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

        :param client: Generated AsyncRunloop client to wrap
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKBlueprintCreateParams],
    ) -> AsyncBlueprint:
        """Create a blueprint and wait for the build to finish.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBlueprintCreateParams` for available parameters
        :return: Wrapper bound to the finished blueprint
        :rtype: AsyncBlueprint
        """
        blueprint = await self._client.blueprints.create_and_await_build_complete(
            **params,
        )
        return AsyncBlueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> AsyncBlueprint:
        """Return a blueprint wrapper for the given ID.

        :param blueprint_id: Blueprint ID to wrap
        :type blueprint_id: str
        :return: Wrapper for the blueprint resource
        :rtype: AsyncBlueprint
        """
        return AsyncBlueprint(self._client, blueprint_id)

    async def list(
        self,
        **params: Unpack[SDKBlueprintListParams],
    ) -> list[AsyncBlueprint]:
        """List available blueprints.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBlueprintListParams` for available parameters
        :return: Blueprint wrappers for each record
        :rtype: list[AsyncBlueprint]
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

        :param client: Generated AsyncRunloop client to wrap
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKObjectCreateParams],
    ) -> AsyncStorageObject:
        """Create a storage object and obtain an upload URL.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectCreateParams` for available parameters
        :return: Wrapper with upload URL set for immediate uploads
        :rtype: AsyncStorageObject
        """
        obj = await self._client.objects.create(**params)
        return AsyncStorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> AsyncStorageObject:
        """Return a storage object wrapper by identifier.

        :param object_id: Storage object identifier to wrap
        :type object_id: str
        :return: Wrapper for the storage object resource
        :rtype: AsyncStorageObject
        """
        return AsyncStorageObject(self._client, object_id, upload_url=None)

    async def list(
        self,
        **params: Unpack[SDKObjectListParams],
    ) -> list[AsyncStorageObject]:
        """List storage objects owned by the caller.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectListParams` for available parameters
        :return: Storage object wrappers for each record
        :rtype: list[AsyncStorageObject]
        """
        page = await self._client.objects.list(
            **params,
        )
        return [AsyncStorageObject(self._client, item.id, upload_url=item.upload_url) for item in page.objects]

    async def upload_from_file(
        self,
        file_path: str | Path,
        *,
        name: Optional[str] = None,
        content_type: Optional[ContentType] = None,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        """Create and upload an object from a local file path.

        :param file_path: Local filesystem path to read
        :type file_path: str | Path
        :param name: Optional object name; defaults to the file name
        :type name: Optional[str]
        :param content_type: Optional MIME type to apply to the object
        :type content_type: Optional[ContentType]
        :param metadata: Optional key-value metadata
        :type metadata: Optional[Dict[str, str]]
        :param ttl: Optional Time-To-Live, after which the object is automatically deleted
        :type ttl: Optional[timedelta]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Wrapper for the uploaded object
        :rtype: AsyncStorageObject
        :raises OSError: If the local file cannot be read
        """
        path = Path(file_path)

        try:
            content = await asyncio.to_thread(lambda: path.read_bytes())
        except OSError as error:
            raise OSError(f"Failed to read file {path}: {error}") from error

        name = name or path.name
        content_type = content_type or detect_content_type(str(file_path))
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None
        obj = await self.create(name=name, content_type=content_type, metadata=metadata, ttl_ms=ttl_ms, **options)
        await obj.upload_content(content)
        await obj.complete()
        return obj

    async def upload_from_dir(
        self,
        dir_path: str | Path,
        *,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        ignore: IgnoreMatcher | Sequence[str] | str | None = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        """Create and upload an object from a local directory.

        The resulting object will be uploaded as a compressed tarball.

        :param dir_path: Local filesystem directory path to tar
        :type dir_path: str | Path
        :param name: Optional object name; defaults to the directory name + '.tar.gz'
        :type name: Optional[str]
        :param metadata: Optional key-value metadata
        :type metadata: Optional[Dict[str, str]]
        :param ttl: Optional Time-To-Live, after which the object is automatically deleted
        :type ttl: Optional[timedelta]
        :param ignore: Optional ignore configuration controlling which files from
            ``dir_path`` are included in the uploaded tarball. This may be:

            - An :class:`~runloop_api_client.lib._ignore.IgnoreMatcher`
              implementation such as :class:`~runloop_api_client.lib._ignore.DockerIgnoreMatcher`
              or :class:`~runloop_api_client.lib._ignore.FilePatternMatcher`.
            - A single pattern string.
            - A sequence of pattern strings.

            Patterns follow Docker-style semantics (``!`` negation, ``**`` support).
        :type ignore: Optional[IgnoreMatcher | Sequence[str] | str]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions`
            for available options
        :return: Wrapper for the uploaded object
        :rtype: AsyncStorageObject
        :raises OSError: If the local file cannot be read
        """
        path = Path(dir_path)
        if not path.is_dir():
            raise ValueError(f"dir_path must be a directory, got: {path}")

        name = name or f"{path.name}.tar.gz"
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None

        def synchronous_io() -> bytes:
            matcher: IgnoreMatcher | None
            if ignore is None:
                matcher = None
            elif isinstance(ignore, IgnoreMatcher):
                matcher = ignore
            else:
                matcher = FilePatternMatcher(ignore)  # type: ignore[arg-type]

            if matcher is None:
                return build_directory_tar(path)
            return build_directory_tar(path, tar_filter=TarFilterMatcher(path, matcher))

        tar_bytes = await asyncio.to_thread(synchronous_io)

        obj = await self.create(name=name, content_type="tgz", metadata=metadata, ttl_ms=ttl_ms, **options)
        await obj.upload_content(tar_bytes)
        await obj.complete()
        return obj

    async def upload_from_text(
        self,
        text: str,
        *,
        name: str,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        """Create and upload an object from a text payload.

        :param text: Text content to upload
        :type text: str
        :param name: Object display name
        :type name: str
        :param metadata: Optional key-value metadata
        :type metadata: Optional[Dict[str, str]]
        :param ttl: Optional Time-To-Live, after which the object is automatically deleted
        :type ttl: Optional[timedelta]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Wrapper for the uploaded object
        :rtype: AsyncStorageObject
        """
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None
        obj = await self.create(name=name, content_type="text", metadata=metadata, ttl_ms=ttl_ms, **options)
        await obj.upload_content(text)
        await obj.complete()
        return obj

    async def upload_from_bytes(
        self,
        data: bytes,
        *,
        name: str,
        content_type: ContentType,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        **options: Unpack[LongRequestOptions],
    ) -> AsyncStorageObject:
        """Create and upload an object from a bytes payload.

        :param data: Binary payload to upload
        :type data: bytes
        :param name: Object display name
        :type name: str
        :param content_type: MIME type describing the payload
        :type content_type: ContentType
        :param metadata: Optional key-value metadata
        :type metadata: Optional[Dict[str, str]]
        :param ttl: Optional Time-To-Live, after which the object is automatically deleted
        :type ttl: Optional[timedelta]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Wrapper for the uploaded object
        :rtype: AsyncStorageObject
        """
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None
        obj = await self.create(name=name, content_type=content_type, metadata=metadata, ttl_ms=ttl_ms, **options)
        await obj.upload_content(data)
        await obj.complete()
        return obj


class AsyncRunloopSDK:
    """High-level asynchronous entry point for the Runloop SDK.

    Provides a Pythonic, object-oriented interface for managing devboxes,
    blueprints, snapshots, and storage objects. Exposes the generated async REST
    client via the ``api`` attribute for advanced use cases.

    :ivar api: Direct access to the generated async REST API client
    :vartype api: AsyncRunloop
    :ivar devbox: High-level async interface for devbox management
    :vartype devbox: AsyncDevboxOps
    :ivar blueprint: High-level async interface for blueprint management
    :vartype blueprint: AsyncBlueprintOps
    :ivar snapshot: High-level async interface for snapshot management
    :vartype snapshot: AsyncSnapshotOps
    :ivar storage_object: High-level async interface for storage object management
    :vartype storage_object: AsyncStorageObjectOps

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

        :param bearer_token: API token; falls back to ``RUNLOOP_API_KEY`` env var, defaults to None
        :type bearer_token: str | None, optional
        :param base_url: Override the API base URL, defaults to None
        :type base_url: str | httpx.URL | None, optional
        :param timeout: Request timeout (seconds) or ``Timeout`` object, defaults to not_given
        :type timeout: float | Timeout | None | NotGiven, optional
        :param max_retries: Maximum automatic retry attempts, defaults to DEFAULT_MAX_RETRIES
        :type max_retries: int, optional
        :param default_headers: Headers merged into every request, defaults to None
        :type default_headers: Mapping[str, str] | None, optional
        :param default_query: Default query parameters merged into every request, defaults to None
        :type default_query: Mapping[str, object] | None, optional
        :param http_client: Custom ``httpx.AsyncClient`` instance to reuse, defaults to None
        :type http_client: httpx.AsyncClient | None, optional
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

        :return: The active SDK instance
        :rtype: AsyncRunloopSDK
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Ensure the API client closes when leaving the context manager."""
        await self.aclose()
