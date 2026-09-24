# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .shared_params.launch_parameters import LaunchParameters

__all__ = ["BlueprintRegisterParams"]


class BlueprintRegisterParams(TypedDict, total=False):
    name: Required[str]
    """Name of the Blueprint."""

    launch_parameters: Optional[LaunchParameters]
    """Parameters to configure your Devbox at launch time."""

    metadata: Optional[Dict[str, str]]
    """(Optional) User defined metadata for the Blueprint."""
