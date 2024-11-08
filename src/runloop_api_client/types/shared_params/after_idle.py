# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AfterIdle"]


class AfterIdle(TypedDict, total=False):
    idle_time_seconds: Required[int]
    """After idle_time_seconds, on_idle action will be taken."""

    on_idle: Required[Literal["shutdown", "suspend"]]
    """Action to take after Devbox becomes idle."""
