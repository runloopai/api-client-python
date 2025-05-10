# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel
from .input_context import InputContext
from .scoring_contract import ScoringContract
from .scenario_environment import ScenarioEnvironment

__all__ = ["ScenarioView"]


class ScenarioView(BaseModel):
    id: str
    """The ID of the Scenario."""

    input_context: InputContext
    """The input context for the Scenario."""

    metadata: Dict[str, str]
    """User defined metadata to attach to the scenario for organization."""

    name: str
    """The name of the Scenario."""

    scoring_contract: ScoringContract
    """The scoring contract for the Scenario."""

    environment: Optional[ScenarioEnvironment] = None
    """The Environment in which the Scenario is run."""

    is_public: Optional[bool] = None
    """Whether this scenario is public."""

    reference_output: Optional[str] = None
    """A string representation of the reference output to solve the scenario.

    Commonly can be the result of a git diff or a sequence of command actions to
    apply to the environment.
    """
