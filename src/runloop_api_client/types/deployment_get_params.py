# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DeploymentGetParams"]


class DeploymentGetParams(TypedDict, total=False):
    limit: str
    """Page Limit"""

    starting_after: str
    """Load the next page starting after the given token."""
