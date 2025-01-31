# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ComputerKeyboardInteractionParams"]


class ComputerKeyboardInteractionParams(TypedDict, total=False):
    action: Required[Literal["key", "type"]]
    """The keyboard action to perform."""

    text: Optional[str]
    """The text to type or the key (with optional modifier) to press."""
