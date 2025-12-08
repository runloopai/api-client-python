# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["Mount", "ObjectMount", "AgentMount", "CodeMount", "FileMount"]


class ObjectMount(TypedDict, total=False):
    object_id: Required[str]
    """The ID of the object to write."""

    object_path: Required[str]
    """The path to write the object on the Devbox.

    Use absolute path of object (ie /home/user/object.txt, or directory if archive
    /home/user/archive_dir)
    """

    type: Required[Literal["object_mount"]]


class AgentMount(TypedDict, total=False):
    agent_id: Required[Optional[str]]
    """The ID of the agent to mount. Either agent_id or name must be set."""

    agent_name: Required[Optional[str]]
    """The name of the agent to mount.

    Returns the most recent agent with a matching name if no agent id string
    provided. Either agent id or name must be set
    """

    type: Required[Literal["agent_mount"]]

    agent_path: Optional[str]
    """Path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """

    auth_token: Optional[str]
    """Optional auth token for private repositories. Only used for git agents."""


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
