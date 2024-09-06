# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes

__all__ = ["DevboxUploadFileParams"]


class DevboxUploadFileParams(TypedDict, total=False):
    file: FileTypes

    path: str
