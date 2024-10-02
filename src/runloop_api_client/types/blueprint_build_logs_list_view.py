# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .blueprint_build_log import BlueprintBuildLog

__all__ = ["BlueprintBuildLogsListView"]


class BlueprintBuildLogsListView(BaseModel):
    blueprint_id: str
    """ID of the Blueprint."""

    logs: List[BlueprintBuildLog]
    """List of logs generated during Blueprint build."""
