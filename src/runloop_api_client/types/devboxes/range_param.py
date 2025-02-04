# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .position_param import PositionParam

__all__ = ["RangeParam"]


class RangeParamTyped(TypedDict, total=False):
    end: Required[PositionParam]
    """The range's end position."""

    start: Required[PositionParam]
    """The range's start position."""


RangeParam: TypeAlias = Union[RangeParamTyped, Dict[str, object]]
