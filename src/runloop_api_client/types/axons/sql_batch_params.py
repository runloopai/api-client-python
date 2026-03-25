# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .sql_statement_params import SqlStatementParams

__all__ = ["SqlBatchParams"]


class SqlBatchParams(TypedDict, total=False):
    statements: Required[Iterable[SqlStatementParams]]
    """The SQL statements to execute atomically within a transaction."""
