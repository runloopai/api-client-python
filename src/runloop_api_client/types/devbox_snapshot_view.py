# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DevboxSnapshotView"]


class DevboxSnapshotView(BaseModel):
    id: str
    """The unique identifier of the snapshot."""

    metadata: Dict[str, str]
    """metadata associated with the snapshot."""

    source_devbox_id: str = FieldInfo(alias="sourceDevboxId")
    """The source devbox identifier."""

    name: Optional[str] = None
    """(Optional) The custom name of the snapshot."""
