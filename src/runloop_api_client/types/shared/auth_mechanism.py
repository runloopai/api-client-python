# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["AuthMechanism"]


class AuthMechanism(BaseModel):
    """
    Defines how the primary credential is applied to requests proxied to the upstream.
    """

    type: str
    """The type of authentication mechanism: 'header', 'bearer', or 'basic'.

    For 'basic', store the secret as plain 'user:pass'; the proxy base64-encodes it.
    """

    key: Optional[str] = None
    """Only valid for 'header' type: the header name (e.g., 'x-api-key')."""
