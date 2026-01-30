# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["GatewayConfigUpdateParams", "AuthMechanism"]


class GatewayConfigUpdateParams(TypedDict, total=False):
    auth_mechanism: Optional[AuthMechanism]
    """New authentication mechanism for applying credentials to proxied requests."""

    description: Optional[str]
    """New description for this gateway configuration."""

    endpoint: Optional[str]
    """New target endpoint URL (e.g., 'https://api.anthropic.com')."""

    name: Optional[str]
    """New name for the GatewayConfig. Must be unique within your account."""


class AuthMechanism(TypedDict, total=False):
    """New authentication mechanism for applying credentials to proxied requests."""

    type: Required[str]
    """The type of authentication mechanism: 'header', 'bearer'."""

    key: Optional[str]
    """For 'header' type: the header name (e.g., 'x-api-key')."""
