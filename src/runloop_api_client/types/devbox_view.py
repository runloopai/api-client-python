# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .resource_size import ResourceSize

__all__ = ["DevboxView", "LaunchParameters"]


class LaunchParameters(BaseModel):
    keep_alive_time_seconds: Optional[int] = None
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: Optional[List[str]] = None
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: Optional[ResourceSize] = None
    """Manual resource configuration for Devbox. If not set, defaults will be used."""


class DevboxView(BaseModel):
    id: Optional[str] = None
    """The id of the Devbox."""

    blueprint_id: Optional[str] = None
    """The Blueprint ID used in creation of the Devbox, if any."""

    create_time_ms: Optional[int] = None
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    end_time_ms: Optional[int] = None
    """The time the Devbox finished execution (Unix timestamp milliseconds)."""

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "execution_failed"]] = None
    """The failure reason if the Devbox failed, if any."""

    initiator_id: Optional[str] = None
    """The initiator ID of the devbox."""

    initiator_type: Optional[Literal["unknown", "api", "invocation"]] = None
    """The initiator of the devbox."""

    launch_parameters: Optional[LaunchParameters] = None
    """The launch parameters used to create the Devbox."""

    metadata: Optional[Dict[str, str]] = None
    """The user defined Devbox metadata."""

    name: Optional[str] = None
    """The name of the Devbox."""

    shutdown_reason: Optional[Literal["api_shutdown", "keep_alive_timeout", "entrypoint_exit"]] = None
    """The shutdown reason if the Devbox shutdown, if any."""

    status: Optional[Literal["provisioning", "initializing", "running", "failure", "shutdown"]] = None
    """The current status of the Devbox."""
