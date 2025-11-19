# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.launch_parameters import LaunchParameters
from .shared.code_mount_parameters import CodeMountParameters

__all__ = ["BlueprintBuildParameters", "BuildContext", "NamedBuildContexts", "Service", "ServiceCredentials"]


class BuildContext(BaseModel):
    object_id: str
    """The ID of an object, whose contents are to be used as a build context."""

    type: Literal["object"]


class NamedBuildContexts(BaseModel):
    object_id: str
    """The ID of an object, whose contents are to be used as a build context."""

    type: Literal["object"]


class ServiceCredentials(BaseModel):
    password: str
    """The password of the container service."""

    username: str
    """The username of the container service."""


class Service(BaseModel):
    image: str
    """The image of the container service."""

    name: str
    """The name of the container service."""

    credentials: Optional[ServiceCredentials] = None
    """The credentials of the container service."""

    env: Optional[Dict[str, str]] = None
    """The environment variables of the container service."""

    options: Optional[str] = None
    """Additional Docker container create options."""

    port_mappings: Optional[List[str]] = None
    """The port mappings of the container service.

    Port mappings are in the format of <host_port>:<container_port>.
    """


class BlueprintBuildParameters(BaseModel):
    name: str
    """Name of the Blueprint."""

    base_blueprint_id: Optional[str] = None
    """
    (Optional) ID of previously built blueprint to use as a base blueprint for this
    build.
    """

    base_blueprint_name: Optional[str] = None
    """
    (Optional) Name of previously built blueprint to use as a base blueprint for
    this build. When set, this will load the latest successfully built Blueprint
    with the given name. Only one of (base_blueprint_id, base_blueprint_name) should
    be specified.
    """

    build_args: Optional[Dict[str, str]] = None
    """(Optional) Arbitrary Docker build args to pass during build."""

    build_context: Optional[BuildContext] = None
    """A build context backed by an Object."""

    code_mounts: Optional[List[CodeMountParameters]] = None
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: Optional[str] = None
    """Dockerfile contents to be used to build the Blueprint."""

    file_mounts: Optional[Dict[str, str]] = None
    """(Optional) Map of paths and file contents to write before setup."""

    launch_parameters: Optional[LaunchParameters] = None
    """Parameters to configure your Devbox at launch time."""

    metadata: Optional[Dict[str, str]] = None
    """(Optional) User defined metadata for the Blueprint."""

    named_build_contexts: Optional[Dict[str, NamedBuildContexts]] = None
    """
    (Optional) Map of named build contexts to attach to the Blueprint build, where
    the keys are the name used when referencing the contexts in a Dockerfile. See
    Docker buildx additional contexts for details:
    https://docs.docker.com/reference/cli/docker/buildx/build/#build-context
    """

    secrets: Optional[Dict[str, str]] = None
    """(Optional) Map of mount IDs/environment variable names to secret names.

    Secrets will be available to commands during the build. Secrets are NOT stored
    in the blueprint image. Example: {"DB_PASS": "DATABASE_PASSWORD"} makes the
    secret 'DATABASE_PASSWORD' available as environment variable 'DB_PASS'.
    """

    services: Optional[List[Service]] = None
    """(Optional) List of containerized services to include in the Blueprint.

    These services will be pre-pulled during the build phase for optimized startup
    performance.
    """

    system_setup_commands: Optional[List[str]] = None
    """A list of commands to run to set up your system."""
