# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .devbox_view import DevboxView

__all__ = ["DevboxListView"]


class DevboxListView(BaseModel):
    devboxes: Optional[List[DevboxView]] = None
    """List of devboxes matching filter."""
