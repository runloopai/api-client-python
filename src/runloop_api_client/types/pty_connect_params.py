# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PtyConnectParams"]


class PtyConnectParams(TypedDict, total=False):
    cols: str
    """Optional initial terminal width in character cells (1..=1000).

    Defaults to 80 when omitted. Applied only if both cols and rows are provided;
    otherwise ignored.
    """

    rows: str
    """Optional initial terminal height in character cells (1..=1000).

    Defaults to 24 when omitted. Applied only if both cols and rows are provided;
    otherwise ignored.
    """
