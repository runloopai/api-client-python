# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .shared.agent_source import AgentSource

__all__ = ["AgentView"]


class AgentView(BaseModel):
    """An Agent represents a registered AI agent entity."""

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

    version: Optional[str] = None
    """Optional version identifier for the Agent.

    For npm/pip sources this is typically a semver string (e.g. '2.0.65'). For git
    sources it can be a branch or tag. Omitted for object sources or when not
    provided.
    """
