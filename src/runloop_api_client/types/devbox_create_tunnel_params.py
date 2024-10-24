# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxCreateTunnelParams"]


class DevboxCreateTunnelParams(TypedDict, total=False):
    port: Required[int]
    """Devbox port that tunnel will expose."""
