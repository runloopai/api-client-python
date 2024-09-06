# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .resource_size import ResourceSize
from .code_mount_parameters import CodeMountParameters

__all__ = ["BlueprintBuildParameters", "LaunchParameters"]


class LaunchParameters(BaseModel):
    keep_alive_time_seconds: Optional[int] = None
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: Optional[List[str]] = None
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: Optional[ResourceSize] = None
    """Manual resource configuration for Devbox. If not set, defaults will be used."""


class BlueprintBuildParameters(BaseModel):
    code_mounts: Optional[List[CodeMountParameters]] = None
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: Optional[str] = None
    """Dockerfile contents to be used to build the Blueprint."""

    file_mounts: Optional[Dict[str, str]] = None
    """(Optional) Map of paths and file contents to write before setup.."""

    launch_parameters: Optional[LaunchParameters] = None
    """Parameters to configure your Devbox at launch time."""

    name: Optional[str] = None
    """Name of the Blueprint."""

    system_setup_commands: Optional[List[str]] = None
    """A list of commands to run to set up your system."""
