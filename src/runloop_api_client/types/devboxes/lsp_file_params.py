# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .file_path import FilePath

__all__ = ["LspFileParams"]


class LspFileParams(TypedDict, total=False):
    path: Required[FilePath]
