# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
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
    """User defined metadata to attach to the scenario for organization."""

    name: Optional[str]
    """Name of the scenario."""

    reference_output: Optional[str]
    """A string representation of the reference output to solve the scenario.

    Commonly can be the result of a git diff or a sequence of command actions to
    apply to the environment.
    """

    required_env_vars: Annotated[Optional[List[str]], PropertyInfo(alias="requiredEnvVars")]
    """Environment variables required to run the benchmark."""

    scoring_contract: Optional[ScoringContractUpdateParam]
    """The scoring contract for the Scenario."""
