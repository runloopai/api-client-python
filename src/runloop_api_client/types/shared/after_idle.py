# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AfterIdle"]


class AfterIdle(BaseModel):
    idle_time_seconds: int
    """After idle_time_seconds, on_idle action will be taken."""

    on_idle: Literal["shutdown", "suspend"]
    """Action to take after Devbox becomes idle."""
