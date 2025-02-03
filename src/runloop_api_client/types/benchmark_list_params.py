# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BenchmarkListParams"]


class BenchmarkListParams(TypedDict, total=False):
    limit: int
    """The limit of items to return. Default is 20."""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""
