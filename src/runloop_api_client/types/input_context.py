# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["InputContext"]


class InputContext(BaseModel):
    problem_statement: str
    """The problem statement for the Scenario."""

    additional_context: Optional[object] = None
    """Additional JSON structured input context."""
