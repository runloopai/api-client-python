# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ExecutionExecuteSyncParams"]


class ExecutionExecuteSyncParams(TypedDict, total=False):
    command: Required[str]
    """The command to execute via the Devbox shell.

    Commands are run from the user home directory in a fresh login shell.
    """

    attach_stdin: Optional[bool]
    """Whether to attach stdin streaming for async commands.

    Not valid for execute_sync endpoint. Defaults to false if not specified.
    """
