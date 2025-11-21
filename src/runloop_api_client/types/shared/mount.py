# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .code_mount_parameters import CodeMountParameters
from .agent_mount_parameters import AgentMountParameters
from .object_mount_parameters import ObjectMountParameters

__all__ = ["Mount", "FileMountParameters"]


class FileMountParameters(BaseModel):
    files: Dict[str, str]
    """Map of file paths to file contents to be written before setup.

    Keys are absolute paths where files should be created, values are the file
    contents.
    """

    type: Literal["file_mount"]


Mount: TypeAlias = Annotated[
    Union[ObjectMountParameters, AgentMountParameters, CodeMountParameters, FileMountParameters],
    PropertyInfo(discriminator="type"),
]
