# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["SqlColumnMetaView"]


class SqlColumnMetaView(BaseModel):
    name: str
    """Column name or alias."""

    type: str
    """Declared type (TEXT, INTEGER, REAL, BLOB, or empty)."""
