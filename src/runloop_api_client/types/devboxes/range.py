# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .position import Position
from ..._models import BaseModel

__all__ = ["Range"]


class Range(BaseModel):
    end: Position
    """The range's end position."""

    start: Position
    """The range's start position."""
