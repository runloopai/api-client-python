# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DevboxAsyncExecutionDetailView"]


class DevboxAsyncExecutionDetailView(BaseModel):
    devbox_id: Optional[str] = None
    """Devbox id where command was executed."""

    execution_id: Optional[str] = None
    """Ephemeral id of the execution in progress."""

    exit_status: Optional[int] = None
    """Exit code of command execution.

    This field will remain unset until the execution has completed.
    """

    shell_name: Optional[str] = None
    """Shell name."""

    status: Optional[Literal["running", "completed", "canceled"]] = None
    """Current status of the execution."""

    stderr: Optional[str] = None
    """Standard error generated by command.

    This field will remain unset until the execution has completed.
    """

    stdout: Optional[str] = None
    """Standard out generated by command.

    This field will remain unset until the execution has completed.
    """
