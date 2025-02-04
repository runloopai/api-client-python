# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from .integer import Integer
from ..._utils import PropertyInfo
from .range_param import RangeParam
from .diagnostic_tag import DiagnosticTag
from .l_sp_any_param import LSpAnyParam
from .diagnostic_severity import DiagnosticSeverity
from .code_description_param import CodeDescriptionParam
from .diagnostic_related_information_param import DiagnosticRelatedInformationParam

__all__ = ["DiagnosticParam"]


class DiagnosticParamTyped(TypedDict, total=False):
    message: Required[str]
    """The diagnostic's message. It usually appears in the user interface"""

    range: Required[RangeParam]
    """The range at which the message applies"""

    code: Union[Integer, str]
    """The diagnostic's code, which usually appear in the user interface."""

    code_description: Annotated[CodeDescriptionParam, PropertyInfo(alias="codeDescription")]
    """
    An optional property to describe the error code. Requires the code field (above)
    to be present/not null.
    """

    data: LSpAnyParam
    """
    A data entry field that is preserved between a `textDocument/publishDiagnostics`
    notification and `textDocument/codeAction` request.
    """

    related_information: Annotated[
        Iterable[DiagnosticRelatedInformationParam], PropertyInfo(alias="relatedInformation")
    ]
    """An array of related diagnostic information, e.g.

    when symbol-names within a scope collide all definitions can be marked via this
    property.
    """

    severity: DiagnosticSeverity
    """The diagnostic's severity.

    Can be omitted. If omitted it is up to the client to interpret diagnostics as
    error, warning, info or hint.
    """

    source: str
    """A human-readable string describing the source of this diagnostic, e.g.

    'typescript' or 'super lint'. It usually appears in the user interface.
    """

    tags: Iterable[DiagnosticTag]
    """Additional metadata about the diagnostic."""


DiagnosticParam: TypeAlias = Union[DiagnosticParamTyped, Dict[str, object]]
