# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["PtyControlResultView"]


class PtyControlResultView(BaseModel):
    session_name: Optional[str] = None

    status: Optional[str] = None
