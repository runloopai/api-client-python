# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AgentMountParameters"]


class AgentMountParameters(BaseModel):
    agent_id: str
    """The ID of the agent to mount."""

    type: Literal["agent_mount"]

    agent_path: Optional[str] = None
    """Optional path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """
