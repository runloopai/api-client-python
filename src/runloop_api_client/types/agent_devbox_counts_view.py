# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict

from .._models import BaseModel

__all__ = ["AgentDevboxCountsView"]


class AgentDevboxCountsView(BaseModel):
    """Devbox counts grouped by agent name.

    Used to efficiently fetch devbox counts for multiple agents in a single request.
    """

    counts: Dict[str, int]
    """Map of agent name to devbox count.

    Each key is an agent name, and the value is the count of devboxes associated
    with that agent.
    """

    total_count: int
    """Total count of devboxes across all agents in the result."""
