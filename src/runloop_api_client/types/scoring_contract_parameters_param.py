# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .scoring_function_parameters_param import ScoringFunctionParametersParam

__all__ = ["ScoringContractParametersParam"]


class ScoringContractParametersParam(TypedDict, total=False):
    scoring_function_parameters: Required[Iterable[ScoringFunctionParametersParam]]
    """A list of scoring functions used to evaluate the Scenario."""
