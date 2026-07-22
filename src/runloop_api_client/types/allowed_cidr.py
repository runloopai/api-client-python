# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .port_rule import PortRule

__all__ = ["AllowedCidr"]


class AllowedCidr(BaseModel):
    """A CIDR-based egress allow rule with optional port restrictions."""

    cidr: str
    """IPv4 CIDR block in canonical form (host bits zero), e.g. '10.12.0.0/16'."""

    ports: Optional[List[PortRule]] = None
    """(Optional) Ports allowed for this CIDR.

    Empty or omitted means all ports and protocols.
    """
