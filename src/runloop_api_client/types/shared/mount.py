# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = ["Mount", "ObjectMount", "AgentMount", "CodeMount", "FileMount"]


class ObjectMount(BaseModel):
    object_id: str
    """The ID of the object to write."""

    object_path: str
    """The path to write the object on the Devbox.

    Use absolute path of object (ie /home/user/object.txt, or directory if archive
    /home/user/archive_dir)
    """

    type: Literal["object_mount"]


class AgentMount(BaseModel):
    agent_id: Optional[str] = None
    """The ID of the agent to mount. Either agent_id or name must be set."""

    agent_name: Optional[str] = None
    """The name of the agent to mount.

    Returns the most recent agent with a matching name if no agent id string
    provided. Either agent id or name must be set
    """

    type: Literal["agent_mount"]

    agent_path: Optional[str] = None
    """Path to mount the agent on the Devbox.

    Required for git and object agents. Use absolute path (e.g., /home/user/agent)
    """

    auth_token: Optional[str] = None
    """Optional auth token for private repositories. Only used for git agents."""


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
