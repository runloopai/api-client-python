# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .file_path import FilePath

__all__ = ["FileContentsResponse"]


class FileContentsResponse(BaseModel):
    contents: str

    full_path: str = FieldInfo(alias="fullPath")

    path: FilePath
