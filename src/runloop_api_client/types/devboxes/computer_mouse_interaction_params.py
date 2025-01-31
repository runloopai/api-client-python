# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ComputerMouseInteractionParams", "Coordinate"]


class ComputerMouseInteractionParams(TypedDict, total=False):
    action: Required[
        Literal["mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click"]
    ]
    """The mouse action to perform."""

    coordinate: Optional[Coordinate]
    """
    The x (pixels from the left) and y (pixels from the top) coordinates for the
    mouse to move or click-drag. Required only by `action=mouse_move` or
    `action=left_click_drag`
    """


class Coordinate(TypedDict, total=False):
    x: Required[int]
    """The x coordinate (pixels from the left) for the mouse to move or click-drag."""

    y: Required[int]
    """The y coordinate (pixels from the top) for the mouse to move or click-drag."""
