"""Synchronous SDK entry points and management interfaces."""

from __future__ import annotations

from typing import Dict, Mapping, Optional
from pathlib import Path
from datetime import timedelta
from typing_extensions import Unpack

import httpx

from .agent import Agent
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
from .devbox import Devbox
from .scorer import Scorer
from .._types import Timeout, NotGiven, not_given
from .._client import DEFAULT_MAX_RETRIES, Runloop
from ._helpers import detect_content_type
from .scenario import Scenario
from .snapshot import Snapshot
from .benchmark import Benchmark
from .blueprint import Blueprint
from .network_policy import NetworkPolicy
from .storage_object import StorageObject
from .scenario_builder import ScenarioBuilder
from ..lib.context_loader import TarFilter, build_directory_tar
from ..types.object_create_params import ContentType
from ..types.shared_params.agent_source import Git, Npm, Pip, Object


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

        :param client: Generated Runloop client to wrap
        :type client: Runloop
        """
        self._client = client

    def create(
        self,
        **params: Unpack[SDKDevboxCreateParams],
    ) -> Devbox:
        """Provision a new devbox and wait until it reaches ``running`` state.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: Devbox
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_id(
        self,
        blueprint_id: str,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> Devbox:
        """Create a devbox from an existing blueprint by identifier.

        :param blueprint_id: Blueprint ID to create from
        :type blueprint_id: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: Devbox
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_id=blueprint_id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_name(
        self,
        blueprint_name: str,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> Devbox:
        """Create a devbox from the latest blueprint with the given name.

        :param blueprint_name: Blueprint name to create from
        :type blueprint_name: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: Devbox
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_name=blueprint_name,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_snapshot(
        self,
        snapshot_id: str,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> Devbox:
        """Create a devbox initialized from a snapshot.

        :param snapshot_id: Snapshot ID to create from
        :type snapshot_id: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the newly created devbox
        :rtype: Devbox
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            snapshot_id=snapshot_id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def from_id(self, devbox_id: str) -> Devbox:
        """Attach to an existing devbox by ID.

        Blocks until the devbox reaches ``running`` state so callers can begin
        issuing commands immediately.

        :param devbox_id: Existing devbox ID
        :type devbox_id: str
        :return: Wrapper bound to the requested devbox
        :rtype: Devbox
        """
        self._client.devboxes.await_running(devbox_id)
        return Devbox(self._client, devbox_id)

    def list(
        self,
        **params: Unpack[SDKDevboxListParams],
    ) -> list[Devbox]:
        """List devboxes accessible to the caller.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxListParams` for available parameters
        :return: Collection of devbox wrappers
        :rtype: list[Devbox]
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
        """Initialize the manager with the generated Runloop client.

        :param client: Generated Runloop client
        :type client: Runloop
        """
        self._client = client

    def list(
        self,
        **params: Unpack[SDKDiskSnapshotListParams],
    ) -> list[Snapshot]:
        """List snapshots created from devboxes.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDiskSnapshotListParams` for available parameters
        :return: Snapshot wrappers for each record
        :rtype: list[Snapshot]
        """
        page = self._client.devboxes.disk_snapshots.list(
            **params,
        )
        return [Snapshot(self._client, item.id) for item in page.snapshots]

    def from_id(self, snapshot_id: str) -> Snapshot:
        """Return a snapshot wrapper for the given ID.

        :param snapshot_id: Snapshot ID to wrap
        :type snapshot_id: str
        :return: Wrapper for the snapshot resource
        :rtype: Snapshot
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

    To use a local directory as a build context, use an object.

    Example:
        >>> from datetime import timedelta
        >>> from runloop_api_client.types.blueprint_build_parameters import BuildContext
        >>> runloop = RunloopSDK()
        >>> obj = runloop.object_storage.upload_from_dir(
        ...     "./",
        ...     ttl=timedelta(hours=1),
        ... )
        >>> blueprint = runloop.blueprint.create(
        ...     name="my-blueprint",
        ...     dockerfile="FROM ubuntu:22.04\\nCOPY . .\\n",
        ...     build_context=BuildContext(type="object", object_id=obj.id),
        ... )
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize the manager.

        :param client: Generated Runloop client to wrap
        :type client: Runloop
        """
        self._client = client

    def create(
        self,
        **params: Unpack[SDKBlueprintCreateParams],
    ) -> Blueprint:
        """Create a blueprint and wait for the build to finish.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBlueprintCreateParams` for available parameters
        :return: Wrapper bound to the finished blueprint
        :rtype: Blueprint
        """
        blueprint = self._client.blueprints.create_and_await_build_complete(
            **params,
        )
        return Blueprint(self._client, blueprint.id)

    def from_id(self, blueprint_id: str) -> Blueprint:
        """Return a blueprint wrapper for the given ID.

        :param blueprint_id: Blueprint ID to wrap
        :type blueprint_id: str
        :return: Wrapper for the blueprint resource
        :rtype: Blueprint
        """
        return Blueprint(self._client, blueprint_id)

    def list(
        self,
        **params: Unpack[SDKBlueprintListParams],
    ) -> list[Blueprint]:
        """List available blueprints.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBlueprintListParams` for available parameters
        :return: Blueprint wrappers for each record
        :rtype: list[Blueprint]
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
        """Initialize the manager with the generated Runloop client.

        :param client: Generated Runloop client
        :type client: Runloop
        """
        self._client = client

    def create(
        self,
        **params: Unpack[SDKObjectCreateParams],
    ) -> StorageObject:
        """Create a storage object and obtain an upload URL.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectCreateParams` for available parameters
        :return: Wrapper with upload URL set for immediate uploads
        :rtype: StorageObject
        """
        obj = self._client.objects.create(**params)
        return StorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> StorageObject:
        """Return a storage object wrapper by identifier.

        :param object_id: Storage object identifier to wrap
        :type object_id: str
        :return: Wrapper for the storage object resource
        :rtype: StorageObject
        """
        return StorageObject(self._client, object_id, upload_url=None)

    def list(
        self,
        **params: Unpack[SDKObjectListParams],
    ) -> list[StorageObject]:
        """List storage objects owned by the caller.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectListParams` for available parameters
        :return: Storage object wrappers for each record
        :rtype: list[StorageObject]
        """
        page = self._client.objects.list(
            **params,
        )
        return [StorageObject(self._client, item.id, upload_url=item.upload_url) for item in page.objects]

    def upload_from_file(
        self,
        file_path: str | Path,
        *,
        name: Optional[str] = None,
        content_type: Optional[ContentType] = None,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
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
        :rtype: StorageObject
        :raises OSError: If the local file cannot be read
        """
        path = Path(file_path)

        try:
            content = path.read_bytes()
        except OSError as error:
            raise OSError(f"Failed to read file {path}: {error}") from error

        name = name or path.name
        content_type = content_type or detect_content_type(str(file_path))
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None
        obj = self.create(name=name, content_type=content_type, metadata=metadata, ttl_ms=ttl_ms, **options)
        obj.upload_content(content)
        obj.complete()
        return obj

    def upload_from_dir(
        self,
        dir_path: str | Path,
        *,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        ignore: TarFilter | None = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
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
        :rtype: StorageObject
        :raises OSError: If the local file cannot be read
        :raises ValueError: If ``dir_path`` does not point to a directory
        """
        path = Path(dir_path)
        if not path.is_dir():
            raise ValueError(f"dir_path must be a directory, got: {path}")

        name = name or f"{path.name}.tar.gz"
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None

        tar_bytes = build_directory_tar(path, tar_filter=ignore)

        obj = self.create(name=name, content_type="tgz", metadata=metadata, ttl_ms=ttl_ms, **options)
        obj.upload_content(tar_bytes)
        obj.complete()
        return obj

    def upload_from_text(
        self,
        text: str,
        *,
        name: str,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
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
        :rtype: StorageObject
        """
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None
        obj = self.create(name=name, content_type="text", metadata=metadata, ttl_ms=ttl_ms, **options)
        obj.upload_content(text)
        obj.complete()
        return obj

    def upload_from_bytes(
        self,
        data: bytes,
        *,
        name: str,
        content_type: ContentType,
        metadata: Optional[Dict[str, str]] = None,
        ttl: Optional[timedelta] = None,
        **options: Unpack[LongRequestOptions],
    ) -> StorageObject:
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
        :rtype: StorageObject
        """
        ttl_ms = int(ttl.total_seconds()) * 1000 if ttl else None
        obj = self.create(name=name, content_type=content_type, metadata=metadata, ttl_ms=ttl_ms, **options)
        obj.upload_content(data)
        obj.complete()
        return obj


class ScorerOps:
    """Create and manage custom scorers. Access via ``runloop.scorer``.

    Example:
        >>> runloop = RunloopSDK()
        >>> scorer = runloop.scorer.create(type="my_scorer", bash_script="echo 'score=1.0'")
        >>> all_scorers = runloop.scorer.list()
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize ScorerOps.

        :param client: Runloop client instance
        :type client: Runloop
        """
        self._client = client

    def create(self, **params: Unpack[SDKScorerCreateParams]) -> Scorer:
        """Create a new scorer with the given type and bash script.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerCreateParams` for available parameters
        :return: The newly created scorer
        :rtype: Scorer
        """
        response = self._client.scenarios.scorers.create(**params)
        return Scorer(self._client, response.id)

    def from_id(self, scorer_id: str) -> Scorer:
        """Get a Scorer instance for an existing scorer ID.

        :param scorer_id: ID of the scorer
        :type scorer_id: str
        :return: Scorer instance for the given ID
        :rtype: Scorer
        """
        return Scorer(self._client, scorer_id)

    def list(self, **params: Unpack[SDKScorerListParams]) -> list[Scorer]:
        """List all scorers, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerListParams` for available parameters
        :return: List of scorers
        :rtype: list[Scorer]
        """
        page = self._client.scenarios.scorers.list(**params)
        return [Scorer(self._client, item.id) for item in page]


class AgentOps:
    """High-level manager for creating and managing agents.

    Accessed via ``runloop.agent`` from :class:`RunloopSDK`, provides methods to
    create, retrieve, and list agents from various sources (npm, pip, git, object storage).

    Example:
        >>> runloop = RunloopSDK()
        >>> # Create agent from NPM package
        >>> agent = runloop.agent.create_from_npm(name="my-agent", package_name="@runloop/example-agent")
        >>> # Create agent from Git repository
        >>> agent = runloop.agent.create_from_git(
        ...     name="git-agent", repository="https://github.com/user/agent-repo", ref="main"
        ... )
        >>> # List all agents
        >>> agents = runloop.agent.list(limit=10)
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize the manager.

        :param client: Generated Runloop client to wrap
        :type client: Runloop
        """
        self._client = client

    def create(
        self,
        **params: Unpack[SDKAgentCreateParams],
    ) -> Agent:
        """Create a new agent.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for available parameters
        :return: Wrapper bound to the newly created agent
        :rtype: Agent
        """
        agent_view = self._client.agents.create(
            **params,
        )
        return Agent(self._client, agent_view.id, agent_view)

    def create_from_npm(
        self,
        *,
        package_name: str,
        registry_url: Optional[str] = None,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> Agent:
        """Create an agent from an NPM package.

        Example:
            >>> agent = runloop.agent.create_from_npm(
            ...     name="my-npm-agent", package_name="@runloop/example-agent", version="1.0.0"
            ... )

        :param package_name: NPM package name
        :type package_name: str
        :param registry_url: NPM registry URL, defaults to None
        :type registry_url: Optional[str], optional
        :param agent_setup: Setup commands to run after installation, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: Agent
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
        return self.create(**params)

    def create_from_pip(
        self,
        *,
        package_name: str,
        registry_url: Optional[str] = None,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> Agent:
        """Create an agent from a Pip package.

        Example:
            >>> agent = runloop.agent.create_from_pip(
            ...     name="my-pip-agent", package_name="runloop-example-agent", version="1.0.0"
            ... )

        :param package_name: Pip package name
        :type package_name: str
        :param registry_url: Pip registry URL, defaults to None
        :type registry_url: Optional[str], optional
        :param agent_setup: Setup commands to run after installation, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: Agent
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
        return self.create(**params)

    def create_from_git(
        self,
        *,
        repository: str,
        ref: Optional[str] = None,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> Agent:
        """Create an agent from a Git repository.

        Example:
            >>> agent = runloop.agent.create_from_git(
            ...     name="my-git-agent",
            ...     repository="https://github.com/user/agent-repo",
            ...     ref="main",
            ...     agent_setup=["npm install", "npm run build"],
            ...     version="1.0.0",
            ... )

        :param repository: Git repository URL
        :type repository: str
        :param ref: Optional Git ref (branch/tag/commit), defaults to main/HEAD
        :type ref: Optional[str], optional
        :param agent_setup: Setup commands to run after cloning, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: Agent
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
        return self.create(**params)

    def create_from_object(
        self,
        *,
        object_id: str,
        agent_setup: Optional[list[str]] = None,
        **params: Unpack[SDKAgentCreateParams],
    ) -> Agent:
        """Create an agent from a storage object.

        Example:
            >>> # First upload agent code as an object
            >>> obj = runloop.storage_object.upload_from_dir("./my-agent")
            >>> # Then create agent from the object
            >>> agent = runloop.agent.create_from_object(
            ...     name="my-object-agent",
            ...     object_id=obj.id,
            ...     agent_setup=["chmod +x setup.sh", "./setup.sh"],
            ...     version="1.0.0",
            ... )

        :param object_id: Storage object ID
        :type object_id: str
        :param agent_setup: Setup commands to run after unpacking, defaults to None
        :type agent_setup: Optional[list[str]], optional
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentCreateParams` for additional parameters (excluding 'source')
        :return: Wrapper bound to the newly created agent
        :rtype: Agent
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
        return self.create(**params)

    def from_id(self, agent_id: str) -> Agent:
        """Attach to an existing agent by ID.

        :param agent_id: Existing agent ID
        :type agent_id: str
        :return: Wrapper bound to the requested agent
        :rtype: Agent
        """
        return Agent(self._client, agent_id)

    def list(
        self,
        **params: Unpack[SDKAgentListParams],
    ) -> list[Agent]:
        """List agents accessible to the caller.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKAgentListParams` for available parameters
        :return: Collection of agent wrappers
        :rtype: list[Agent]
        """
        page = self._client.agents.list(
            **params,
        )
        return [Agent(self._client, item.id, item) for item in page.agents]


class ScenarioOps:
    """Manage scenarios. Access via ``runloop.scenario``.

    Example:
        >>> runloop = RunloopSDK()
        >>> scenario = runloop.scenario.from_id("scn-xxx")
        >>> run = scenario.run()
        >>> scenarios = runloop.scenario.list()

    Example using builder:
        >>> builder = (
        ...     runloop.scenario.builder("my-scenario")
        ...     .from_blueprint(blueprint)
        ...     .with_problem_statement("Fix the bug")
        ...     .add_test_command_scorer("tests", test_command="pytest")
        ... )
        >>> params = builder.build()
        >>> scenario = runloop.scenario.create(**params)  # equivalent to builder.push()
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize ScenarioOps.

        :param client: Runloop client instance
        :type client: Runloop
        """
        self._client = client

    def builder(self, name: str) -> ScenarioBuilder:
        """Create a new scenario builder.

        :param name: Name for the scenario
        :type name: str
        :return: A new ScenarioBuilder instance
        :rtype: ScenarioBuilder
        """
        return ScenarioBuilder(name, self._client)

    def from_id(self, scenario_id: str) -> Scenario:
        """Get a Scenario instance for an existing scenario ID.

        :param scenario_id: ID of the scenario
        :type scenario_id: str
        :return: Scenario instance for the given ID
        :rtype: Scenario
        """
        return Scenario(self._client, scenario_id)

    def list(self, **params: Unpack[SDKScenarioListParams]) -> list[Scenario]:
        """List all scenarios, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScenarioListParams` for available parameters
        :return: List of scenarios
        :rtype: list[Scenario]
        """
        page = self._client.scenarios.list(**params)
        return [Scenario(self._client, item.id) for item in page]


class BenchmarkOps:
    """Manage benchmarks. Access via ``runloop.benchmark``.

    Example:
        >>> runloop = RunloopSDK()
        >>> benchmarks = runloop.benchmark.list()
        >>> benchmark = runloop.benchmark.from_id("bmd_xxx")
        >>> run = benchmark.start_run(run_name="evaluation-v1")
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize BenchmarkOps.

        :param client: Runloop client instance
        :type client: Runloop
        """
        self._client = client

    def create(self, **params: Unpack[SDKBenchmarkCreateParams]) -> Benchmark:
        """Create a new benchmark.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkCreateParams` for available parameters
        :return: The newly created benchmark
        :rtype: Benchmark
        """
        response = self._client.benchmarks.create(**params)
        return Benchmark(self._client, response.id)

    def from_id(self, benchmark_id: str) -> Benchmark:
        """Get a Benchmark instance for an existing benchmark ID.

        :param benchmark_id: ID of the benchmark
        :type benchmark_id: str
        :return: Benchmark instance for the given ID
        :rtype: Benchmark
        """
        return Benchmark(self._client, benchmark_id)

    def list(self, **params: Unpack[SDKBenchmarkListParams]) -> list[Benchmark]:
        """List all benchmarks, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkListParams` for available parameters
        :return: List of benchmarks
        :rtype: list[Benchmark]
        """
        page = self._client.benchmarks.list(**params)
        return [Benchmark(self._client, item.id) for item in page.benchmarks]


class NetworkPolicyOps:
    """High-level manager for creating and managing network policies.

    Accessed via ``runloop.network_policy`` from :class:`RunloopSDK`, provides methods
    to create, retrieve, update, delete, and list network policies.

    Example:
        >>> runloop = RunloopSDK()
        >>> policy = runloop.network_policy.create(
        ...     name="my-policy",
        ...     allowed_hostnames=["github.com", "*.npmjs.org"],
        ... )
        >>> policies = runloop.network_policy.list()
    """

    def __init__(self, client: Runloop) -> None:
        """Initialize NetworkPolicyOps.

        :param client: Runloop client instance
        :type client: Runloop
        """
        self._client = client

    def create(self, **params: Unpack[SDKNetworkPolicyCreateParams]) -> NetworkPolicy:
        """Create a new network policy.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKNetworkPolicyCreateParams` for available parameters
        :return: The newly created network policy
        :rtype: NetworkPolicy
        """
        response = self._client.network_policies.create(**params)
        return NetworkPolicy(self._client, response.id)

    def from_id(self, network_policy_id: str) -> NetworkPolicy:
        """Get a NetworkPolicy instance for an existing network policy ID.

        :param network_policy_id: ID of the network policy
        :type network_policy_id: str
        :return: NetworkPolicy instance for the given ID
        :rtype: NetworkPolicy
        """
        return NetworkPolicy(self._client, network_policy_id)

    def list(self, **params: Unpack[SDKNetworkPolicyListParams]) -> list[NetworkPolicy]:
        """List all network policies, optionally filtered by parameters.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKNetworkPolicyListParams` for available parameters
        :return: List of network policies
        :rtype: list[NetworkPolicy]
        """
        page = self._client.network_policies.list(**params)
        return [NetworkPolicy(self._client, item.id) for item in page]


class RunloopSDK:
    """High-level synchronous entry point for the Runloop SDK.

    Provides a Pythonic, object-oriented interface for managing devboxes, blueprints,
    snapshots, and storage objects. Exposes the generated REST client via the ``api``
    attribute for advanced use cases.

    :ivar api: Direct access to the generated REST API client
    :vartype api: Runloop
    :ivar agent: High-level interface for agent management.
    :vartype agent: AgentOps
    :ivar benchmark: High-level interface for benchmark management
    :vartype benchmark: BenchmarkOps
    :ivar devbox: High-level interface for devbox management
    :vartype devbox: DevboxOps
    :ivar blueprint: High-level interface for blueprint management
    :vartype blueprint: BlueprintOps
    :ivar scenario: High-level interface for scenario management
    :vartype scenario: ScenarioOps
    :ivar scorer: High-level interface for scorer management
    :vartype scorer: ScorerOps
    :ivar snapshot: High-level interface for snapshot management
    :vartype snapshot: SnapshotOps
    :ivar storage_object: High-level interface for storage object management
    :vartype storage_object: StorageObjectOps
    :ivar network_policy: High-level interface for network policy management
    :vartype network_policy: NetworkPolicyOps

    Example:
        >>> runloop = RunloopSDK()  # Uses RUNLOOP_API_KEY env var
        >>> devbox = runloop.devbox.create(name="my-devbox")
        >>> result = devbox.cmd.exec("echo 'hello'")
        >>> print(result.stdout())
        >>> devbox.shutdown()
    """

    api: Runloop
    agent: AgentOps
    benchmark: BenchmarkOps
    devbox: DevboxOps
    blueprint: BlueprintOps
    network_policy: NetworkPolicyOps
    scenario: ScenarioOps
    scorer: ScorerOps
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
        :param http_client: Custom ``httpx.Client`` instance to reuse, defaults to None
        :type http_client: httpx.Client | None, optional
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

        self.agent = AgentOps(self.api)
        self.benchmark = BenchmarkOps(self.api)
        self.devbox = DevboxOps(self.api)
        self.blueprint = BlueprintOps(self.api)
        self.network_policy = NetworkPolicyOps(self.api)
        self.scenario = ScenarioOps(self.api)
        self.scorer = ScorerOps(self.api)
        self.snapshot = SnapshotOps(self.api)
        self.storage_object = StorageObjectOps(self.api)

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self.api.close()

    def __enter__(self) -> "RunloopSDK":
        """Allow ``with RunloopSDK() as runloop`` usage.

        :return: The active SDK instance
        :rtype: RunloopSDK
        """
        return self

    def __exit__(self, *_exc_info: object) -> None:
        """Ensure the API client closes when leaving the context manager."""
        self.close()
