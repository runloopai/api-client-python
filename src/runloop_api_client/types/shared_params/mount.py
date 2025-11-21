# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .code_mount_parameters import CodeMountParameters
from .agent_mount_parameters import AgentMountParameters
from .object_mount_parameters import ObjectMountParameters

__all__ = ["Mount", "FileMountParameters"]


class FileMountParameters(TypedDict, total=False):
    files: Required[Dict[str, str]]
    """Map of file paths to file contents to be written before setup.

    Keys are absolute paths where files should be created, values are the file
    contents.
    """

    type: Required[Literal["file_mount"]]


Mount: TypeAlias = Union[ObjectMountParameters, AgentMountParameters, CodeMountParameters, FileMountParameters]
