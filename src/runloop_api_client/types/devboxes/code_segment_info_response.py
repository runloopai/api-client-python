# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field as FieldInfo

from .range import Range
from .file_uri import FileUri
from ..._models import BaseModel
from .base_range import BaseRange
from .symbol_tag import SymbolTag
from .symbol_kind import SymbolKind
from .base_location import BaseLocation
from .base_diagnostic import BaseDiagnostic
from .base_code_action import BaseCodeAction
from .signature_help_response import SignatureHelpResponse

__all__ = ["CodeSegmentInfoResponse", "Symbol", "Hover"]


class Symbol(BaseModel):
    kind: SymbolKind
    """The kind of this symbol."""

    name: str
    """The name of this symbol.

    Will be displayed in the user interface and therefore must not be an empty
    string or a string only consisting of white spaces.
    """

    range: Range
    """
    The range enclosing this symbol not including leading/trailing whitespace but
    everything else like comments. This information is typically used to determine
    if the clients cursor is inside the symbol to reveal in the symbol in the UI.
    """

    selection_range: Range = FieldInfo(alias="selectionRange")
    """
    The range that should be selected and revealed when this symbol is being picked,
    e.g the name of a function. Must be contained by the `range`.
    """

    children: Optional[List[object]] = None
    """Children of this symbol, e.g. properties of a class."""

    deprecated: Optional[bool] = None
    """Indicates if this symbol is deprecated."""

    detail: Optional[str] = None
    """More detail for this symbol, e.g the signature of a function."""

    tags: Optional[List[SymbolTag]] = None
    """Tags for this document symbol."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class Hover(BaseModel):
    contents: object

    range: Optional[BaseRange] = None


class CodeSegmentInfoResponse(BaseModel):
    actions: List[BaseCodeAction]

    diagnostics: List[BaseDiagnostic]

    references: List[BaseLocation]

    symbol: Symbol
    """
    Represents programming constructs like variables, classes, interfaces etc. that
    appear in a document. Document symbols can be hierarchical and they have two
    ranges: one that encloses its definition and one that points to its most
    interesting range, e.g. the range of an identifier.
    """

    uri: FileUri

    hover: Optional[Hover] = None

    signature: Optional[SignatureHelpResponse] = None
