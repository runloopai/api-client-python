"""Asynchronous SDK entry points and management interfaces."""

from __future__ import annotations

import asyncio
from typing import Dict, Mapping, Optional
from pathlib import Path
from datetime import timedelta
from typing_extensions import Unpack

import httpx

from ._types import (
    LongRequestOptions,
    SDKAgentListParams,
    SDKDevboxListParams,
    SDKObjectListParams,
    SDKScorerListParams,
    SDKAgentCreateParams,
    SDKDevboxCreateParams,
    SDKObjectCreateParams,
    SDKScenarioListParams,
    SDKScorerCreateParams,
    SDKBenchmarkListParams,
    SDKBlueprintListParams,
    SDKBenchmarkCreateParams,
    SDKBlueprintCreateParams,
    SDKDiskSnapshotListParams,
    SDKNetworkPolicyListParams,
    SDKNetworkPolicyCreateParams,
    SDKDevboxCreateFromImageParams,
)
from .._types import Timeout, NotGiven, not_given
from .._client import DEFAULT_MAX_RETRIES, AsyncRunloop
from ._helpers import detect_content_type
from .async_agent import AsyncAgent
from .async_devbox import AsyncDevbox
from .async_scorer import AsyncScorer
from .async_scenario import AsyncScenario
from .async_snapshot import AsyncSnapshot
from .async_benchmark import AsyncBenchmark
from .async_blueprint import AsyncBlueprint
from ..lib.context_loader import TarFilter, build_directory_tar
from .async_network_policy import AsyncNetworkPolicy
from .async_storage_object import AsyncStorageObject
from .async_scenario_builder import AsyncScenarioBuilder
from ..types.object_create_params import ContentType
from ..types.shared_params.agent_source import Git, Npm, Pip, Object


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

    To use a local directory as a build context, use an object.

    Example:
        >>> from datetime import timedelta
        >>> from runloop_api_client.types.blueprint_build_parameters import BuildContext
        >>> runloop = AsyncRunloopSDK()
        >>> obj = await runloop.object_storage.upload_from_dir(
        ...     "./",
        ...     ttl=timedelta(hours=1),
        ... )
        >>> blueprint = await runloop.blueprint.create(
        ...     name="my-blueprint",
        ...     dockerfile="FROM ubuntu:22.04\\nCOPY . .\\n",
        ...     build_context=BuildContext(type="object", object_id=obj.id),
        ... )
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
        ignore: TarFilter | None = None,
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
        :param ignore: Optional tar filter function compatible with
            :meth:`tarfile.TarFile.add`. If provided, it will be called for each
            member to allow modification or exclusion (by returning ``None``).
        :type ignore: Optional[TarFilter]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions`
            for available options
        :return: Wrapper for the uploaded object
        :rtype: AsyncStorageObject
        :raises OSError: If the local directory cannot be read
        :raises ValueError: If ``dir_path`` does not point to a directory
        """
        path = Path(dir_path)
        if not path.is_dir():
            raise ValueError(f"dir_path must be a directory, got: {path}")

        name = name or f"{path.name}.tar.gz"
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None

        def synchronous_io() -> bytes:
            return build_directory_tar(path, tar_filter=ignore)

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


class AsyncScorerOps:
    """Create and manage custom scorers (async). Access via ``runloop.scorer``.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> scorer = await runloop.scorer.create(type="my_scorer", bash_script="echo 'score=1.0'")
        >>> all_scorers = await runloop.scorer.list()
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize AsyncScorerOps.

        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(self, **params: Unpack[SDKScorerCreateParams]) -> AsyncScorer:
        """Create a new scorer with the given type and bash script.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerCreateParams` for available parameters
        :return: The newly created scorer
        :rtype: AsyncScorer
        """
        response = await self._client.scenarios.scorers.create(**params)
        return AsyncScorer(self._client, response.id)

    def from_id(self, scorer_id: str) -> AsyncScorer:
        """Get an AsyncScorer instance for an existing scorer ID.

        :param scorer_id: ID of the scorer
        :type scorer_id: str
        :return: AsyncScorer instance for the given ID
        :rtype: AsyncScorer
        """
        return AsyncScorer(self._client, scorer_id)

    async def list(self, **params: Unpack[SDKScorerListParams]) -> list[AsyncScorer]:
        """List all scorers, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerListParams` for available parameters
        :return: List of scorers
        :rtype: list[AsyncScorer]
        """
        page = await self._client.scenarios.scorers.list(**params)
        return [AsyncScorer(self._client, item.id) async for item in page]


class AsyncAgentOps:
    """High-level async manager for creating and managing agents.

    Accessed via ``runloop.agent`` from :class:`AsyncRunloopSDK`, provides
    coroutines to create, retrieve, and list agents from various sources (npm, pip, git, object storage).

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> # Create agent from NPM package
        >>> agent = await runloop.agent.create_from_npm(name="my-agent", package_name="@runloop/example-agent")
        >>> # Create agent from Git repository
        >>> agent = await runloop.agent.create_from_git(
        ...     name="git-agent", repository="https://github.com/user/agent-repo", ref="main"
        ... )
        >>> # List all agents
        >>> agents = await runloop.agent.list(limit=10)
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize the manager.

        :param client: Generated AsyncRunloop client to wrap
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(
        self,
        **params: Unpack[SDKAgentCreateParams],
    ) -> AsyncAgent:
        """Create a new agent.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for available parameters
        :return: Wrapper bound to the newly created agent
        :rtype: AsyncAgent
        """
        agent_view = await self._client.agents.create(
            **params,
        )
        return AsyncAgent(self._client, agent_view.id, agent_view)

    async def create_from_npm(
        self,
        *,
        package_name: str,
        registry_url: Optional[str] = None,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> AsyncAgent:
        """Create an agent from an NPM package.

        :param package_name: NPM package name
        :type package_name: str
        :param registry_url: NPM registry URL, defaults to None
        :type registry_url: Optional[str], optional
        :param agent_setup: Setup commands to run after installation, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: AsyncAgent
        :raises ValueError: If 'source' is provided in params
        """
        if "source" in params:
            raise ValueError(
                "Cannot specify 'source' when using create_from_npm(); source is automatically set to npm configuration"
            )

        npm_config: Npm = {"package_name": package_name}
        if registry_url is not None:
            npm_config["registry_url"] = registry_url
        if agent_setup is not None:
            npm_config["agent_setup"] = agent_setup

        params["source"] = {"type": "npm", "npm": npm_config}
        return await self.create(**params)

    async def create_from_pip(
        self,
        *,
        package_name: str,
        registry_url: Optional[str] = None,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> AsyncAgent:
        """Create an agent from a Pip package.

        :param package_name: Pip package name
        :type package_name: str
        :param registry_url: Pip registry URL, defaults to None
        :type registry_url: Optional[str], optional
        :param agent_setup: Setup commands to run after installation, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: AsyncAgent
        :raises ValueError: If 'source' is provided in params
        """
        if "source" in params:
            raise ValueError(
                "Cannot specify 'source' when using create_from_pip(); source is automatically set to pip configuration"
            )

        pip_config: Pip = {"package_name": package_name}
        if registry_url is not None:
            pip_config["registry_url"] = registry_url
        if agent_setup is not None:
            pip_config["agent_setup"] = agent_setup

        params["source"] = {"type": "pip", "pip": pip_config}
        return await self.create(**params)

    async def create_from_git(
        self,
        *,
        repository: str,
        ref: Optional[str] = None,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> AsyncAgent:
        """Create an agent from a Git repository.

        :param repository: Git repository URL
        :type repository: str
        :param ref: Optional Git ref (branch/tag/commit), defaults to main/HEAD
        :type ref: Optional[str], optional
        :param agent_setup: Setup commands to run after cloning, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: AsyncAgent
        :raises ValueError: If 'source' is provided in params
        """
        if "source" in params:
            raise ValueError(
                "Cannot specify 'source' when using create_from_git(); source is automatically set to git configuration"
            )

        git_config: Git = {"repository": repository}
        if ref is not None:
            git_config["ref"] = ref
        if agent_setup is not None:
            git_config["agent_setup"] = agent_setup

        params["source"] = {"type": "git", "git": git_config}
        return await self.create(**params)

    async def create_from_object(
        self,
        *,
        object_id: str,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> AsyncAgent:
        """Create an agent from a storage object.

        :param object_id: Storage object ID
        :type object_id: str
        :param agent_setup: Setup commands to run after unpacking, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: AsyncAgent
        :raises ValueError: If 'source' is provided in params
        """
        if "source" in params:
            raise ValueError(
                "Cannot specify 'source' when using create_from_object(); source is automatically set to object configuration"
            )

        object_config: Object = {"object_id": object_id}
        if agent_setup is not None:
            object_config["agent_setup"] = agent_setup

        params["source"] = {"type": "object", "object": object_config}
        return await self.create(**params)

    def from_id(self, agent_id: str) -> AsyncAgent:
        """Attach to an existing agent by ID.

        :param agent_id: Existing agent ID
        :type agent_id: str
        :return: Wrapper bound to the requested agent
        :rtype: AsyncAgent
        """
        return AsyncAgent(self._client, agent_id)

    async def list(
        self,
        **params: Unpack[SDKAgentListParams],
    ) -> list[AsyncAgent]:
        """List agents accessible to the caller.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentListParams` for available parameters
        :return: Collection of agent wrappers
        :rtype: list[AsyncAgent]
        """
        page = await self._client.agents.list(
            **params,
        )
        return [AsyncAgent(self._client, item.id, item) for item in page.agents]


class AsyncScenarioOps:
    """Manage scenarios (async). Access via ``runloop.scenario``.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> scenario = runloop.scenario.from_id("scn-xxx")
        >>> run = await scenario.run()
        >>> scenarios = await runloop.scenario.list()

    Example using builder:
        >>> builder = (
        ...     runloop.scenario.builder("my-scenario")
        ...     .from_blueprint(blueprint)
        ...     .with_problem_statement("Fix the bug")
        ...     .add_test_command_scorer("tests", test_command="pytest")
        ... )
        >>> params = builder.build()
        >>> scenario = await runloop.scenario.create(**params)  # equivalent to builder.push()
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize AsyncScenarioOps.

        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        """
        self._client = client

    def builder(self, name: str) -> AsyncScenarioBuilder:
        """Create a new scenario builder.

        :param name: Name for the scenario
        :type name: str
        :return: A new AsyncScenarioBuilder instance
        :rtype: AsyncScenarioBuilder
        """
        return AsyncScenarioBuilder(name, self._client)

    def from_id(self, scenario_id: str) -> AsyncScenario:
        """Get an AsyncScenario instance for an existing scenario ID.

        :param scenario_id: ID of the scenario
        :type scenario_id: str
        :return: AsyncScenario instance for the given ID
        :rtype: AsyncScenario
        """
        return AsyncScenario(self._client, scenario_id)

    async def list(self, **params: Unpack[SDKScenarioListParams]) -> list[AsyncScenario]:
        """List all scenarios, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScenarioListParams` for available parameters
        :return: List of scenarios
        :rtype: list[AsyncScenario]
        """
        page = await self._client.scenarios.list(**params)
        return [AsyncScenario(self._client, item.id) async for item in page]


class AsyncBenchmarkOps:
    """Manage benchmarks (async). Access via ``runloop.benchmark``.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> benchmarks = await runloop.benchmark.list()
        >>> benchmark = runloop.benchmark.from_id("bmd_xxx")
        >>> run = await benchmark.start_run(run_name="evaluation-v1")
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize AsyncBenchmarkOps.

        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(self, **params: Unpack[SDKBenchmarkCreateParams]) -> AsyncBenchmark:
        """Create a new benchmark.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkCreateParams` for available parameters
        :return: The newly created benchmark
        :rtype: AsyncBenchmark
        """
        response = await self._client.benchmarks.create(**params)
        return AsyncBenchmark(self._client, response.id)

    def from_id(self, benchmark_id: str) -> AsyncBenchmark:
        """Get an AsyncBenchmark instance for an existing benchmark ID.

        :param benchmark_id: ID of the benchmark
        :type benchmark_id: str
        :return: AsyncBenchmark instance for the given ID
        :rtype: AsyncBenchmark
        """
        return AsyncBenchmark(self._client, benchmark_id)

    async def list(self, **params: Unpack[SDKBenchmarkListParams]) -> list[AsyncBenchmark]:
        """List all benchmarks, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkListParams` for available parameters
        :return: List of benchmarks
        :rtype: list[AsyncBenchmark]
        """
        page = await self._client.benchmarks.list(**params)
        return [AsyncBenchmark(self._client, item.id) for item in page.benchmarks]


class AsyncNetworkPolicyOps:
    """High-level async manager for creating and managing network policies.

    Accessed via ``runloop.network_policy`` from :class:`AsyncRunloopSDK`, provides
    coroutines to create, retrieve, update, delete, and list network policies.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> policy = await runloop.network_policy.create(
        ...     name="my-policy",
        ...     allowed_hostnames=["github.com", "*.npmjs.org"],
        ... )
        >>> policies = await runloop.network_policy.list()
    """

    def __init__(self, client: AsyncRunloop) -> None:
        """Initialize AsyncNetworkPolicyOps.

        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        """
        self._client = client

    async def create(self, **params: Unpack[SDKNetworkPolicyCreateParams]) -> AsyncNetworkPolicy:
        """Create a new network policy.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKNetworkPolicyCreateParams` for available parameters
        :return: The newly created network policy
        :rtype: AsyncNetworkPolicy
        """
        response = await self._client.network_policies.create(**params)
        return AsyncNetworkPolicy(self._client, response.id)

    def from_id(self, network_policy_id: str) -> AsyncNetworkPolicy:
        """Get an AsyncNetworkPolicy instance for an existing network policy ID.

        :param network_policy_id: ID of the network policy
        :type network_policy_id: str
        :return: AsyncNetworkPolicy instance for the given ID
        :rtype: AsyncNetworkPolicy
        """
        return AsyncNetworkPolicy(self._client, network_policy_id)

    async def list(self, **params: Unpack[SDKNetworkPolicyListParams]) -> list[AsyncNetworkPolicy]:
        """List all network policies, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKNetworkPolicyListParams` for available parameters
        :return: List of network policies
        :rtype: list[AsyncNetworkPolicy]
        """
        page = self._client.network_policies.list(**params)
        return [AsyncNetworkPolicy(self._client, item.id) async for item in page]


class AsyncRunloopSDK:
    """High-level asynchronous entry point for the Runloop SDK.

    Provides a Pythonic, object-oriented interface for managing devboxes,
    blueprints, snapshots, and storage objects. Exposes the generated async REST
    client via the ``api`` attribute for advanced use cases.

    :ivar api: Direct access to the generated async REST API client
    :vartype api: AsyncRunloop
    :ivar agent: High-level async interface for agent management.
    :vartype agent: AsyncAgentOps
    :ivar benchmark: High-level async interface for benchmark management
    :vartype benchmark: AsyncBenchmarkOps
    :ivar devbox: High-level async interface for devbox management
    :vartype devbox: AsyncDevboxOps
    :ivar blueprint: High-level async interface for blueprint management
    :vartype blueprint: AsyncBlueprintOps
    :ivar scenario: High-level async interface for scenario management
    :vartype scenario: AsyncScenarioOps
    :ivar scorer: High-level async interface for scorer management
    :vartype scorer: AsyncScorerOps
    :ivar snapshot: High-level async interface for snapshot management
    :vartype snapshot: AsyncSnapshotOps
    :ivar storage_object: High-level async interface for storage object management
    :vartype storage_object: AsyncStorageObjectOps
    :ivar network_policy: High-level async interface for network policy management
    :vartype network_policy: AsyncNetworkPolicyOps

    Example:
        >>> runloop = AsyncRunloopSDK()  # Uses RUNLOOP_API_KEY env var
        >>> devbox = await runloop.devbox.create(name="my-devbox")
        >>> result = await devbox.cmd.exec("echo 'hello'")
        >>> print(await result.stdout())
        >>> await devbox.shutdown()
    """

    api: AsyncRunloop
    agent: AsyncAgentOps
    benchmark: AsyncBenchmarkOps
    devbox: AsyncDevboxOps
    blueprint: AsyncBlueprintOps
    network_policy: AsyncNetworkPolicyOps
    scenario: AsyncScenarioOps
    scorer: AsyncScorerOps
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

        self.agent = AsyncAgentOps(self.api)
        self.benchmark = AsyncBenchmarkOps(self.api)
        self.devbox = AsyncDevboxOps(self.api)
        self.blueprint = AsyncBlueprintOps(self.api)
        self.network_policy = AsyncNetworkPolicyOps(self.api)
        self.scenario = AsyncScenarioOps(self.api)
        self.scorer = AsyncScorerOps(self.api)
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
