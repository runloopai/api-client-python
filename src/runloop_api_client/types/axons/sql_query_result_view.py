# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .sql_column_meta_view import SqlColumnMetaView
from .sql_result_meta_view import SqlResultMetaView

__all__ = ["SqlQueryResultView"]


class SqlQueryResultView(BaseModel):
    columns: List[SqlColumnMetaView]
    """Column metadata."""

    meta: SqlResultMetaView
    """Execution metadata."""

    rows: List[object]
    """Result rows (empty for non-SELECT statements)."""
