# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .agent_mount import AgentMount
from .object_mount import ObjectMount

__all__ = ["Mount", "CodeMount", "FileMount"]


class CodeMount(TypedDict, total=False):
    repo_name: Required[str]
    """The name of the repo to mount.

    By default, code will be mounted at /home/user/{repo_name}s.
    """

    repo_owner: Required[str]
    """The owner of the repo."""

    type: Required[Literal["code_mount"]]

    token: Optional[str]
    """The authentication token necessary to pull repo."""

    install_command: Optional[str]
    """Installation command to install and setup repository."""


class FileMount(TypedDict, total=False):
    content: Required[str]
    """Content of the file to mount."""

    target: Required[str]
    """Target path where the file should be mounted."""

    type: Required[Literal["file_mount"]]


Mount: TypeAlias = Union[ObjectMount, AgentMount, CodeMount, FileMount]
