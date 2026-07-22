# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["PortRule"]


class PortRule(BaseModel):
    """A port or port range allowed for a CIDR egress rule."""

    port: int
    """The allowed port (1-65535), or the start of a port range."""

    end_port: Optional[int] = None
    """(Optional) Inclusive end of the port range (port-65535).

    Omit for a single port.
    """

    protocol: Optional[Literal["TCP", "UDP"]] = None
    """L4 protocol for a port rule."""
