# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["InputContextUpdateParam"]


class InputContextUpdateParam(TypedDict, total=False):
    additional_context: Optional[object]
    """Additional JSON structured input context."""

    problem_statement: Optional[str]
    """The problem statement for the Scenario."""
