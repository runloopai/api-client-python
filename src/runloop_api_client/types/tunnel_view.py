# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TunnelView"]


class TunnelView(BaseModel):
    """A V2 tunnel provides secure HTTP access to services running on a Devbox.

    Tunnels allow external clients to reach web servers, APIs, or other HTTP services running inside a Devbox without requiring direct network access. Each tunnel is uniquely identified by an encrypted tunnel_key and can be configured for either open (public) or authenticated access.
    Usage: https://{port}-{tunnel_key}.tunnel.runloop.ai
    """

    auth_mode: Literal["open", "authenticated"]
    """The authentication mode for the tunnel."""

    create_time_ms: int
    """Creation time of the tunnel (Unix timestamp milliseconds)."""

    tunnel_key: str
    """The encrypted tunnel key used to construct the tunnel URL.

    URL format: https://{port}-{tunnel_key}.tunnel.runloop.{domain}
    """

    auth_token: Optional[str] = None
    """Bearer token for tunnel authentication.

    Only present when auth_mode is 'authenticated'.
    """
