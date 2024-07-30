# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import TypedDict

from .resource_size import ResourceSize
from .code_mount_parameters_param import CodeMountParametersParam

__all__ = ["BlueprintPreviewParams", "LaunchParameters"]


class BlueprintPreviewParams(TypedDict, total=False):
    code_mounts: Iterable[CodeMountParametersParam]
    """A list of code mounts to be included in the Blueprint."""

    dockerfile: str
    """Dockerfile contents to be used to build the Blueprint."""

    launch_parameters: LaunchParameters
    """Parameters to configure your Devbox at launch time."""

    name: str
    """Name of the Blueprint."""

    system_setup_commands: List[str]
    """A list of commands to run to set up your system."""


class LaunchParameters(TypedDict, total=False):
    launch_commands: List[str]
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: ResourceSize
    """Manual resource configuration for Devbox. If not set, defaults will be used."""
