# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .agent_view import AgentView

__all__ = ["AgentListView"]


class AgentListView(BaseModel):
    """A paginated list of Agents."""

    agents: List[AgentView]
    """The list of Agents."""

    has_more: bool
    """Whether there are more Agents to fetch."""

    remaining_count: Optional[int] = None
    """The count of remaining Agents.

    Deprecated: will be removed in a future breaking change.
    """

    total_count: Optional[int] = None
    """The total count of Agents.

    Deprecated: will be removed in a future breaking change.
    """
