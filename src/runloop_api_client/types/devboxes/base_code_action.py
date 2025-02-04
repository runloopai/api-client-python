# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .base_command import BaseCommand
from .base_workspace_edit import BaseWorkspaceEdit

__all__ = ["BaseCodeAction"]


class BaseCodeAction(BaseModel):
    title: str

    command: Optional[BaseCommand] = None

    edit: Optional[BaseWorkspaceEdit] = None

    is_preferred: Optional[bool] = FieldInfo(alias="isPreferred", default=None)

    kind: Optional[str] = None
