# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CodeMountParametersParam"]


class CodeMountParametersParam(TypedDict, total=False):
    token: str
    """The authentication token necessary to pull repo."""

    install_command: str
    """Installation command to install and setup repository."""

    repo_name: str
    """The name of the repo to mount.

    By default, code will be mounted at /home/user/{repo_name}s.
    """

    repo_owner: str
    """The owner of the repo."""
