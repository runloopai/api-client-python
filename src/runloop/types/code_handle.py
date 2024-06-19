# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["CodeHandle"]


class CodeHandle(BaseModel):
    id: Optional[str] = None
    """The id of the CodeHandle."""

    commit_hash: Optional[str] = None
    """The git commit hash associated with the code."""

    owner: Optional[str] = None
    """The owner of the repository."""

    repo_name: Optional[str] = None
    """The name of the source repository."""
