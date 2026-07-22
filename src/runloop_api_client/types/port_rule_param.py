# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["PortRuleParam"]


class PortRuleParam(TypedDict, total=False):
    """A port or port range allowed for a CIDR egress rule."""

    port: Required[int]
    """The allowed port (1-65535), or the start of a port range."""

    end_port: Optional[int]
    """(Optional) Inclusive end of the port range (port-65535).

    Omit for a single port.
    """

    protocol: Optional[Literal["TCP", "UDP"]]
    """L4 protocol for a port rule."""
