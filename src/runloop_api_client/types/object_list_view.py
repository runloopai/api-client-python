# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .object_view import ObjectView

__all__ = ["ObjectListView"]


class ObjectListView(BaseModel):
    """A paginated list of Objects."""

    has_more: bool
    """True if there are more results available beyond this page."""

    objects: List[ObjectView]
    """List of Object entities."""

    remaining_count: Optional[int] = None
    """Number of Objects remaining after this page.

    Deprecated: will be removed in a future breaking change.
    """

    total_count: Optional[int] = None
    """Total number of Objects across all pages.

    Deprecated: will be removed in a future breaking change.
    """
