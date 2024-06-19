# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CodeHandleCreateParams"]


class CodeHandleCreateParams(TypedDict, total=False):
    auth_token: str
    """A short lived, scoped authentication token."""

    branch: str
    """Branch or tag to checkout instead of main."""

    name: str
    """The name of the code repository."""

    owner: str
    """The account that owns the repository."""
