# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["RunListParams"]


# Split into separate params so that OO SDK list_runs params can omit the benchmark_id
# Neither of these params are exposed to the user, only the derived SDKBenchmarkListRunsParams
class RunSelfListParams(TypedDict, total=False):
    limit: int
    """The limit of items to return. Default is 20. Max is 5000."""

    name: str
    """Filter by name"""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""


class RunListParams(RunSelfListParams, total=False):
    benchmark_id: str
    """The Benchmark ID to filter by."""
