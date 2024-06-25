# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DevboxView"]


class DevboxView(BaseModel):
    id: Optional[str] = None
    """The id of the Devbox."""

    create_time_ms: Optional[int] = None
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    status: Optional[str] = None
    """
    The current status of the Devbox (provisioning, initializing, running, failure,
    shutdown).
    """
