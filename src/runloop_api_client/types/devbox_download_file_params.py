# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxDownloadFileParams"]


class DevboxDownloadFileParams(TypedDict, total=False):
    path: Required[str]
    """The path on the Devbox filesystem to read the file from.

    Path is relative to user home directory.
    """
