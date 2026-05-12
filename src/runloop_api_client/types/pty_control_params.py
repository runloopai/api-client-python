# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional, TypedDict
from typing_extensions import Literal

__all__ = ["PtyControlParams"]


class PtyControlParams(TypedDict, total=False):
    action: Literal["resize", "signal", "close"]
    """Control action to apply to the PTY session."""

    cols: Optional[int]
    """Terminal width in columns for resize actions."""

    rows: Optional[int]
    """Terminal height in rows for resize actions."""

    signal: Optional[str]
    """Signal name for signal actions."""
