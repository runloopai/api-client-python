# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["WatchedFileResponse"]


class WatchedFileResponse(BaseModel):
    filename: str

    full_path: str = FieldInfo(alias="fullPath")

    path: str
