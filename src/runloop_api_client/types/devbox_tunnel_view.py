# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DevboxTunnelView"]


class DevboxTunnelView(BaseModel):
    devbox_id: str
    """ID of the Devbox the tunnel routes to."""

    port: int
    """Port of the Devbox the tunnel routes to."""

    url: str
    """Public url used to access Devbox."""
