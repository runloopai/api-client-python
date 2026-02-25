# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .secret_view import SecretView

__all__ = ["SecretListView"]


class SecretListView(BaseModel):
    """A paginated list of Secrets."""

    has_more: bool
    """True if there are more results available beyond this page."""

    secrets: List[SecretView]
    """List of Secret objects. Values are omitted for security."""

    remaining_count: Optional[int] = None
    """Number of Secrets remaining after this page.

    Deprecated: will be removed in a future breaking change.
    """

    total_count: Optional[int] = None
    """Total number of Secrets across all pages.

    Deprecated: will be removed in a future breaking change.
    """
