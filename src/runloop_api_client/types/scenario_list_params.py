# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ScenarioListParams"]


class ScenarioListParams(TypedDict, total=False):
    benchmark_id: str
    """Filter scenarios by benchmark ID."""

    limit: int
    """The limit of items to return. Default is 20."""

    name: str
    """Query for Scenarios with a given name."""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""
