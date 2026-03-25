# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AxonView"]


class AxonView(BaseModel):
    id: str
    """The axon identifier."""

    created_at_ms: int
    """Creation time in milliseconds since epoch."""

    name: Optional[str] = None
    """The name of the axon."""
