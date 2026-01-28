# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .benchmark_job_view import BenchmarkJobView

__all__ = ["BenchmarkJobListView"]


class BenchmarkJobListView(BaseModel):
    has_more: bool

    jobs: List[BenchmarkJobView]
    """List of BenchmarkJobs matching filter."""

    remaining_count: int

    total_count: int
