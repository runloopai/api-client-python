from __future__ import annotations

import io
import os
from typing import Any, Dict, List, Union, Literal, Optional
from pathlib import Path

import httpx

from .._client import Runloop
from ..types.object_view import ObjectView
from ..types.object_download_url_view import ObjectDownloadURLView

ContentType = Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"]
UploadData = Union[str, bytes, bytearray, Path, os.PathLike[str], io.IOBase]


class StorageObjectClient:
    """
    Manage :class:`StorageObject` instances and provide convenience upload helpers.
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def create(
        self,
        name: str,
        *,
        content_type: ContentType | None = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "StorageObject":
        content_type = content_type or _detect_content_type(name)
        obj = self._client.objects.create(
            name=name,
            content_type=content_type,
            metadata=metadata,
        )
        return StorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> "StorageObject":
        return StorageObject(self._client, object_id, upload_url=None)

    def list(self, **params: Any) -> List["StorageObject"]:
        page = self._client.objects.list(**params)
        return [StorageObject(self._client, item.id, upload_url=None) for item in getattr(page, "objects", [])]

    def upload_from_file(
        self,
        path: str | Path,
        name: str | None = None,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> "StorageObject":
        file_path = Path(path)
        object_name = name or file_path.name
        obj = self.create(object_name, content_type=content_type, metadata=metadata)
        obj.upload_content(file_path)
        obj.complete()
        return obj

    def upload_from_text(
        self,
        text: str,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "StorageObject":
        obj = self.create(name, content_type="text", metadata=metadata)
        obj.upload_content(text)
        obj.complete()
        return obj

    def upload_from_bytes(
        self,
        data: bytes,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> "StorageObject":
        obj = self.create(name, content_type=content_type or _detect_content_type(name), metadata=metadata)
        obj.upload_content(data)
        obj.complete()
        return obj


class StorageObject:
    """
    Wrapper around storage object operations, including uploads and downloads.
    """

    def __init__(self, client: Runloop, object_id: str, upload_url: str | None) -> None:
        self._client = client
        self._id = object_id
        self._upload_url = upload_url

    def __repr__(self) -> str:
        return f"<StorageObject id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    @property
    def upload_url(self) -> str | None:
        return self._upload_url

    def refresh(self, **request_options: Any) -> ObjectView:
        return self._client.objects.retrieve(self._id, **request_options)

    def complete(self, **request_options: Any) -> ObjectView:
        result = self._client.objects.complete(self._id, **request_options)
        self._upload_url = None
        return result

    def get_download_url(self, *, duration_seconds: int | None = None, **request_options: Any) -> ObjectDownloadURLView:
        if duration_seconds is None:
            return self._client.objects.download(self._id, **request_options)
        return self._client.objects.download(self._id, duration_seconds=duration_seconds, **request_options)

    def download_as_bytes(self, *, duration_seconds: int | None = None, **request_options: Any) -> bytes:
        url_view = self.get_download_url(duration_seconds=duration_seconds, **request_options)
        response = httpx.get(url_view.download_url)
        response.raise_for_status()
        return response.content

    def download_as_text(
        self,
        *,
        duration_seconds: int | None = None,
        encoding: str = "utf-8",
        **request_options: Any,
    ) -> str:
        url_view = self.get_download_url(duration_seconds=duration_seconds, **request_options)
        response = httpx.get(url_view.download_url)
        response.raise_for_status()
        response.encoding = encoding
        return response.text

    def delete(self, **request_options: Any) -> Any:
        return self._client.objects.delete(self._id, **request_options)

    def upload_content(self, data: UploadData) -> None:
        url = self._ensure_upload_url()
        payload = _read_upload_data(data)
        response = httpx.put(url, content=payload)
        response.raise_for_status()

    def _ensure_upload_url(self) -> str:
        if not self._upload_url:
            raise RuntimeError("No upload URL available. Create a new object before uploading content.")
        return self._upload_url


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


def _detect_content_type(name: str) -> ContentType:
    lower = name.lower()
    if lower.endswith(".tar.gz") or lower.endswith(".tgz"):
        return "tgz"
    ext = Path(lower).suffix
    return _CONTENT_TYPE_MAP.get(ext, "unspecified")


def _read_upload_data(data: UploadData) -> bytes:
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
    if isinstance(data, io.IOBase) and hasattr(data, "read"):
        result = data.read()
        if isinstance(result, str):
            return result.encode("utf-8")
        return result
    raise TypeError("Unsupported upload data type. Provide str, bytes, path, or file-like object.")
