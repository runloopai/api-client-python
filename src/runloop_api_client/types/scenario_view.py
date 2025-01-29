# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .input_context_parameters import InputContextParameters

__all__ = ["ScenarioView", "ScoringContract", "ScoringContractScoringFunctionParameter", "Environment"]


class ScoringContractScoringFunctionParameter(BaseModel):
    name: str
    """Name of scoring function."""

    weight: float
    """Wight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """

    bash_script: Optional[str] = None
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be an integer between 0 and 100, and look
    like "score=[0..100].
    """


class ScoringContract(BaseModel):
    scoring_function_parameters: List[ScoringContractScoringFunctionParameter]
    """A list of scoring functions used to evaluate the Scenario."""


class Environment(BaseModel):
    blueprint_id: Optional[str] = None
    """Use the blueprint with matching ID."""

    prebuilt_id: Optional[str] = None
    """Use the prebuilt with matching ID."""

    snapshot_id: Optional[str] = None
    """Use the snapshot with matching ID."""


class ScenarioView(BaseModel):
    id: str
    """The ID of the Scenario."""

    input_context: InputContextParameters
    """The input context for the Scenario."""

    name: str
    """The name of the Scenario."""

    scoring_contract: ScoringContract
    """The scoring contract for the Scenario."""

    environment: Optional[Environment] = None
    """The Environment in which the Scenario is run."""
