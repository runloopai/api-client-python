# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DevboxListDiskSnapshotsParams"]


class DevboxListDiskSnapshotsParams(TypedDict, total=False):
    devbox_id: str
    """Devbox ID to filter by."""

    limit: int
    """The limit of items to return. Default is 20."""

    metadata_key: Annotated[str, PropertyInfo(alias="metadata[key]")]
    """Filter snapshots by metadata key-value pair.

    Can be used multiple times for different keys.
    """

    metadata_key_in: Annotated[str, PropertyInfo(alias="metadata[key][in]")]
    """Filter snapshots by metadata key with multiple possible values (OR condition)."""

    source_blueprint_id: str
    """Source Blueprint ID to filter snapshots by."""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""
