# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ScoringFunctionParam"]


class ScoringFunctionParam(TypedDict, total=False):
    name: Required[str]
    """Name of scoring function."""

    weight: Required[float]
    """Wight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """

    bash_script: Optional[str]
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be an integer between 0 and 100, and look
    like "score=[0..100].
    """
