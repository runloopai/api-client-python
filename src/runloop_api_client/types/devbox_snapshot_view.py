# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["DevboxSnapshotView"]


class DevboxSnapshotView(BaseModel):
    id: str
    """The unique identifier of the snapshot."""

    create_time_ms: int
    """Creation time of the Snapshot (Unix timestamp milliseconds)."""

    metadata: Dict[str, str]
    """User defined metadata associated with the snapshot."""

    source_devbox_id: str
    """The source Devbox ID this snapshot was created from."""

    commit_message: Optional[str] = None
    """(Optional) The commit message of the snapshot (max 1000 characters)."""

    name: Optional[str] = None
    """(Optional) The custom name of the snapshot."""

    source_blueprint_id: Optional[str] = None
    """(Optional) The source Blueprint ID this snapshot was created from."""
