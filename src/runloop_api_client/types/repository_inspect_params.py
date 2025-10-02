# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["RepositoryInspectParams"]


class RepositoryInspectParams(TypedDict, total=False):
    github_auth_token: Optional[str]
    """GitHub authentication token for accessing private repositories."""
