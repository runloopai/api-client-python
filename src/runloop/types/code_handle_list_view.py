# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .code_handle_view import CodeHandleView

__all__ = ["CodeHandleListView"]


class CodeHandleListView(BaseModel):
    code_handles: Optional[List[CodeHandleView]] = None
    """List of code handles matching given query."""
