# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["BlueprintBuildLog"]


class BlueprintBuildLog(BaseModel):
    level: Optional[str] = None
    """Log line severity level."""

    message: Optional[str] = None
    """Log line message."""

    timestamp_ms: Optional[int] = None
    """Time of log (Unix timestamp milliseconds)."""
