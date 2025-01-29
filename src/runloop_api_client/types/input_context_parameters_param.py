# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["InputContextParametersParam"]


class InputContextParametersParam(TypedDict, total=False):
    problem_statement: Required[str]
    """The problem statement for the Scenario."""
