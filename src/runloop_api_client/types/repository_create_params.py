# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["RepositoryCreateParams"]


class RepositoryCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the repository."""

    owner: Required[str]
    """Account owner of the repository."""
