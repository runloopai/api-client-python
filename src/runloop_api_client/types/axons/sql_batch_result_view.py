# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .sql_step_result_view import SqlStepResultView

__all__ = ["SqlBatchResultView"]


class SqlBatchResultView(BaseModel):
    results: List[SqlStepResultView]
    """One result per statement, in order."""
