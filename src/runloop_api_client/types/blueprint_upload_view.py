# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .blueprint_view import BlueprintView

__all__ = ["BlueprintUploadView"]


class BlueprintUploadView(BaseModel):
    blueprint: BlueprintView
    """The created Blueprint, awaiting its image upload."""

    push_reference: str
    """The reference to push the image to, e.g. via docker push."""
