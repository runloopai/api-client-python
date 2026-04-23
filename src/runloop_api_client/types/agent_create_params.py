# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .shared_params.agent_source import AgentSource

__all__ = ["AgentCreateParams"]


class AgentCreateParams(TypedDict, total=False):
    name: Required[str]
    """The name of the Agent."""

    source: Optional[AgentSource]
    """The source configuration for the Agent."""

    version: Optional[str]
    """Optional version identifier for the Agent.

    For npm/pip sources this is typically a semver string (e.g. '2.0.65'). For git
    sources it can be a branch or tag. Semantics are user-defined for object
    sources.
    """
