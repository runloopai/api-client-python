# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .agent_mount import AgentMount
from .object_mount import ObjectMount

__all__ = ["Mount", "CodeMount", "FileMount"]


class CodeMount(BaseModel):
    repo_name: str
    """The name of the repo to mount.

    By default, code will be mounted at /home/user/{repo_name}s.
    """

    repo_owner: str
    """The owner of the repo."""

    type: Literal["code_mount"]

    token: Optional[str] = None
    """The authentication token necessary to pull repo."""

    install_command: Optional[str] = None
    """Installation command to install and setup repository."""


class FileMount(BaseModel):
    content: str
    """Content of the file to mount."""

    target: str
    """Target path where the file should be mounted."""

    type: Literal["file_mount"]


Mount: TypeAlias = Annotated[Union[ObjectMount, AgentMount, CodeMount, FileMount], PropertyInfo(discriminator="type")]
