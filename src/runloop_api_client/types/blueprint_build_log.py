# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["BlueprintBuildLog"]


class BlueprintBuildLog(BaseModel):
    level: str
    """Log line severity level."""

    message: str
    """Log line message."""

    timestamp_ms: int
    """Time of log (Unix timestamp milliseconds)."""
