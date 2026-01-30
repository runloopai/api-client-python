# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

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

    description: Optional[str]
    """Optional description for this gateway configuration."""


class AuthMechanism(TypedDict, total=False):
    """How credentials should be applied to proxied requests.

    Specify the type ('header', 'bearer') and optional key field.
    """

    type: Required[str]
    """The type of authentication mechanism: 'header', 'bearer'."""

    key: Optional[str]
    """For 'header' type: the header name (e.g., 'x-api-key')."""
