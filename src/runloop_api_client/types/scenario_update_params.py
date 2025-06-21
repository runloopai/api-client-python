# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .input_context_param import InputContextParam
from .scoring_contract_param import ScoringContractParam
from .scenario_environment_param import ScenarioEnvironmentParam

__all__ = ["ScenarioUpdateParams"]


class ScenarioUpdateParams(TypedDict, total=False):
    environment_parameters: Optional[ScenarioEnvironmentParam]
    """The Environment in which the Scenario will run."""

    input_context: Optional[InputContextParam]
    """The input context for the Scenario."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the scenario for organization."""

    name: Optional[str]
    """Name of the scenario."""

    reference_output: Optional[str]
    """A string representation of the reference output to solve the scenario.

    Commonly can be the result of a git diff or a sequence of command actions to
    apply to the environment.
    """

    scoring_contract: Optional[ScoringContractParam]
    """The scoring contract for the Scenario."""
