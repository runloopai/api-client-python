# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .scoring_function_result_view import ScoringFunctionResultView

__all__ = ["ScoringContractResultView"]


class ScoringContractResultView(BaseModel):
    score: float
    """Total score for all scoring contracts. This will be a value between 0 and 1."""

    scoring_function_results: List[ScoringFunctionResultView]
    """List of all individual scoring function results."""
