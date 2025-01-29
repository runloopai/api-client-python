# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .scoring_function import ScoringFunction

__all__ = ["ScoringContract"]


class ScoringContract(BaseModel):
    scoring_function_parameters: List[ScoringFunction]
    """A list of scoring functions used to evaluate the Scenario."""
