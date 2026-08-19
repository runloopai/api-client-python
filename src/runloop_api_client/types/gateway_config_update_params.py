# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .shared_params.custom_header import CustomHeader

__all__ = ["GatewayConfigUpdateParams", "AuthMechanism"]


class GatewayConfigUpdateParams(TypedDict, total=False):
    auth_mechanism: Optional[AuthMechanism]
    """
    Defines how credentials are applied to HTTP requests when proxying through the
    gateway.
    """

    custom_headers: Optional[Iterable[CustomHeader]]
    """New list of additional headers.

    Replaces the existing list entirely; use an empty list to clear all custom
    headers. At most 8 entries.
    """

    description: Optional[str]
    """New description for this gateway configuration."""

    endpoint: Optional[str]
    """New target endpoint URL (e.g., 'https://api.anthropic.com')."""

    name: Optional[str]
    """New name for the GatewayConfig. Must be unique within your account."""


class AuthMechanism(TypedDict, total=False):
    """
    Defines how credentials are applied to HTTP requests when proxying through the gateway.
    """

    type: Required[str]
    """The type of authentication mechanism: 'header', 'bearer', or 'basic'.

    For 'basic', store the secret as plain 'user:pass'; the gateway base64-encodes
    it.
    """

    key: Optional[str]
    """Only valid for 'header' type: the header name (e.g., 'x-api-key')."""
