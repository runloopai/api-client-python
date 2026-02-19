# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .scenario_run_view import ScenarioRunView

__all__ = ["ScenarioRunListView"]


class ScenarioRunListView(BaseModel):
    has_more: bool

    runs: List[ScenarioRunView]
    """List of ScenarioRuns matching filter."""

    remaining_count: Optional[int] = None

    total_count: Optional[int] = None
