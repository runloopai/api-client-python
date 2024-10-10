# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DevboxDiskSnapshotsResponse", "Snapshot"]


class Snapshot(BaseModel):
    id: str
    """The unique identifier of the snapshot."""

    metadata: Dict[str, str]
    """metadata associated with the snapshot."""

    source_devbox_id: str = FieldInfo(alias="sourceDevboxId")
    """The source devbox identifier."""

    name: Optional[str] = None
    """(Optional) The custom name of the snapshot."""


class DevboxDiskSnapshotsResponse(BaseModel):
    has_more: bool

    snapshots: List[Snapshot]
    """List of snapshots matching filter."""

    total_count: int
