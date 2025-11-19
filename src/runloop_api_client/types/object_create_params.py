# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Literal, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ObjectCreateParams"]


# We manually define the content type here to use as a type hint in the SDK.
# If the API supports new content types, update this list accordingly.
ContentType = Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"]


class ObjectCreateParams(TypedDict, total=False):
    content_type: Required[ContentType]
    """The content type of the Object."""

    name: Required[str]
    """The name of the Object."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the object for organization."""

    ttl_ms: Optional[int]
    """
    Optional lifetime of the object in milliseconds, after which the object is
    automatically deleted. Time starts ticking after the object is created.
    """
