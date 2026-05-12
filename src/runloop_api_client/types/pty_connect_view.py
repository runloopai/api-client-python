# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["PtyConnectView"]


class PtyConnectView(BaseModel):
    connect_url: str
    """WebSocket URL path used to attach to the PTY stream."""

    session_id: Optional[str] = None
    """Optional server-side PTY session identifier."""
