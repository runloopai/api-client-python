# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .watched_file_response import WatchedFileResponse

__all__ = ["LspFilesResponse"]

LspFilesResponse: TypeAlias = List[WatchedFileResponse]
