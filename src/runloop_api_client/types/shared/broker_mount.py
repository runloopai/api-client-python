# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BrokerMount"]


class BrokerMount(BaseModel):
    axon_id: str
    """The ID of the axon event stream to mount onto the Devbox."""

    type: Literal["broker_mount"]

    agent_binary: Optional[str] = None
    """Binary to launch the agent (e.g., 'opencode').

    Used by protocols that launch a subprocess (acp, claude_json).
    """

    launch_args: Optional[List[str]] = None
    """Arguments to pass to the agent command (e.g., ['acp']).

    Used by protocols that launch a subprocess (acp, claude_json).
    """

    protocol: Optional[Literal["acp", "claude_json"]] = None
    """The protocol used by the broker to deliver events to the agent."""

    working_directory: Optional[str] = None
    """Working directory in which to launch the agent binary.

    Defaults to the home directory if not specified.
    """
