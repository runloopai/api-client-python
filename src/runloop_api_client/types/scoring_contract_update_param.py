# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .scoring_function_param import ScoringFunctionParam

__all__ = ["ScoringContractUpdateParam"]


class ScoringContractUpdateParam(TypedDict, total=False):
    scoring_function_parameters: Optional[Iterable[ScoringFunctionParam]]
    """A list of scoring functions used to evaluate the Scenario."""
