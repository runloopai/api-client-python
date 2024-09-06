# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .blueprint_view import BlueprintView

__all__ = ["BlueprintListView"]


class BlueprintListView(BaseModel):
    blueprints: Optional[List[BlueprintView]] = None
    """List of blueprints matching filter."""

    has_more: Optional[bool] = None

    total_count: Optional[int] = None
