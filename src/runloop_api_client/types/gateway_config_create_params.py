# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .shared_params.custom_header import CustomHeader
from .shared_params.auth_mechanism import AuthMechanism

__all__ = ["GatewayConfigCreateParams"]


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
