# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ScoringFunctionResultView"]


class ScoringFunctionResultView(BaseModel):
    output: str
    """Log output of the scoring function."""

    score: float
    """Final score for the given scoring function."""

    scoring_function_name: str
    """Scoring function name that ran."""

    state: Literal["unknown", "complete", "error"]
    """The state of the scoring function application."""
