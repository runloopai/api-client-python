# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["InspectionSourceParam"]


class InspectionSourceParam(TypedDict, total=False):
    inspection_id: Required[str]
    """The ID of a repository inspection."""

    github_auth_token: Optional[str]
    """GitHub authentication token for accessing private repositories."""
