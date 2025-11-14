# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ObjectListParams"]


class ObjectListParams(TypedDict, total=False):
    content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"]
    """Filter storage objects by content type."""

    limit: int
    """The limit of items to return. Default is 20."""

    name: str
    """Filter storage objects by name (partial match supported)."""

    search: str
    """Search by object ID or name."""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""

    state: Literal["UPLOADING", "READ_ONLY", "DELETED", "ERROR"]
    """Filter storage objects by state."""
