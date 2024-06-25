# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["InvocationSpanListView"]


class InvocationSpanListView(BaseModel):
    invocation_id: Optional[str] = FieldInfo(alias="invocationId", default=None)

    spans: Optional[object] = None
    """List of spans matching given query."""
