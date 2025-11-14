# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..devbox_snapshot_view import DevboxSnapshotView

__all__ = ["DevboxSnapshotAsyncStatusView"]


class DevboxSnapshotAsyncStatusView(BaseModel):
    status: Literal["in_progress", "error", "complete", "deleted"]
    """The current status of the snapshot operation."""

    error_message: Optional[str] = None
    """Error message if the operation failed."""

    snapshot: Optional[DevboxSnapshotView] = None
    """The snapshot details if the operation completed successfully."""
