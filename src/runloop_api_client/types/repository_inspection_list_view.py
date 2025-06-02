# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .repository_inspection_details import RepositoryInspectionDetails

__all__ = ["RepositoryInspectionListView"]


class RepositoryInspectionListView(BaseModel):
    inspections: List[RepositoryInspectionDetails]
    """List of inspections for this repository."""
