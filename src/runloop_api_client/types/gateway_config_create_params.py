# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .shared_params.custom_header import CustomHeader

__all__ = ["GatewayConfigCreateParams", "AuthMechanism"]


class GatewayConfigCreateParams(TypedDict, total=False):
    auth_mechanism: Required[AuthMechanism]
    """How credentials should be applied to proxied requests.

    Specify the type ('header', 'bearer') and optional key field.
    """

    endpoint: Required[str]
    """The target endpoint URL (e.g., 'https://api.anthropic.com')."""

    name: Required[str]
    """The human-readable name for the GatewayConfig.

    Must be unique within your account.
    """

    custom_headers: Optional[Iterable[CustomHeader]]
    """Additional headers applied to proxied requests after the auth mechanism.

    At most 8 entries.
    """

    description: Optional[str]
    """Optional description for this gateway configuration."""


class AuthMechanism(TypedDict, total=False):
    """How credentials should be applied to proxied requests.

    Specify the type ('header', 'bearer') and optional key field.
    """

    type: Required[str]
    """The type of authentication mechanism: 'header', 'bearer', or 'basic'.

    For 'basic', store the secret as plain 'user:pass'; the gateway base64-encodes
    it.
    """

    key: Optional[str]
    """Only valid for 'header' type: the header name (e.g., 'x-api-key')."""
