# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CodeActionApplicationResult"]


class CodeActionApplicationResult(BaseModel):
    success: bool

    error: Optional[str] = None

    files_changed: Optional[List[str]] = FieldInfo(alias="filesChanged", default=None)
