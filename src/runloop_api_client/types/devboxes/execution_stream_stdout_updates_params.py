# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ExecutionStreamStdoutUpdatesParams"]


class ExecutionStreamStdoutUpdatesParams(TypedDict, total=False):
    devbox_id: Required[str]

    offset: str
    """
    The byte offset to start the stream from (if unspecified, starts from the
    beginning of the stream)
    """
