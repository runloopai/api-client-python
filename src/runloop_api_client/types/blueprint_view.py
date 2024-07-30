# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .blueprint_build_parameters import BlueprintBuildParameters

__all__ = ["BlueprintView"]


class BlueprintView(BaseModel):
    id: Optional[str] = None
    """The id of the Blueprint."""

    create_time_ms: Optional[int] = None
    """Creation time of the Blueprint (Unix timestamp milliseconds)."""

    name: Optional[str] = None
    """The name of the Blueprint."""

    parameters: Optional[BlueprintBuildParameters] = None
    """The parameters used to create Blueprint."""

    status: Optional[Literal["provisioning", "building", "failed", "build_complete"]] = None
    """The status of the Blueprint build."""
