# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["CodeMountParameters"]


class CodeMountParameters(BaseModel):
    repo_name: str
    """The name of the repo to mount.

    By default, code will be mounted at /home/user/{repo_name}s.
    """

    repo_owner: str
    """The owner of the repo."""

    token: Optional[str] = None
    """The authentication token necessary to pull repo."""

    install_command: Optional[str] = None
    """Installation command to install and setup repository."""
