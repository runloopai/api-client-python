# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from .range_param import RangeParam

__all__ = ["TextEditParam"]


class TextEditParamTyped(TypedDict, total=False):
    new_text: Required[Annotated[str, PropertyInfo(alias="newText")]]
    """The string to be inserted. For delete operations use an empty string."""

    range: Required[RangeParam]
    """The range of the text document to be manipulated.

    To insert text into a document create a range where start === end.
    """


TextEditParam: TypeAlias = Union[TextEditParamTyped, Dict[str, object]]
