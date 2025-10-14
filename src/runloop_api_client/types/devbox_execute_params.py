# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DevboxExecuteParams"]


class DevboxExecuteParams(TypedDict, total=False):
    command: Required[str]
    """The command to execute via the Devbox shell.

    By default, commands are run from the user home directory unless shell_name is
    specified. If shell_name is specified the command is run from the directory
    based on the recent state of the persistent shell.
    """

    command_id: Required[str]
    """The command ID in UUIDv7 string format for idempotency and tracking"""

    last_n: str
    """Last n lines of standard error / standard out to return (default: 100)"""

    optimistic_timeout: Optional[int]
    """Timeout in seconds to wait for command completion.

    Operation is not killed. Max is 600 seconds.
    """

    shell_name: Optional[str]
    """The name of the persistent shell to create or use if already created.

    When using a persistent shell, the command will run from the directory at the
    end of the previous command and environment variables will be preserved.
    """
