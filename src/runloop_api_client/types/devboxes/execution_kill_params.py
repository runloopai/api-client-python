# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ExecutionKillParams"]


class ExecutionKillParams(TypedDict, total=False):
    devbox_id: Required[str]

    kill_process_group: Optional[bool]
