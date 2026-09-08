# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["AxonCreateParams"]


class AxonCreateParams(TypedDict, total=False):
    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the axon for organization."""

    name: Optional[str]
    """(Optional) Name for the axon."""
