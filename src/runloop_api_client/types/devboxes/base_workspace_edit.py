# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from .record_string_text_edit_array import RecordStringTextEditArray

__all__ = ["BaseWorkspaceEdit"]


class BaseWorkspaceEdit(BaseModel):
    changes: Optional[RecordStringTextEditArray] = None
    """Construct a type with a set of properties K of type T"""
