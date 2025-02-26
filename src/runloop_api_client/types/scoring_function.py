# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ScoringFunction"]


class ScoringFunction(BaseModel):
    name: str
    """Name of scoring function. Names must only contain [a-zA-Z0-9_-]."""

    type: str
    """Type of the scoring function.

    Use 'bash' as type and fill out 'bash_script' field for scoring via custom bash
    scripts. Otherwise use a type corresponding to a custom scorer function or a
    public Runloop scorer type.
    """

    weight: float
    """Weight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """

    bash_script: Optional[str] = None
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be a float between 0.0 and 1.0, and look
    like "score=[0.0..1.0].
    """

    scorer_params: Optional[object] = None
    """
    Additional JSON structured context to pass to the scoring function if using
    custom scorer.
    """
