# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .agent_view import AgentView

__all__ = ["AgentListView"]


class AgentListView(BaseModel):
    agents: List[AgentView]
    """The list of Agents."""

    has_more: bool
    """Whether there are more Agents to fetch."""

    remaining_count: int
    """The count of remaining Agents."""

    total_count: int
    """The total count of Agents."""
