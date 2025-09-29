# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr
from .shared_params.launch_parameters import LaunchParameters
from .shared_params.code_mount_parameters import CodeMountParameters

__all__ = ["BlueprintCreateParams", "Service", "ServiceCredentials"]


class BlueprintCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the Blueprint."""

    base_blueprint_id: Optional[str]
    """
    (Optional) ID of previously built blueprint to use as a base blueprint for this
    build.
    """

    base_blueprint_name: Optional[str]
    """
    (Optional) Name of previously built blueprint to use as a base blueprint for
    this build. When set, this will load the latest successfully built Blueprint
    with the given name. Only one of (base_blueprint_id, base_blueprint_name) should
    be specified.
    """

    build_args: Optional[Dict[str, str]]
    """(Optional) Arbitrary Docker build args to pass during build."""

    code_mounts: Optional[Iterable[CodeMountParameters]]
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: Optional[str]
    """Dockerfile contents to be used to build the Blueprint."""

    file_mounts: Optional[Dict[str, str]]
    """(Optional) Map of paths and file contents to write before setup."""

    launch_parameters: Optional[LaunchParameters]
    """Parameters to configure your Devbox at launch time."""

    metadata: Optional[Dict[str, str]]
    """(Optional) User defined metadata for the Blueprint."""

    services: Optional[Iterable[Service]]
    """(Optional) List of containerized services to include in the Blueprint.

    These services will be pre-pulled during the build phase for optimized startup
    performance.
    """

    system_setup_commands: Optional[SequenceNotStr[str]]
    """A list of commands to run to set up your system."""


class ServiceCredentials(TypedDict, total=False):
    password: Required[str]
    """The password of the container service."""

    username: Required[str]
    """The username of the container service."""


class Service(TypedDict, total=False):
    image: Required[str]
    """The image of the container service."""

    name: Required[str]
    """The name of the container service."""

    credentials: Optional[ServiceCredentials]
    """The credentials of the container service."""

    env: Optional[Dict[str, str]]
    """The environment variables of the container service."""

    options: Optional[str]
    """Additional Docker container create options."""

    port_mappings: Optional[SequenceNotStr[str]]
    """The port mappings of the container service.

    Port mappings are in the format of <host_port>:<container_port>.
    """
