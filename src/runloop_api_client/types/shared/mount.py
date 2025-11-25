# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .code_mount_parameters import CodeMountParameters
from .agent_mount_parameters import AgentMountParameters
from .object_mount_parameters import ObjectMountParameters

__all__ = ["Mount", "FileMountParameters"]


class FileMountParameters(BaseModel):
    content: str
    """Content of the file to mount."""

    target: str
    """Target path where the file should be mounted."""

    type: Literal["file_mount"]


Mount: TypeAlias = Annotated[
    Union[ObjectMountParameters, AgentMountParameters, CodeMountParameters, FileMountParameters],
    PropertyInfo(discriminator="type"),
]
