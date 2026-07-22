# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr
from .allowed_cidr_param import AllowedCidrParam

__all__ = ["NetworkPolicyUpdateParams"]


class NetworkPolicyUpdateParams(TypedDict, total=False):
    allow_agent_gateway: Optional[bool]
    """If true, allows devbox egress to the agent gateway."""

    allow_all: Optional[bool]
    """If true, all egress traffic is allowed (ALLOW_ALL policy)."""

    allow_devbox_to_devbox: Optional[bool]
    """If true, allows traffic between the account's own devboxes via tunnels."""

    allow_mcp_gateway: Optional[bool]
    """If true, allows devbox egress to the MCP hub."""

    allow_runloop_mirrors: Optional[bool]
    """If true, allows devbox egress to Runloop's package/image registry mirrors.

    Implicitly allowed when allow_all is true.
    """

    allowed_cidrs: Optional[Iterable[AllowedCidrParam]]
    """
    Updated IPv4 CIDR-based allow list with optional port restrictions, additive
    with allowed_hostnames.
    """

    allowed_hostnames: Optional[SequenceNotStr[str]]
    """Updated DNS-based allow list with wildcard support.

    Examples: ['github.com', '*.npmjs.org'].
    """

    description: Optional[str]
    """Updated description for the NetworkPolicy."""

    name: Optional[str]
    """Updated human-readable name for the NetworkPolicy."""
