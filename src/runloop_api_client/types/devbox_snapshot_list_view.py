# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .devbox_snapshot_view import DevboxSnapshotView

__all__ = ["DevboxSnapshotListView"]


class DevboxSnapshotListView(BaseModel):
    has_more: bool

    remaining_count: int

    snapshots: List[DevboxSnapshotView]
    """List of snapshots matching filter."""

    total_count: int
