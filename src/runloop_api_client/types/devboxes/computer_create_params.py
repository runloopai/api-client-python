# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ComputerCreateParams", "DisplayDimensions"]


class ComputerCreateParams(TypedDict, total=False):
    display_dimensions: Optional[DisplayDimensions]
    """Customize the dimensions of the computer display."""

    name: Optional[str]
    """The name to use for the created computer."""


class DisplayDimensions(TypedDict, total=False):
    display_height_px: Required[int]
    """The height of the display being controlled by the model in pixels."""

    display_width_px: Required[int]
    """The width of the display being controlled by the model in pixels."""
