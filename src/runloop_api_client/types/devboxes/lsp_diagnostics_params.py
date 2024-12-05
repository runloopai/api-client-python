# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .file_uri import FileUri

__all__ = ["LspDiagnosticsParams"]


class LspDiagnosticsParams(TypedDict, total=False):
    uri: Required[FileUri]
