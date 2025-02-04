# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from .code_action_kind import CodeActionKind
from .diagnostic_param import DiagnosticParam
from .code_action_trigger_kind import CodeActionTriggerKind

__all__ = ["CodeActionContextParam"]


class CodeActionContextParamTyped(TypedDict, total=False):
    diagnostics: Required[Iterable[DiagnosticParam]]
    """
    An array of diagnostics known on the client side overlapping the range provided
    to the `textDocument/codeAction` request. They are provided so that the server
    knows which errors are currently presented to the user for the given range.
    There is no guarantee that these accurately reflect the error state of the
    resource. The primary parameter to compute code actions is the provided range.
    """

    only: List[CodeActionKind]
    """Requested kind of actions to return.

    Actions not of this kind are filtered out by the client before being shown. So
    servers can omit computing them.
    """

    trigger_kind: Annotated[CodeActionTriggerKind, PropertyInfo(alias="triggerKind")]
    """The reason why code actions were requested."""


CodeActionContextParam: TypeAlias = Union[CodeActionContextParamTyped, Dict[str, object]]
