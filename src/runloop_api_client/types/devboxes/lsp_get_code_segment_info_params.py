# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .file_uri import FileUri
from .symbol_type import SymbolType

__all__ = ["LspGetCodeSegmentInfoParams"]


class LspGetCodeSegmentInfoParams(TypedDict, total=False):
    symbol_name: Required[Annotated[str, PropertyInfo(alias="symbolName")]]

    uri: Required[FileUri]

    symbol_type: Annotated[SymbolType, PropertyInfo(alias="symbolType")]
