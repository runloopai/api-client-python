# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["InvocationLogsResponse", "Log"]


class Log(BaseModel):
    level: Optional[str] = None
    """Log line severity level."""

    message: Optional[str] = None
    """Log line message."""

    timestamp_ms: Optional[int] = None
    """Time of log (Unix timestamp milliseconds)."""


class InvocationLogsResponse(BaseModel):
    invocation_id: Optional[str] = None
    """ID of the invocation."""

    logs: Optional[List[Log]] = None
    """List of logs for the given invocation."""
