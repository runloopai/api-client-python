# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .devbox_snapshot_view import DevboxSnapshotView

__all__ = ["DevboxSnapshotListView"]


class DevboxSnapshotListView(BaseModel):
    has_more: bool

    snapshots: List[DevboxSnapshotView]
    """List of snapshots matching filter."""

    remaining_count: Optional[int] = None

    total_count: Optional[int] = None
