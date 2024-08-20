# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DevboxExecuteSyncParams"]


class DevboxExecuteSyncParams(TypedDict, total=False):
    command: str
    """The command to execute on the Devbox."""
