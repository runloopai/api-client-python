# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["DevboxLogsListView", "Log"]


class Log(BaseModel):
    level: Optional[str] = None
    """Log line severity level."""

    message: Optional[str] = None
    """Log line message."""

    timestamp_ms: Optional[int] = None
    """Time of log (Unix timestamp milliseconds)."""


class DevboxLogsListView(BaseModel):
    logs: Optional[List[Log]] = None
    """List of logs for the given devbox."""
