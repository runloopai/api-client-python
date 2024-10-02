# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxExecuteSyncParams"]


class DevboxExecuteSyncParams(TypedDict, total=False):
    command: Required[str]
    """The command to execute on the Devbox."""

    shell_name: str
    """Which named shell to run the command in."""
