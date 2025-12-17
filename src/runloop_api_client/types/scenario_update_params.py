# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, TypedDict

from .._types import SequenceNotStr
from .input_context_update_param import InputContextUpdateParam
from .scenario_environment_param import ScenarioEnvironmentParam
from .scoring_contract_update_param import ScoringContractUpdateParam

__all__ = ["ScenarioUpdateParams"]


class ScenarioUpdateParams(TypedDict, total=False):
    environment_parameters: Optional[ScenarioEnvironmentParam]
    """The Environment in which the Scenario will run."""

    input_context: Optional[InputContextUpdateParam]
    """The input context for the Scenario."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the scenario. Pass in empty map to clear."""

    name: Optional[str]
    """Name of the scenario. Cannot be blank."""

    reference_output: Optional[str]
    """A string representation of the reference output to solve the scenario.

    Commonly can be the result of a git diff or a sequence of command actions to
    apply to the environment. Pass in empty string to clear.
    """

    required_environment_variables: Optional[SequenceNotStr[str]]
    """Environment variables required to run the scenario.

    Pass in empty list to clear.
    """

    required_secret_names: Optional[SequenceNotStr[str]]
    """Secrets required to run the scenario. Pass in empty list to clear."""

    scoring_contract: Optional[ScoringContractUpdateParam]
    """The scoring contract for the Scenario."""

    validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]]
    """Validation strategy. Pass in empty string to clear."""
