# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["DevboxUploadFileParams"]


class DevboxUploadFileParams(TypedDict, total=False):
    path: Required[str]
    """The path to write the file to on the Devbox.

    Path is relative to user home directory.
    """

    file: FileTypes
