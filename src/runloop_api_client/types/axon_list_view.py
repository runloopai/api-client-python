# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .axon_view import AxonView

__all__ = ["AxonListView"]


class AxonListView(BaseModel):
    axons: List[AxonView]
    """List of active axons."""
