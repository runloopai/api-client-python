# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["LogListParams"]


class LogListParams(TypedDict, total=False):
    execution_id: str
    """ID of execution to filter logs by."""

    shell_name: str
    """Shell Name to filter logs by."""
