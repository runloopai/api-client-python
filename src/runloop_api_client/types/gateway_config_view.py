# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .shared.custom_header import CustomHeader

__all__ = ["GatewayConfigView", "AuthMechanism"]


class AuthMechanism(BaseModel):
    """How credentials should be applied to proxied requests."""

    type: str
    """The type of authentication mechanism: 'header', 'bearer', or 'basic'.

    For 'basic', store the secret as plain 'user:pass'; the gateway base64-encodes
    it.
    """

    key: Optional[str] = None
    """Only valid for 'header' type: the header name (e.g., 'x-api-key')."""


class GatewayConfigView(BaseModel):
    """
    A GatewayConfig defines a configuration for proxying API requests through the agent gateway. It specifies the target endpoint and how credentials should be applied.
    """

    id: str
    """The unique identifier of the GatewayConfig."""

    auth_mechanism: AuthMechanism
    """How credentials should be applied to proxied requests."""

    create_time_ms: int
    """Creation time of the GatewayConfig (Unix timestamp in milliseconds)."""

    endpoint: str
    """The target endpoint URL (e.g., 'https://api.anthropic.com')."""

    name: str
    """The human-readable name of the GatewayConfig.

    Unique per account (or globally for system configs).
    """

    account_id: Optional[str] = None
    """The account ID that owns this config."""

    custom_headers: Optional[List[CustomHeader]] = None
    """Additional headers applied to proxied requests after the auth mechanism.

    Secret-backed entries reference the secret by 'sec\\__' id; values are never
    returned.
    """

    description: Optional[str] = None
    """Optional description for this gateway configuration."""
