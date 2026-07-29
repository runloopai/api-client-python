# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DevboxEvictionEventView"]


class DevboxEvictionEventView(BaseModel):
    devbox_id: str
    """The ID of the Devbox with a pending eviction."""

    eviction_deadline_ms: int
    """Unix timestamp (milliseconds) after which the Devbox will be suspended.

    Advisory and best-effort.
    """
