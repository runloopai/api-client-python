# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .input_context_parameters import InputContextParameters
from .scoring_contract_parameters import ScoringContractParameters
from .scenario_environment_parameters import ScenarioEnvironmentParameters

__all__ = ["ScenarioView"]


class ScenarioView(BaseModel):
    id: str
    """The ID of the Scenario."""

    input_context: InputContextParameters
    """The input context for the Scenario."""

    name: str
    """The name of the Scenario."""

    scoring_contract: ScoringContractParameters
    """The scoring contract for the Scenario."""

    environment: Optional[ScenarioEnvironmentParameters] = None
    """The Environment in which the Scenario is run."""
