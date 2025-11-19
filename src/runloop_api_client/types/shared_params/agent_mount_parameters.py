# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AgentMountParameters"]


class AgentMountParameters(TypedDict, total=False):
    agent_id: Required[Optional[str]]
    """The ID of the agent to mount. Either agent_id or name must be set."""

    agent_name: Required[Optional[str]]
    """The name of the agent to mount.

    Returns the most recent agent with a matching name if no agent id string
    provided. Either agent id or name must be set
    """

    type: Required[Literal["agent_mount"]]

    agent_path: Optional[str]
    """Path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """

    auth_token: Optional[str]
    """Optional auth token for private repositories. Only used for git agents."""
