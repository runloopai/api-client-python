# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ScoringFunctionParam"]


class ScoringFunctionParam(TypedDict, total=False):
    name: Required[str]
    """Name of scoring function. Names must only contain [a-zA-Z0-9_-]."""

    type: Required[str]
    """Type of the scoring function.

    Use 'bash' as type and fill out 'bash_script' field for scoring via custom bash
    scripts. Otherwise use a type corresponding to a custom scorer function or a
    public Runloop scorer type.
    """

    weight: Required[float]
    """Weight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """

    bash_script: Optional[str]
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be a float between 0.0 and 1.0, and look
    like "score=[0.0..1.0].
    """

    scorer_params: Optional[object]
    """
    Additional JSON structured context to pass to the scoring function if using
    custom scorer.
    """
