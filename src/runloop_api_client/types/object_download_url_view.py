# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ObjectDownloadURLView"]


class ObjectDownloadURLView(BaseModel):
    """A response containing a presigned download URL for an Object."""

    download_url: str
    """The presigned download URL for the Object."""
