# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AxonSubscribeSseParams"]


class AxonSubscribeSseParams(TypedDict, total=False):
    after_sequence: int
    """Resume SSE stream from events after this sequence number (used internally for reconnection)"""
