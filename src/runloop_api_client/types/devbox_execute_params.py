# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DevboxExecuteParams"]


class DevboxExecuteParams(TypedDict, total=False):
    command: Required[str]
    """The command to execute via the Devbox shell.

    Commands are run from the user home directory in a fresh login shell.
    """

    command_id: Required[str]
    """The command ID in UUIDv7 string format for idempotency and tracking"""

    last_n: str
    """Last n lines of standard error / standard out to return (default: 100)"""

    optimistic_timeout: Optional[int]
    """Timeout in seconds to wait for command completion, up to 25 seconds.

    Defaults to 25 seconds. Operation is not killed.
    """
