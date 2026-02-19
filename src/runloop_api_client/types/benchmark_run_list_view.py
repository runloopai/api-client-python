# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .benchmark_run_view import BenchmarkRunView

__all__ = ["BenchmarkRunListView"]


class BenchmarkRunListView(BaseModel):
    has_more: bool

    runs: List[BenchmarkRunView]
    """List of BenchmarkRuns matching filter."""

    remaining_count: Optional[int] = None

    total_count: Optional[int] = None
