# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .blueprint_build_parameters import BlueprintBuildParameters

__all__ = ["BlueprintView"]


class BlueprintView(BaseModel):
    id: str
    """The id of the Blueprint."""

    create_time_ms: int
    """Creation time of the Blueprint (Unix timestamp milliseconds)."""

    name: str
    """The name of the Blueprint."""

    parameters: BlueprintBuildParameters
    """The parameters used to create Blueprint."""

    status: Literal["provisioning", "building", "failed", "build_complete"]
    """The status of the Blueprint build."""

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "build_failed"]] = None
    """The failure reason if the Blueprint build failed, if any."""
