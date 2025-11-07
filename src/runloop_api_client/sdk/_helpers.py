from __future__ import annotations

import io
import os
from typing import Union
from pathlib import Path

from .._types import FileTypes
from .._utils import file_from_path

UploadInput = Union[FileTypes, str, os.PathLike[str], Path, bytes, bytearray, io.IOBase]


def normalize_upload_input(file: UploadInput) -> FileTypes:
    """
    Normalize a variety of Python file representations into the generated client's FileTypes.
    """
    if isinstance(file, tuple):
        return file
    if isinstance(file, bytes):
        return file
    if isinstance(file, bytearray):
        return bytes(file)
    if isinstance(file, (str, Path, os.PathLike)):
        return file_from_path(file)
    if isinstance(file, io.TextIOBase):
        return file.read().encode("utf-8")
    if isinstance(file, io.BufferedIOBase) or isinstance(file, io.RawIOBase):
        return file
    if isinstance(file, io.IOBase) and hasattr(file, "read"):
        data = file.read()
        if isinstance(data, str):
            return data.encode("utf-8")
        return data
    raise TypeError("Unsupported file type for upload. Provide path, bytes, or file-like object.")
