# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .scoring_contract_result_view import ScoringContractResultView

__all__ = ["ScenarioRunView"]


class ScenarioRunView(BaseModel):
    id: str
    """ID of the ScenarioRun."""

    devbox_id: str
    """ID of the Devbox on which the Scenario is running."""

    scenario_id: str
    """ID of the Scenario that has been run."""

    state: Literal["running", "scoring", "scored", "completed", "canceled", "timeout", "failed"]
    """The state of the ScenarioRun."""

    benchmark_run_id: Optional[str] = None
    """ID of the BenchmarkRun that this Scenario is associated with, if any."""

    duration_ms: Optional[int] = None
    """Duration scenario took to run."""

    name: Optional[str] = None
    """Optional name of ScenarioRun."""

    scoring_contract_result: Optional[ScoringContractResultView] = None
    """The input context for the Scenario."""

    start_time_ms: Optional[int] = None
    """The time that the scenario started"""
