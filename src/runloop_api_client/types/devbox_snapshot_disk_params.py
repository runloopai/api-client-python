# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["DevboxSnapshotDiskParams"]


class DevboxSnapshotDiskParams(TypedDict, total=False):
    metadata: Dict[str, str]
    """(Optional) Metadata used to describe the snapshot"""

    name: str
    """(Optional) A user specified name to give the snapshot"""
