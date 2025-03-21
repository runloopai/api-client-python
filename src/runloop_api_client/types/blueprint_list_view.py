# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .blueprint_view import BlueprintView

__all__ = ["BlueprintListView"]


class BlueprintListView(BaseModel):
    blueprints: List[BlueprintView]
    """List of blueprints matching filter."""

    has_more: bool

    remaining_count: int

    total_count: int
