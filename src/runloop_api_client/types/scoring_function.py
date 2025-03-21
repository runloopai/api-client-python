# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["ScoringFunction"]


class ScoringFunction(BaseModel):
    name: str
    """Name of scoring function. Names must only contain [a-zA-Z0-9_-]."""

    scoring_function: ScoringFunction
    """The scoring function to use for evaluating this scenario.

    The type field determines which built-in function to use.
    """

    weight: float
    """Weight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """
