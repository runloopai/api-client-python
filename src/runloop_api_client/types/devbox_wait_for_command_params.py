# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["DevboxWaitForCommandParams"]


class DevboxWaitForCommandParams(TypedDict, total=False):
    statuses: Required[
        List[
            Literal[
                "provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"
            ]
        ]
    ]
    """The Devbox statuses to wait for.

    At least one status must be provided. The devbox will be returned as soon as it
    reaches any of the provided statuses.
    """

    timeout_seconds: Optional[int]
    """(Optional) Timeout in seconds to wait for the status, up to 30 seconds.

    Defaults to 10 seconds.
    """
