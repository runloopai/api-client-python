# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["RepositoryConnectionView"]


class RepositoryConnectionView(BaseModel):
    id: str
    """The ID of the Repository."""

    name: str
    """The name of the Repository."""

    owner: str
    """The account owner of the Repository."""
