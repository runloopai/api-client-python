# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["BenchmarkUpdateScenariosParams"]


class BenchmarkUpdateScenariosParams(TypedDict, total=False):
    scenarios_to_add: Optional[SequenceNotStr[str]]
    """Scenario IDs to add to the Benchmark."""

    scenarios_to_remove: Optional[SequenceNotStr[str]]
    """Scenario IDs to remove from the Benchmark."""
