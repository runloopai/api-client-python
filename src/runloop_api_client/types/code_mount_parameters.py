# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["CodeMountParameters"]


class CodeMountParameters(BaseModel):
    token: Optional[str] = None
    """The authentication token necessary to pull repo."""

    install_command: Optional[str] = None
    """Installation command to install and setup repository."""

    repo_name: Optional[str] = None
    """The name of the repo to mount.

    By default, code will be mounted at /home/user/{repo_name}s.
    """

    repo_owner: Optional[str] = None
    """The owner of the repo."""
