# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SecretListParams"]


class SecretListParams(TypedDict, total=False):
    limit: int
    """The limit of items to return. Default is 20."""
