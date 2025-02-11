# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ScoringFunction"]


class ScoringFunction(BaseModel):
    name: str
    """Name of scoring function."""

    type: str
    """Type of the scoring function. Defaults to bash script."""

    weight: float
    """Wight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """

    bash_script: Optional[str] = None
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be an integer between 0 and 100, and look
    like "score=[0..100].
    """

    scorer_params: Optional[object] = None
    """
    Additional JSON structured context to pass to the scoring function if using
    custom scorer.
    """
