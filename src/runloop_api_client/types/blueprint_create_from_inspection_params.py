# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr
from .inspection_source_param import InspectionSourceParam
from .shared_params.launch_parameters import LaunchParameters

__all__ = ["BlueprintCreateFromInspectionParams"]


class BlueprintCreateFromInspectionParams(TypedDict, total=False):
    inspection_source: Required[InspectionSourceParam]
    """(Optional) Use a RepositoryInspection a source of a Blueprint build.

    The Dockerfile will be automatically created based on the RepositoryInspection
    contents.
    """

    name: Required[str]
    """Name of the Blueprint."""

    file_mounts: Optional[Dict[str, str]]
    """(Optional) Map of paths and file contents to write before setup."""

    launch_parameters: Optional[LaunchParameters]
    """Parameters to configure your Devbox at launch time."""

    metadata: Optional[Dict[str, str]]
    """(Optional) User defined metadata for the Blueprint."""

    system_setup_commands: Optional[SequenceNotStr[str]]
    """A list of commands to run to set up your system."""
