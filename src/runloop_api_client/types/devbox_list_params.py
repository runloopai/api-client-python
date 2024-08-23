# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DevboxListParams"]


class DevboxListParams(TypedDict, total=False):
    limit: str
    """Page Limit"""

    starting_after: str
    """Load the next page starting after the given token."""

    status: str
    """Filter by status"""
