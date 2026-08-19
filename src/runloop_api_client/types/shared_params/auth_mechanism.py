# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["AuthMechanism"]


class AuthMechanism(TypedDict, total=False):
    """
    Defines how the primary credential is applied to requests proxied to the upstream.
    """

    type: Required[str]
    """The type of authentication mechanism: 'header', 'bearer', or 'basic'.

    For 'basic', store the secret as plain 'user:pass'; the proxy base64-encodes it.
    """

    key: Optional[str]
    """Only valid for 'header' type: the header name (e.g., 'x-api-key')."""
