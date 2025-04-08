# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .scoring_contract_result_view import ScoringContractResultView

__all__ = ["BenchmarkRunView", "ScenarioRun"]


class ScenarioRun(BaseModel):
    scenario_id: str
    """ID of the Scenario that has been run."""

    scoring_result: ScoringContractResultView = FieldInfo(alias="scoringResult")
    """The scoring result of the ScenarioRun."""

    scenario_run_id: Optional[str] = FieldInfo(alias="scenarioRunId", default=None)
    """ID of the scenario run."""


class BenchmarkRunView(BaseModel):
    id: str
    """The ID of the BenchmarkRun."""

    benchmark_id: str
    """The ID of the Benchmark."""

    metadata: Dict[str, str]
    """User defined metadata to attach to the benchmark run for organization."""

    pending_scenarios: List[str]
    """List of Scenarios that need to be completed before benchmark can be completed."""

    scenario_runs: List[ScenarioRun]
    """List of Scenarios have been completed."""

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
