# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .position_param import PositionParam

__all__ = ["RangeParam"]


class RangeParam(TypedDict, total=False):
    end: Required[PositionParam]
    """The range's end position."""

    start: Required[PositionParam]
    """The range's start position."""
