# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["PtyControlParams"]


class PtyControlParams(TypedDict, total=False):
    action: Literal["resize", "signal", "close"]

    cols: int

    rows: int

    signal: str
