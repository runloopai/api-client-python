# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .scenario_view import ScenarioView

__all__ = ["ScenarioDefinitionListView"]


class ScenarioDefinitionListView(BaseModel):
    has_more: bool

    remaining_count: int

    scenarios: List[ScenarioView]
    """List of Scenarios matching filter."""

    total_count: int
