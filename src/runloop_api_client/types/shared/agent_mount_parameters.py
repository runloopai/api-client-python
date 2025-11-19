# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AgentMountParameters"]


class AgentMountParameters(BaseModel):
    agent_id: Optional[str] = None
    """The ID of the agent to mount. Either agent_id or name must be set."""

    agent_name: Optional[str] = None
    """The name of the agent to mount.

    Returns the most recent agent with a matching name if no agent id string
    provided. Either agent id or name must be set
    """

    type: Literal["agent_mount"]

    agent_path: Optional[str] = None
    """Path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """

    auth_token: Optional[str] = None
    """Optional auth token for private repositories. Only used for git agents."""
