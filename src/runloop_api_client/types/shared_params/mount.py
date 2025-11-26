# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .code_mount_parameters import CodeMountParameters
from .agent_mount_parameters import AgentMountParameters
from .object_mount_parameters import ObjectMountParameters

__all__ = ["Mount", "FileMountParameters"]


class FileMountParameters(TypedDict, total=False):
    content: Required[str]
    """Content of the file to mount."""

    target: Required[str]
    """Target path where the file should be mounted."""

    type: Required[Literal["file_mount"]]


Mount: TypeAlias = Union[ObjectMountParameters, AgentMountParameters, CodeMountParameters, FileMountParameters]
