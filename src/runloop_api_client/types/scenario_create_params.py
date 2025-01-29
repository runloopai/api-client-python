# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .input_context_param import InputContextParam
from .scoring_contract_param import ScoringContractParam
from .scenario_environment_param import ScenarioEnvironmentParam

__all__ = ["ScenarioCreateParams"]


class ScenarioCreateParams(TypedDict, total=False):
    input_context: Required[InputContextParam]
    """The input context for the Scenario."""

    name: Required[str]
    """Name of the scenario."""

    scoring_contract: Required[ScoringContractParam]
    """The scoring contract for the Scenario."""

    environment_parameters: Optional[ScenarioEnvironmentParam]
    """The Environment in which the Scenario will run."""
