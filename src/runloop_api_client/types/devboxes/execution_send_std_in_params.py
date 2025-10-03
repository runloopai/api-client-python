# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ExecutionSendStdInParams"]


class ExecutionSendStdInParams(TypedDict, total=False):
    devbox_id: Required[str]

    text: str
    """Text to send to std in of the running execution."""
