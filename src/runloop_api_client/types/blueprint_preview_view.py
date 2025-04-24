# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["BlueprintPreviewView"]


class BlueprintPreviewView(BaseModel):
    dockerfile: str
    """The Dockerfile contents that will built."""
