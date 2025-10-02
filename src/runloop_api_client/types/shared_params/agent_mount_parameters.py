# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AgentMountParameters"]


class AgentMountParameters(TypedDict, total=False):
    agent_id: Required[str]
    """The ID of the agent to mount."""

    type: Required[Literal["agent_mount"]]

    agent_path: Optional[str]
    """Optional path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """
