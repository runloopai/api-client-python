# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxReadFileContentsParams"]


class DevboxReadFileContentsParams(TypedDict, total=False):
    file_path: Required[str]
    """The path of the file to read."""
