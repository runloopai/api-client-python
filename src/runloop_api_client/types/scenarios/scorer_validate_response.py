# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from ..scenario_environment import ScenarioEnvironment
from ..scoring_function_result_view import ScoringFunctionResultView

__all__ = ["ScorerValidateResponse"]


class ScorerValidateResponse(BaseModel):
    name: str
    """Name of the custom scorer."""

    scoring_context: object
    """Json context that gets passed to the custom scorer"""

    scoring_result: ScoringFunctionResultView
    """Result of the scoring function."""

    environment_parameters: Optional[ScenarioEnvironment] = None
    """The Environment in which the Scenario will run."""
