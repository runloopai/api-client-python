# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .scope_entry_view import ScopeEntryView

__all__ = ["RestrictedKeyCreatedView"]


class RestrictedKeyCreatedView(BaseModel):
    id: Optional[str] = None

    expires_at_ms: Optional[int] = None

    key_secret: Optional[str] = None

    name: Optional[str] = None

    scopes: Optional[List[ScopeEntryView]] = None
