# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .shared.launch_parameters import LaunchParameters
from .shared.code_mount_parameters import CodeMountParameters

__all__ = ["BlueprintBuildParameters"]


class BlueprintBuildParameters(BaseModel):
    name: str
    """Name of the Blueprint."""

    base_blueprint_id: Optional[str] = None
    """
    (Optional) ID of previously built blueprint to use as a base blueprint for this
    build.
    """

    code_mounts: Optional[List[CodeMountParameters]] = None
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: Optional[str] = None
    """Dockerfile contents to be used to build the Blueprint."""

    file_mounts: Optional[Dict[str, str]] = None
    """(Optional) Map of paths and file contents to write before setup."""

    launch_parameters: Optional[LaunchParameters] = None
    """Parameters to configure your Devbox at launch time."""

    system_setup_commands: Optional[List[str]] = None
    """A list of commands to run to set up your system."""
