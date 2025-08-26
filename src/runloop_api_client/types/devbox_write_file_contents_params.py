# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxWriteFileContentsParams"]


class DevboxWriteFileContentsParams(TypedDict, total=False):
    contents: Required[str]
    """The UTF-8 string contents to write to the file."""

    file_path: Required[str]
    """The path to write the file to on the Devbox.

    Path is relative to user home directory.
    """
