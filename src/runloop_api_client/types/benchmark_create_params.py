# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["BenchmarkCreateParams"]


class BenchmarkCreateParams(TypedDict, total=False):
    name: Required[str]
    """The name of the Benchmark."""

    scenario_ids: Optional[List[str]]
    """The Scenario IDs that make up the Benchmark."""
