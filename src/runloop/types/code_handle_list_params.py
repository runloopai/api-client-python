# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CodeHandleListParams"]


class CodeHandleListParams(TypedDict, total=False):
    owner: str
    """Repo owner name."""

    repo_name: str
    """Repo name."""
