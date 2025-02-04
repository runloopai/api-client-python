# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .base_command_param import BaseCommandParam
from .base_workspace_edit_param import BaseWorkspaceEditParam

__all__ = ["LspApplyCodeActionParams"]


class LspApplyCodeActionParams(TypedDict, total=False):
    title: Required[str]

    command: BaseCommandParam

    edit: BaseWorkspaceEditParam

    is_preferred: Annotated[bool, PropertyInfo(alias="isPreferred")]

    kind: str
