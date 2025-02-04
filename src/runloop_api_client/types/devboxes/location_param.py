# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .range_param import RangeParam
from .document_uri import DocumentUri

__all__ = ["LocationParam"]


class LocationParamTyped(TypedDict, total=False):
    range: Required[RangeParam]
    """A range in a text document expressed as (zero-based) start and end positions.

    If you want to specify a range that contains a line including the line ending
    character(s) then use an end position denoting the start of the next line. For
    example:

    ```ts
    {
        start: { line: 5, character: 23 }
        end : { line 6, character : 0 }
    }
    ```

    The Range namespace provides helper functions to work with {@link Range}
    literals.
    """

    uri: Required[DocumentUri]
    """A tagging type for string properties that are actually document URIs."""


LocationParam: TypeAlias = Union[LocationParamTyped, Dict[str, object]]
