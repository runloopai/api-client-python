# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .scenario_view import ScenarioView

__all__ = ["ScenarioDefinitionListView"]


class ScenarioDefinitionListView(BaseModel):
    has_more: bool

    scenarios: List[ScenarioView]
    """List of Scenarios matching filter."""

    remaining_count: Optional[int] = None

    total_count: Optional[int] = None
