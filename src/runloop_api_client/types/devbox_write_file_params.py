# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxWriteFileParams"]


class DevboxWriteFileParams(TypedDict, total=False):
    contents: Required[str]
    """The contents to write to file."""

    file_path: Required[str]
    """The path of the file to read."""
