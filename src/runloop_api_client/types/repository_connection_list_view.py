# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .repository_connection_view import RepositoryConnectionView

__all__ = ["RepositoryConnectionListView"]


class RepositoryConnectionListView(BaseModel):
    has_more: bool

    repositories: List[RepositoryConnectionView]
    """List of repositories matching filter."""

    remaining_count: Optional[int] = None

    total_count: Optional[int] = None
