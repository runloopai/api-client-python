# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.launch_parameters import LaunchParameters
from .shared_params.code_mount_parameters import CodeMountParameters

__all__ = ["DevboxCreateParams", "Mount", "MountObjectMountParameters", "MountAgentMountParameters"]


class DevboxCreateParams(TypedDict, total=False):
    blueprint_id: Optional[str]
    """Blueprint ID to use for the Devbox.

    If none set, the Devbox will be created with the default Runloop Devbox image.
    Only one of (Snapshot ID, Blueprint ID, Blueprint name) should be specified.
    """

    blueprint_name: Optional[str]
    """Name of Blueprint to use for the Devbox.

    When set, this will load the latest successfully built Blueprint with the given
    name. Only one of (Snapshot ID, Blueprint ID, Blueprint name) should be
    specified.
    """

    code_mounts: Optional[Iterable[CodeMountParameters]]
    """A list of code mounts to be included in the Devbox."""

    entrypoint: Optional[str]
    """
    (Optional) When specified, the Devbox will run this script as its main
    executable. The devbox lifecycle will be bound to entrypoint, shutting down when
    the process is complete.
    """

    environment_variables: Optional[Dict[str, str]]
    """(Optional) Environment variables used to configure your Devbox."""

    file_mounts: Optional[Dict[str, str]]
    """(Optional) Map of paths and file contents to write before setup.."""

    launch_parameters: Optional[LaunchParameters]
    """Parameters to configure the resources and launch time behavior of the Devbox."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the devbox for organization."""

    mounts: Optional[Iterable[Mount]]
    """A list of file system mounts to be included in the Devbox."""

    name: Optional[str]
    """(Optional) A user specified name to give the Devbox."""

    repo_connection_id: Optional[str]
    """Repository connection id the devbox should source its base image from."""

    secrets: Optional[Dict[str, str]]
    """(Optional) Map of environment variable names to secret names.

    The secret values will be securely injected as environment variables in the
    Devbox. Example: {"DB_PASS": "DATABASE_PASSWORD"} sets environment variable
    'DB_PASS' to the value of secret 'DATABASE_PASSWORD'.
    """

    snapshot_id: Optional[str]
    """Snapshot ID to use for the Devbox.

    Only one of (Snapshot ID, Blueprint ID, Blueprint name) should be specified.
    """


class MountObjectMountParameters(TypedDict, total=False):
    object_id: Required[str]
    """The ID of the object to write."""

    object_path: Required[str]
    """The path to write the object on the Devbox.

    Use absolute path of object (ie /home/user/object.txt, or directory if archive
    /home/user/archive_dir)
    """

    type: Required[Literal["object_mount"]]


class MountAgentMountParameters(TypedDict, total=False):
    agent_id: Required[str]
    """The ID of the agent to mount."""

    type: Required[Literal["agent_mount"]]

    agent_path: Optional[str]
    """Optional path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """


Mount: TypeAlias = Union[MountObjectMountParameters, MountAgentMountParameters]
