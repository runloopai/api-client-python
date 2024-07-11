# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["DevboxLogsListView", "Log"]


class Log(BaseModel):
    cmd: Optional[str] = None
    """The Command Executed"""

    cmd_id: Optional[str] = None
    """Identifier of the associated command the log is sourced from."""

    exit_code: Optional[int] = None
    """The Exit Code of the command"""

    level: Optional[str] = None
    """Log line severity level."""

    message: Optional[str] = None
    """Log line message."""

    source: Optional[Literal["setup_commands", "entrypoint", "exec"]] = None
    """The source of the log."""

    timestamp_ms: Optional[int] = None
    """Time of log (Unix timestamp milliseconds)."""


class DevboxLogsListView(BaseModel):
    logs: Optional[List[Log]] = None
    """List of logs for the given devbox."""
