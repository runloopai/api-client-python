# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["NetworkPolicyUpdateParams"]


class NetworkPolicyUpdateParams(TypedDict, total=False):
    allow_all: Optional[bool]
    """If true, all egress traffic is allowed (ALLOW_ALL policy)."""

    allow_devbox_to_devbox: Optional[bool]
    """If true, allows traffic between the account's own devboxes via tunnels."""

    allowed_hostnames: Optional[SequenceNotStr[str]]
    """Updated DNS-based allow list with wildcard support.

    Examples: ['github.com', '*.npmjs.org'].
    """

    description: Optional[str]
    """Updated description for the NetworkPolicy."""

    name: Optional[str]
    """Updated human-readable name for the NetworkPolicy."""
