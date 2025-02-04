# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING

from .uinteger import Uinteger
from ..._models import BaseModel

__all__ = ["Position"]


class Position(BaseModel):
    character: Uinteger
    """Character offset on a line in a document (zero-based).

    The meaning of this offset is determined by the negotiated
    `PositionEncodingKind`.

    If the character value is greater than the line length it defaults back to the
    line length.
    """

    line: Uinteger
    """Line position in a document (zero-based).

    If a line number is greater than the number of lines in a document, it defaults
    back to the number of lines in the document. If a line number is negative, it
    defaults to 0.
    """

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
