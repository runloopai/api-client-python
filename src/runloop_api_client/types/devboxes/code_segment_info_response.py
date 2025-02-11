# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

from .file_uri import FileUri
from ..._compat import PYDANTIC_V2
from ..._models import BaseModel
from .base_range import BaseRange
from .base_location import BaseLocation
from .base_diagnostic import BaseDiagnostic
from .base_code_action import BaseCodeAction
from .signature_help_response import SignatureHelpResponse

__all__ = ["CodeSegmentInfoResponse", "Hover"]


class Hover(BaseModel):
    contents: object

    range: Optional[BaseRange] = None


class CodeSegmentInfoResponse(BaseModel):
    actions: List[BaseCodeAction]

    diagnostics: List[BaseDiagnostic]

    references: List[BaseLocation]

    symbol: "DocumentSymbol"
    """
    Represents programming constructs like variables, classes, interfaces etc. that
    appear in a document. Document symbols can be hierarchical and they have two
    ranges: one that encloses its definition and one that points to its most
    interesting range, e.g. the range of an identifier.
    """

    uri: FileUri

    hover: Optional[Hover] = None

    signature: Optional[SignatureHelpResponse] = None


from .document_symbol import DocumentSymbol

if PYDANTIC_V2:
    CodeSegmentInfoResponse.model_rebuild()
    Hover.model_rebuild()
else:
    CodeSegmentInfoResponse.update_forward_refs()  # type: ignore
    Hover.update_forward_refs()  # type: ignore
