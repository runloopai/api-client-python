# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable, Optional
from typing_extensions import Required, TypedDict

from .shared_params.launch_parameters import LaunchParameters
from .shared_params.code_mount_parameters import CodeMountParameters

__all__ = ["BlueprintCreateParams"]


class BlueprintCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the Blueprint."""

    code_mounts: Optional[Iterable[CodeMountParameters]]
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: Optional[str]
    """Dockerfile contents to be used to build the Blueprint."""

    file_mounts: Optional[Dict[str, str]]
    """(Optional) Map of paths and file contents to write before setup.."""

    launch_parameters: Optional[LaunchParameters]
    """Parameters to configure your Devbox at launch time."""

    system_setup_commands: Optional[List[str]]
    """A list of commands to run to set up your system."""
