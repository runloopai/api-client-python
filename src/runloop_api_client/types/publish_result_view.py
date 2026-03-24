# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["PublishResultView"]


class PublishResultView(BaseModel):
    sequence: int
    """Assigned sequence number."""

    timestamp_ms: int
    """Timestamp in milliseconds since epoch."""
