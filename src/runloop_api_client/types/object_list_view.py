# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .object_view import ObjectView

__all__ = ["ObjectListView"]


class ObjectListView(BaseModel):
    has_more: bool
    """True if there are more results available beyond this page."""

    objects: List[ObjectView]
    """List of Object entities."""

    remaining_count: int
    """Number of Objects remaining after this page."""

    total_count: int
    """Total number of Objects across all pages."""
