# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DevboxExecutionDetailView"]


class DevboxExecutionDetailView(BaseModel):
    devbox_id: str
    """Devbox id where command was executed."""

    exit_status: int
    """Exit status of command execution."""

    stderr: str
    """Standard error generated by command."""

    stdout: str
    """Standard out generated by command."""

    shell_name: Optional[str] = None
    """Shell name."""
