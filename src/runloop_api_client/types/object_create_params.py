# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ObjectCreateParams"]


class ObjectCreateParams(TypedDict, total=False):
    content_type: Required[
        Literal[
            "UNSPECIFIED",
            "TEXT_PLAIN",
            "TEXT_HTML",
            "TEXT_CSS",
            "TEXT_JAVASCRIPT",
            "TEXT_YAML",
            "TEXT_CSV",
            "APPLICATION_JSON",
            "APPLICATION_XML",
            "APPLICATION_PDF",
            "APPLICATION_ZIP",
            "APPLICATION_GZIP",
            "APPLICATION_TAR",
            "APPLICATION_TAR_GZIP",
            "APPLICATION_OCTET_STREAM",
            "IMAGE_JPEG",
            "IMAGE_PNG",
            "IMAGE_GIF",
            "IMAGE_SVG",
            "IMAGE_WEBP",
        ]
    ]
    """The content type of the Object."""

    name: Required[str]
    """The name of the Object."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the object for organization."""
