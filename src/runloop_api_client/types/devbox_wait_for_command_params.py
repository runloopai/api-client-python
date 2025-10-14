# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["DevboxWaitForCommandParams"]


class DevboxWaitForCommandParams(TypedDict, total=False):
    devbox_id: Required[str]

    statuses: Required[List[Literal["queued", "running", "completed"]]]
    """The command execution statuses to wait for.

    At least one status must be provided. The command will be returned as soon as it
    reaches any of the provided statuses.
    """

    last_n: str
    """Last n lines of standard error / standard out to return (default: 100)"""

    timeout_seconds: Optional[int]
    """(Optional) Timeout in seconds to wait for the status, up to 60 seconds.

    Defaults to 60 seconds.
    """
