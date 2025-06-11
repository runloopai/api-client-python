# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .secret_view import SecretView

__all__ = ["SecretListView"]


class SecretListView(BaseModel):
    has_more: bool
    """True if there are more results available beyond this page."""

    remaining_count: int
    """Number of Secrets remaining after this page."""

    secrets: List[SecretView]
    """List of Secret objects. Values are omitted for security."""

    total_count: int
    """Total number of Secrets across all pages."""
