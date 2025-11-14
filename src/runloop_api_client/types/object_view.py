# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ObjectView"]


class ObjectView(BaseModel):
    id: str
    """The unique identifier of the Object."""

    content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"]
    """The content type of the Object."""

    create_time_ms: int
    """The creation time of the Object in milliseconds since epoch."""

    name: str
    """The name of the Object."""

    state: Literal["UPLOADING", "READ_ONLY", "DELETED", "ERROR"]
    """The current state of the Object."""

    delete_after_time_ms: Optional[int] = None
    """The time after which the Object will be deleted in milliseconds since epoch."""

    size_bytes: Optional[int] = None
    """The size of the Object content in bytes (null until uploaded)."""

    upload_url: Optional[str] = None
    """Presigned URL for uploading content to S3 (only present on create)."""
