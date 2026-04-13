# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["APIKeyCreatedView"]


class APIKeyCreatedView(BaseModel):
    id: Optional[str] = None

    expires_at_ms: Optional[int] = None

    key_secret: Optional[str] = None

    name: Optional[str] = None
