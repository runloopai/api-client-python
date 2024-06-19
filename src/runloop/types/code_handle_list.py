# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .code_handle import CodeHandle

__all__ = ["CodeHandleList"]


class CodeHandleList(BaseModel):
    code_handles: Optional[List[CodeHandle]] = None
    """List of code handles matching given query."""
