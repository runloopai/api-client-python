# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["DevboxEnableTunnelParams"]


class DevboxEnableTunnelParams(TypedDict, total=False):
    auth_mode: Optional[Literal["open", "authenticated"]]
    """Authentication mode for the tunnel. Defaults to 'public' if not specified."""

    http_keep_alive: Optional[bool]
    """
    When true, HTTP traffic through the tunnel counts as activity for idle lifecycle
    policies, resetting the idle timer. Defaults to true if not specified.
    """
