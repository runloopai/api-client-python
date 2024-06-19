# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["LatchFulfillParams"]


class LatchFulfillParams(TypedDict, total=False):
    result: Required[object]
    """Json of the event to complete the latch with"""
