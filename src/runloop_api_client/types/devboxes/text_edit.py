# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING

from pydantic import Field as FieldInfo

from .range import Range
from ..._models import BaseModel

__all__ = ["TextEdit"]


class TextEdit(BaseModel):
    new_text: str = FieldInfo(alias="newText")
    """The string to be inserted. For delete operations use an empty string."""

    range: Range
    """The range of the text document to be manipulated.

    To insert text into a document create a range where start === end.
    """

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
