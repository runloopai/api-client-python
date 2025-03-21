# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .scenario_run_view import ScenarioRunView

__all__ = ["ScenarioRunListView"]


class ScenarioRunListView(BaseModel):
    has_more: bool

    remaining_count: int

    runs: List[ScenarioRunView]
    """List of ScenarioRuns matching filter."""

    total_count: int
