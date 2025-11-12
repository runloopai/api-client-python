# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AgentListParams"]


class AgentListParams(TypedDict, total=False):
    is_public: bool
    """Filter agents by public visibility."""

    limit: int
    """The limit of items to return. Default is 20."""

    name: str
    """Filter agents by name (partial match supported)."""

    search: str
    """Search by agent ID or name."""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""
