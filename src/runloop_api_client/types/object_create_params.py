# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ObjectCreateParams"]


class ObjectCreateParams(TypedDict, total=False):
    content_type: Required[Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"]]
    """The content type of the Object."""

    name: Required[str]
    """The name of the Object."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the object for organization."""
