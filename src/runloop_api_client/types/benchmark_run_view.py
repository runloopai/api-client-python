# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BenchmarkRunView"]


class BenchmarkRunView(BaseModel):
    id: str
    """The ID of the BenchmarkRun."""

    benchmark_id: str
    """The ID of the Benchmark."""

    start_time_ms: int
    """The time the benchmark run execution started (Unix timestamp milliseconds)."""

    state: Literal["running", "completed"]
    """The state of the BenchmarkRun."""

    duration_ms: Optional[int] = None
    """The duration for the BenchmarkRun to complete."""

    name: Optional[str] = None
    """The name of the BenchmarkRun."""

    score: Optional[float] = None
    """The final score across the BenchmarkRun, present once completed.

    Calculated as sum of scenario scores / number of scenario runs.
    """
