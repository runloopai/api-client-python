# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["BrokerMount"]


class BrokerMount(TypedDict, total=False):
    axon_id: Required[str]
    """The ID of the axon event stream to mount onto the Devbox."""

    type: Required[Literal["broker_mount"]]

    agent_binary: Optional[str]
    """Binary to launch the agent (e.g., 'opencode').

    Used by protocols that launch a subprocess (acp, claude_json, codex_app_server).
    """

    launch_args: Optional[SequenceNotStr[str]]
    """Arguments to pass to the agent command (e.g., ['acp']).

    Used by protocols that launch a subprocess (acp, claude_json, codex_app_server).
    """

    protocol: Optional[Literal["acp", "claude_json", "codex_app_server"]]
    """The protocol used by the broker to deliver events to the agent."""
