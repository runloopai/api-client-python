# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DevboxWriteFileParams"]


class DevboxWriteFileParams(TypedDict, total=False):
    contents: str
    """The contents to write to file."""

    file_path: str
    """The path of the file to read."""
