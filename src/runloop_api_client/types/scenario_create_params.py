# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .input_context_parameters_param import InputContextParametersParam
from .scoring_contract_parameters_param import ScoringContractParametersParam
from .scenario_environment_parameters_param import ScenarioEnvironmentParametersParam

__all__ = ["ScenarioCreateParams"]


class ScenarioCreateParams(TypedDict, total=False):
    input_context: Required[InputContextParametersParam]
    """The input context for the Scenario."""

    name: Required[str]
    """Name of the scenario."""

    scoring_contract: Required[ScoringContractParametersParam]
    """The scoring contract for the Scenario."""

    environment_parameters: Optional[ScenarioEnvironmentParametersParam]
    """The Environment in which the Scenario will run."""
