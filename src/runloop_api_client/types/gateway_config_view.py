# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["GatewayConfigView", "AuthMechanism"]


class AuthMechanism(BaseModel):
    """How credentials should be applied to proxied requests."""

    type: str
    """The type of authentication mechanism: 'header', 'bearer'."""

    key: Optional[str] = None
    """For 'header' type: the header name (e.g., 'x-api-key')."""


class GatewayConfigView(BaseModel):
    """
    A GatewayConfig defines a configuration for proxying API requests through the credential gateway. It specifies the target endpoint and how credentials should be applied.
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

    description: Optional[str] = None
    """Optional description for this gateway configuration."""
