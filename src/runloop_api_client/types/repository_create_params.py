# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["RepositoryCreateParams"]


class RepositoryCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the repository."""

    owner: Required[str]
    """Account owner of the repository."""

    blueprint_id: Optional[str]
    """ID of blueprint to use as base for resulting RepositoryVersion blueprint."""

    github_auth_token: Optional[str]
    """GitHub authentication token for accessing private repositories."""
