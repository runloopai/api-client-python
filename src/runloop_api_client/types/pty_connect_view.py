# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["PtyConnectView"]


class PtyConnectView(BaseModel):
    attached: bool

    created: bool

    cols: Optional[int] = None

    connect_url: Optional[str] = None

    idle_ttl_seconds: Optional[int] = None

    protocol_version: Optional[str] = None

    rows: Optional[int] = None

    session_name: Optional[str] = None

    status: Optional[str] = None
