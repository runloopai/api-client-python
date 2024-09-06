# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .blueprint_build_log import BlueprintBuildLog

__all__ = ["BlueprintBuildLogsListView"]


class BlueprintBuildLogsListView(BaseModel):
    blueprint_id: Optional[str] = None
    """ID of the Blueprint."""

    logs: Optional[List[BlueprintBuildLog]] = None
    """List of logs generated during Blueprint build."""
