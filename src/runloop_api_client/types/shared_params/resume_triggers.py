# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ResumeTriggers"]


class ResumeTriggers(TypedDict, total=False):
    """Triggers that can resume a suspended Devbox."""

    axon_event: Optional[bool]
    """When true, axon events targeting a suspended Devbox will trigger a resume."""

    http: Optional[bool]
    """When true, HTTP traffic to a suspended Devbox via tunnel will trigger a resume."""
