# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .repository_version_details import RepositoryVersionDetails

__all__ = ["RepositoryVersionListView"]


class RepositoryVersionListView(BaseModel):
    analyzed_versions: List[RepositoryVersionDetails]
    """List of analyzed versions of this repository."""
