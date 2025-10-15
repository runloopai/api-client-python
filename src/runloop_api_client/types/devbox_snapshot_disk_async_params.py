# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["DevboxSnapshotDiskAsyncParams"]


class DevboxSnapshotDiskAsyncParams(TypedDict, total=False):
    commit_message: Optional[str]
    """(Optional) Commit message associated with the snapshot (max 1000 characters)"""

    metadata: Optional[Dict[str, str]]
    """(Optional) Metadata used to describe the snapshot"""

    name: Optional[str]
    """(Optional) A user specified name to give the snapshot"""
