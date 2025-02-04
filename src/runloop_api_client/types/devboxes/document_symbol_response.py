# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .base_range import BaseRange
from .symbol_kind import SymbolKind

__all__ = ["DocumentSymbolResponse", "DocumentSymbolResponseItem"]


class DocumentSymbolResponseItem(BaseModel):
    kind: SymbolKind
    """A symbol kind."""

    name: str

    range: BaseRange

    selection_range: BaseRange = FieldInfo(alias="selectionRange")


DocumentSymbolResponse: TypeAlias = List[DocumentSymbolResponseItem]
