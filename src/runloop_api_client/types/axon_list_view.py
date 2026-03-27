# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .axon_view import AxonView

__all__ = ["AxonListView"]


class AxonListView(BaseModel):
    axons: List[AxonView]
    """List of active axons."""

    has_more: bool

    total_count: Optional[int] = None
