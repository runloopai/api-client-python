# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .benchmark_view import BenchmarkView

__all__ = ["BenchmarkListView"]


class BenchmarkListView(BaseModel):
    benchmarks: List[BenchmarkView]
    """List of Benchmarks matching filter."""

    has_more: bool

    total_count: int
