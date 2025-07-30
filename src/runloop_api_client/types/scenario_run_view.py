# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .scoring_contract_result_view import ScoringContractResultView

__all__ = ["ScenarioRunView"]


class ScenarioRunView(BaseModel):
    id: str
    """ID of the ScenarioRun."""

    devbox_id: str
    """ID of the Devbox on which the Scenario is running."""

    metadata: Dict[str, str]
    """User defined metadata to attach to the scenario run for organization."""

    scenario_id: str
    """ID of the Scenario that has been run."""

    state: Literal["running", "scoring", "scored", "completed", "canceled", "timeout", "failed"]
    """The state of the ScenarioRun."""

    benchmark_run_id: Optional[str] = None
    """ID of the BenchmarkRun that this Scenario is associated with, if any."""

    duration_ms: Optional[int] = None
    """Duration scenario took to run."""

    environment_variables: Optional[Dict[str, str]] = None
    """Environment variables used to run the scenario."""

    name: Optional[str] = None
    """Optional name of ScenarioRun."""

    purpose: Optional[str] = None
    """Purpose of the ScenarioRun."""

    scoring_contract_result: Optional[ScoringContractResultView] = None
    """The scoring result of the ScenarioRun."""

    secrets_provided: Optional[Dict[str, str]] = None
    """User secrets used to run the scenario."""

    start_time_ms: Optional[int] = None
    """The time that the scenario started"""
