# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .scoring_function_parameters import ScoringFunctionParameters

__all__ = ["ScoringContractParameters"]


class ScoringContractParameters(BaseModel):
    scoring_function_parameters: List[ScoringFunctionParameters]
    """A list of scoring functions used to evaluate the Scenario."""
