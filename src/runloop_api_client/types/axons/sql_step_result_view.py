# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from .sql_step_error_view import SqlStepErrorView
from .sql_query_result_view import SqlQueryResultView

__all__ = ["SqlStepResultView"]


class SqlStepResultView(BaseModel):
    error: Optional[SqlStepErrorView] = None
    """Error on failure."""

    success: Optional[SqlQueryResultView] = None
    """Result on success."""
