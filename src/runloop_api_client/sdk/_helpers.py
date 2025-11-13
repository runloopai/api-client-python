from __future__ import annotations

import io
import os
from typing import Dict, Union, Literal, Callable
from pathlib import Path

LogCallback = Callable[[str], None]

ContentType = Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"]
UploadData = Union[str, bytes, bytearray, Path, os.PathLike[str], io.IOBase]

_CONTENT_TYPE_MAP: Dict[str, ContentType] = {
    ".txt": "text",
    ".html": "text",
    ".css": "text",
    ".js": "text",
    ".json": "text",
    ".xml": "text",
    ".yaml": "text",
    ".yml": "text",
    ".md": "text",
    ".csv": "text",
    ".gz": "gzip",
    ".tar": "tar",
    ".tgz": "tgz",
    ".tar.gz": "tgz",
}


def detect_content_type(name: str) -> ContentType:
    lower = name.lower()
    if lower.endswith(".tar.gz") or lower.endswith(".tgz"):
        return "tgz"
    ext = Path(lower).suffix
    return _CONTENT_TYPE_MAP.get(ext, "unspecified")


def read_upload_data(data: UploadData) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, (Path, os.PathLike)):
        return Path(data).read_bytes()
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, io.TextIOBase):
        return data.read().encode("utf-8")
    if isinstance(data, io.BufferedIOBase) or isinstance(data, io.RawIOBase):
        return data.read()
    if hasattr(data, "read"):
        result = data.read()
        if isinstance(result, str):
            return result.encode("utf-8")
        return result
    raise TypeError("Unsupported upload data type. Provide str, bytes, path, or file-like object.")
