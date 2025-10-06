# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ExecutionSendStdInParams"]


class ExecutionSendStdInParams(TypedDict, total=False):
    devbox_id: Required[str]

    signal: Optional[Literal["EOF", "INTERRUPT"]]
    """Signal to send to std in of the running execution."""

    text: Optional[str]
    """Text to send to std in of the running execution."""
