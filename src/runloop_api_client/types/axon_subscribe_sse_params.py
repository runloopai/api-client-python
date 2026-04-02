# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AxonSubscribeSseParams"]


class AxonSubscribeSseParams(TypedDict, total=False):
    after_sequence: int
    """Sequence number after which to start streaming.

    Events with sequence > this value are returned. If unset, replay from the
    beginning.
    """
