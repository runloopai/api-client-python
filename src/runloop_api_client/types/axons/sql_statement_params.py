# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["SqlStatementParams"]


class SqlStatementParams(TypedDict, total=False):
    sql: Required[str]
    """SQL query with ?-style positional placeholders."""

    params: Iterable[object]
    """Positional parameter bindings for ? placeholders."""
