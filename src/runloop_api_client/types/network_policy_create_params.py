# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr
from .allowed_cidr_param import AllowedCidrParam

__all__ = ["NetworkPolicyCreateParams"]


class NetworkPolicyCreateParams(TypedDict, total=False):
    name: Required[str]
    """The human-readable name for the NetworkPolicy.

    Must be unique within the account.
    """

    allow_agent_gateway: Optional[bool]
    """
    (Optional) If true, allows devbox egress to the agent gateway for credential
    proxying. Defaults to false.
    """

    allow_all: Optional[bool]
    """(Optional) If true, all egress traffic is allowed (ALLOW_ALL policy).

    Defaults to false.
    """

    allow_devbox_to_devbox: Optional[bool]
    """
    (Optional) If true, allows traffic between the account's own devboxes via
    tunnels. Defaults to false. If allow_all is true, this is automatically set to
    true.
    """

    allow_mcp_gateway: Optional[bool]
    """(Optional) If true, allows devbox egress to the MCP hub for MCP server access.

    Defaults to false.
    """

    allow_runloop_mirrors: Optional[bool]
    """
    (Optional) If true, allows devbox egress to Runloop's package/image registry
    mirrors. Defaults to false. Implicitly allowed when allow_all is true.
    """

    allowed_cidrs: Optional[Iterable[AllowedCidrParam]]
    """
    (Optional) IPv4 CIDR-based allow list with optional port restrictions, additive
    with allowed_hostnames. Example: [{'cidr': '10.12.0.0/16', 'ports': [{'port':
    443}]}].
    """

    allowed_hostnames: Optional[SequenceNotStr[str]]
    """(Optional) DNS-based allow list with wildcard support.

    Examples: ['github.com', '*.npmjs.org'].
    """

    description: Optional[str]
    """Optional description for the NetworkPolicy."""
