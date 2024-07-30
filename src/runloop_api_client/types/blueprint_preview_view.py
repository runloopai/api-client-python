# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["BlueprintPreviewView"]


class BlueprintPreviewView(BaseModel):
    dockerfile: Optional[str] = None
    """The Dockerfile contents that will built."""
