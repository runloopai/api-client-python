# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .scope_entry_view_param import ScopeEntryViewParam

__all__ = ["RestrictedKeyCreateParams"]


class RestrictedKeyCreateParams(TypedDict, total=False):
    expires_at_ms: Optional[int]

    name: str

    scopes: Iterable[ScopeEntryViewParam]
