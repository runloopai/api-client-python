# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING

from .position import Position
from ..._models import BaseModel

__all__ = ["Range"]


class Range(BaseModel):
    end: Position
    """The range's end position."""

    start: Position
    """The range's start position."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
