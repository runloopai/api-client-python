# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .input_context_parameters_param import InputContextParametersParam

__all__ = [
    "ScenarioCreateParams",
    "ScoringContract",
    "ScoringContractScoringFunctionParameter",
    "EnvironmentParameters",
]


class ScenarioCreateParams(TypedDict, total=False):
    input_context: Required[InputContextParametersParam]
    """The input context for the Scenario."""

    name: Required[str]
    """Name of the scenario."""

    scoring_contract: Required[ScoringContract]
    """The scoring contract for the Scenario."""

    environment_parameters: Optional[EnvironmentParameters]
    """The Environment in which the Scenario will run."""


class ScoringContractScoringFunctionParameter(TypedDict, total=False):
    name: Required[str]
    """Name of scoring function."""

    weight: Required[float]
    """Wight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """

    bash_script: Optional[str]
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be an integer between 0 and 100, and look
    like "score=[0..100].
    """


class ScoringContract(TypedDict, total=False):
    scoring_function_parameters: Required[Iterable[ScoringContractScoringFunctionParameter]]
    """A list of scoring functions used to evaluate the Scenario."""


class EnvironmentParameters(TypedDict, total=False):
    blueprint_id: Optional[str]
    """Use the blueprint with matching ID."""

    prebuilt_id: Optional[str]
    """Use the prebuilt with matching ID."""

    snapshot_id: Optional[str]
    """Use the snapshot with matching ID."""
