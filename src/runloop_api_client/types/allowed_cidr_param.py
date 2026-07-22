# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .port_rule_param import PortRuleParam

__all__ = ["AllowedCidrParam"]


class AllowedCidrParam(TypedDict, total=False):
    """A CIDR-based egress allow rule with optional port restrictions."""

    cidr: Required[str]
    """IPv4 CIDR block in canonical form (host bits zero), e.g. '10.12.0.0/16'."""

    ports: Optional[Iterable[PortRuleParam]]
    """(Optional) Ports allowed for this CIDR.

    Empty or omitted means all ports and protocols.
    """
