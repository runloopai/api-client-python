from __future__ import annotations

from typing import Any, Dict, List, Optional
from pathlib import Path

import httpx

from .._client import AsyncRunloop
from .storage_object import UploadData, ContentType, _read_upload_data, _detect_content_type
from ..types.object_view import ObjectView
from ..types.object_download_url_view import ObjectDownloadURLView


class AsyncStorageObjectClient:
    """
    Async manager for :class:`AsyncStorageObject` instances.
    """

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(
        self,
        name: str,
        *,
        content_type: ContentType | None = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "AsyncStorageObject":
        content_type = content_type or _detect_content_type(name)
        obj = await self._client.objects.create(
            name=name,
            content_type=content_type,
            metadata=metadata,
        )
        return AsyncStorageObject(self._client, obj.id, upload_url=obj.upload_url)

    def from_id(self, object_id: str) -> "AsyncStorageObject":
        return AsyncStorageObject(self._client, object_id, upload_url=None)

    async def list(self, **params: Any) -> List["AsyncStorageObject"]:
        page = await self._client.objects.list(**params)
        return [AsyncStorageObject(self._client, item.id, upload_url=None) for item in getattr(page, "objects", [])]

    async def upload_from_file(
        self,
        path: str | Path,
        name: str | None = None,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> "AsyncStorageObject":
        file_path = Path(path)
        object_name = name or file_path.name
        obj = await self.create(object_name, content_type=content_type, metadata=metadata)
        await obj.upload_content(file_path)
        await obj.complete()
        return obj

    async def upload_from_text(
        self,
        text: str,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "AsyncStorageObject":
        obj = await self.create(name, content_type="text", metadata=metadata)
        await obj.upload_content(text)
        await obj.complete()
        return obj

    async def upload_from_bytes(
        self,
        data: bytes,
        name: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
        content_type: ContentType | None = None,
    ) -> "AsyncStorageObject":
        obj = await self.create(name, content_type=content_type or _detect_content_type(name), metadata=metadata)
        await obj.upload_content(data)
        await obj.complete()
        return obj


class AsyncStorageObject:
    """
    Async wrapper around storage object operations.
    """

    def __init__(self, client: AsyncRunloop, object_id: str, upload_url: str | None) -> None:
        self._client = client
        self._id = object_id
        self._upload_url = upload_url

    def __repr__(self) -> str:
        return f"<AsyncStorageObject id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    @property
    def upload_url(self) -> str | None:
        return self._upload_url

    async def refresh(self, **request_options: Any) -> ObjectView:
        return await self._client.objects.retrieve(self._id, **request_options)

    async def complete(self, **request_options: Any) -> ObjectView:
        result = await self._client.objects.complete(self._id, **request_options)
        self._upload_url = None
        return result

    async def get_download_url(
        self,
        *,
        duration_seconds: int | None = None,
        **request_options: Any,
    ) -> ObjectDownloadURLView:
        if duration_seconds is None:
            return await self._client.objects.download(self._id, **request_options)
        return await self._client.objects.download(self._id, duration_seconds=duration_seconds, **request_options)

    async def download_as_bytes(
        self,
        *,
        duration_seconds: int | None = None,
        **request_options: Any,
    ) -> bytes:
        url_view = await self.get_download_url(duration_seconds=duration_seconds, **request_options)
        async with httpx.AsyncClient() as client:
            response = await client.get(url_view.download_url)
        response.raise_for_status()
        return response.content

    async def download_as_text(
        self,
        *,
        duration_seconds: int | None = None,
        encoding: str = "utf-8",
        **request_options: Any,
    ) -> str:
        url_view = await self.get_download_url(duration_seconds=duration_seconds, **request_options)
        async with httpx.AsyncClient() as client:
            response = await client.get(url_view.download_url)
        response.raise_for_status()
        response.encoding = encoding
        return response.text

    async def delete(self, **request_options: Any) -> Any:
        return await self._client.objects.delete(self._id, **request_options)

    async def upload_content(self, data: UploadData) -> None:
        url = self._ensure_upload_url()
        payload = _read_upload_data(data)
        async with httpx.AsyncClient() as client:
            response = await client.put(url, content=payload)
        response.raise_for_status()

    def _ensure_upload_url(self) -> str:
        if not self._upload_url:
            raise RuntimeError("No upload URL available. Create a new object before uploading content.")
        return self._upload_url
