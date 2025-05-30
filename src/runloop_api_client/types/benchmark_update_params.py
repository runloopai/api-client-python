# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["BenchmarkUpdateParams"]


class BenchmarkUpdateParams(TypedDict, total=False):
    is_public: Required[bool]
    """Whether this benchmark is public."""

    name: Required[str]
    """The name of the Benchmark. This must be unique."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the benchmark for organization."""

    scenario_ids: Optional[List[str]]
    """The Scenario IDs that make up the Benchmark."""
