# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .shared.agent_source import AgentSource

__all__ = ["AgentView"]


class AgentView(BaseModel):
    id: str
    """The unique identifier of the Agent."""

    create_time_ms: int
    """The creation time of the Agent (Unix timestamp milliseconds)."""

    is_public: bool
    """Whether the Agent is publicly accessible."""

    name: str
    """The name of the Agent."""

    source: Optional[AgentSource] = None
    """The source configuration for the Agent."""
