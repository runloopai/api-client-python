# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional, TypedDict

__all__ = ["PtyConnectParams"]


class PtyConnectParams(TypedDict, total=False):
    command: Optional[str]
    """Optional command to start in the PTY."""

    cwd: Optional[str]
    """Optional working directory."""

    env: Optional[Dict[str, str]]
    """Environment variables to set for the PTY process."""

    cols: Optional[int]
    """Terminal width in columns."""

    rows: Optional[int]
    """Terminal height in rows."""
