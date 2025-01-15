# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RepositoryConnectionView"]


class RepositoryConnectionView(BaseModel):
    id: str
    """The ID of the Repository."""

    name: str
    """The name of the Repository."""

    owner: str
    """The account owner of the Repository."""

    status: Literal["pending", "failure", "active"]
    """The current status of the Repository."""

    failure_reason: Optional[str] = None
    """Reason for failure, if the status is 'failure'."""
