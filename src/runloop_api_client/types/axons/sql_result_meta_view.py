# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["SqlResultMetaView"]


class SqlResultMetaView(BaseModel):
    changes: int
    """Rows modified by INSERT/UPDATE/DELETE."""

    duration_ms: float
    """Execution time in milliseconds."""

    rows_read_limit_reached: bool
    """True when result was truncated at the row limit."""
