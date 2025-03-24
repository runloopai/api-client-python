# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["DevboxLogsListView", "Log"]


class Log(BaseModel):
    level: str
    """Log line severity level."""

    source: Literal["setup_commands", "entrypoint", "exec", "files", "stats"]
    """The source of the log."""

    timestamp_ms: int
    """Time of log (Unix timestamp milliseconds)."""

    cmd: Optional[str] = None
    """The Command Executed"""

    cmd_id: Optional[str] = None
    """Identifier of the associated command the log is sourced from."""

    exit_code: Optional[int] = None
    """The Exit Code of the command"""

    message: Optional[str] = None
    """Log line message."""

    shell_name: Optional[str] = None
    """The Shell name the cmd executed in."""


class DevboxLogsListView(BaseModel):
    logs: List[Log]
    """List of logs for the given devbox."""
