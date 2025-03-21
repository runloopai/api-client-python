# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .benchmark_run_view import BenchmarkRunView

__all__ = ["BenchmarkRunListView"]


class BenchmarkRunListView(BaseModel):
    has_more: bool

    remaining_count: int

    runs: List[BenchmarkRunView]
    """List of BenchmarkRuns matching filter."""

    total_count: int
