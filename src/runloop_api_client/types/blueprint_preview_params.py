# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Required, TypedDict

from .code_mount_parameters_param import CodeMountParametersParam
from .shared_params.launch_parameters import LaunchParameters

__all__ = ["BlueprintPreviewParams"]


class BlueprintPreviewParams(TypedDict, total=False):
    name: Required[str]
    """Name of the Blueprint."""

    code_mounts: Iterable[CodeMountParametersParam]
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: str
    """Dockerfile contents to be used to build the Blueprint."""

    file_mounts: Dict[str, str]
    """(Optional) Map of paths and file contents to write before setup.."""

    launch_parameters: LaunchParameters
    """Parameters to configure your Devbox at launch time."""

    system_setup_commands: List[str]
    """A list of commands to run to set up your system."""
