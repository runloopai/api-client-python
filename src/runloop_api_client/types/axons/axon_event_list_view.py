# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from ..axon_event_view import AxonEventView

__all__ = ["AxonEventListView"]


class AxonEventListView(BaseModel):
    events: List[AxonEventView]
    """List of axon events."""

    has_more: bool

    total_count: Optional[int] = None
