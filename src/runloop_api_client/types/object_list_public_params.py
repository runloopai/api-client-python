# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ObjectListPublicParams"]


class ObjectListPublicParams(TypedDict, total=False):
    content_type: str
    """Filter objects by content type."""

    limit: int
    """The limit of items to return. Default is 20."""

    name: str
    """Filter objects by name (partial match supported)."""

    search: str
    """Search by object ID or name."""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""

    state: str
    """Filter objects by state (UPLOADING, READ_ONLY, DELETED)."""
