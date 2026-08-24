# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxCreateGatewayTokenParams"]


class DevboxCreateGatewayTokenParams(TypedDict, total=False):
    gateway: Required[str]
    """The gateway config to use. Can be a gateway config ID (gwc_xxx) or name."""

    secret: Required[str]
    """The secret containing the credential. Can be a secret ID or name."""
