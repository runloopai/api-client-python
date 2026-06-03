# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["PtyTunnelView"]


class PtyTunnelView(BaseModel):
    """An ephemeral PTY tunnel providing authenticated terminal access to a Devbox.

    These tunnels are not stored on the Devbox and are generated fresh on each request. Usage: https://{port}-{tunnel_key}.tunnel.runloop.ai with X-Runloop-Tunnel-Authorization: Bearer {auth_token}.
    """

    auth_token: str
    """Bearer token for tunnel authentication.

    Always required for PTY tunnels. Pass as X-Runloop-Tunnel-Authorization: Bearer
    {auth_token}.
    """

    tunnel_key: str
    """The encrypted tunnel key used to construct the tunnel URL.

    URL format: https://{port}-{tunnel_key}.tunnel.runloop.{domain}
    """
