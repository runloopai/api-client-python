# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DevboxWriteFileContentsParams"]


class DevboxWriteFileContentsParams(TypedDict, total=False):
    contents: Required[str]
    """The UTF-8 string contents to write to the file."""

    file_path: Required[str]
    """The path to write the file to on the Devbox.

    Path is relative to user home directory.
    """

    chmod: Optional[str]
    """File permissions in octal format (e.g., "644", "1755").

    Optional. If not specified, default system permissions will be used.
    """

    owner: Optional[str]
    """File owner username.

    Optional. If not specified, the file will be owned by the current user.
    """
