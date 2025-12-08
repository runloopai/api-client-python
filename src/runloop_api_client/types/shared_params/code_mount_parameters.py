# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["CodeMountParameters"]


class CodeMountParameters(TypedDict, total=False):
    repo_name: Required[str]
    """The name of the repo to mount.

    By default, code will be mounted at /home/user/{repo_name}s.
    """

    repo_owner: Required[str]
    """The owner of the repo."""

    token: Optional[str]
    """The authentication token necessary to pull repo."""

    install_command: Optional[str]
    """Installation command to install and setup repository."""
