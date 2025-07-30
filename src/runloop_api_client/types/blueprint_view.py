# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .blueprint_build_parameters import BlueprintBuildParameters

__all__ = ["BlueprintView", "ContainerizedService", "ContainerizedServiceCredentials"]


class ContainerizedServiceCredentials(BaseModel):
    password: str
    """The password of the container service."""

    username: str
    """The username of the container service."""


class ContainerizedService(BaseModel):
    image: str
    """The image of the container service."""

    name: str
    """The name of the container service."""

    credentials: Optional[ContainerizedServiceCredentials] = None
    """The credentials of the container service."""

    env: Optional[Dict[str, str]] = None
    """The environment variables of the container service."""

    options: Optional[str] = None
    """Additional Docker container create options."""

    port_mappings: Optional[List[str]] = None
    """The port mappings of the container service.

    Port mappings are in the format of <host_port>:<container_port>.
    """


class BlueprintView(BaseModel):
    id: str
    """The id of the Blueprint."""

    create_time_ms: int
    """Creation time of the Blueprint (Unix timestamp milliseconds)."""

    name: str
    """The name of the Blueprint."""

    parameters: BlueprintBuildParameters
    """The parameters used to create Blueprint."""

    state: Literal["created", "deleted"]
    """The state of the Blueprint."""

    status: Literal["provisioning", "building", "failed", "build_complete"]
    """The status of the Blueprint build."""

    base_blueprint_id: Optional[str] = None
    """The ID of the base Blueprint."""

    containerized_services: Optional[List[ContainerizedService]] = FieldInfo(
        alias="containerizedServices", default=None
    )
    """List of ContainerizedServices available in the Blueprint.

    Services can be explicitly started when creating a Devbox.
    """

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "build_failed"]] = None
    """The failure reason if the Blueprint build failed, if any."""
