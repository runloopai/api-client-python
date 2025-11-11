from __future__ import annotations

from typing import Any

import httpx

from typing_extensions import override

from .._client import AsyncRunloop
from .._types import Body, Headers, NotGiven, Query, Timeout, not_given
from ._helpers import UploadData, read_upload_data
from ..types.object_view import ObjectView
from ..types.object_download_url_view import ObjectDownloadURLView


class AsyncStorageObject:
    """
    Async wrapper around storage object operations.
    """

    def __init__(self, client: AsyncRunloop, object_id: str, upload_url: str | None) -> None:
        self._client = client
        self._id = object_id
        self._upload_url = upload_url

    @override
    def __repr__(self) -> str:
        return f"<AsyncStorageObject id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    @property
    def upload_url(self) -> str | None:
        return self._upload_url

    async def refresh(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> ObjectView:
        return await self._client.objects.retrieve(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def complete(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ObjectView:
        result = await self._client.objects.complete(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        self._upload_url = None
        return result

    async def get_download_url(
        self,
        *,
        duration_seconds: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> ObjectDownloadURLView:
        if duration_seconds is None:
            return await self._client.objects.download(
                self._id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        return await self._client.objects.download(
            self._id,
            duration_seconds=duration_seconds,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def download_as_bytes(
        self,
        *,
        duration_seconds: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> bytes:
        url_view = await self.get_download_url(
            duration_seconds=duration_seconds,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url_view.download_url)
        response.raise_for_status()
        return response.content

    async def download_as_text(
        self,
        *,
        duration_seconds: int | None = None,
        encoding: str = "utf-8",
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> str:
        url_view = await self.get_download_url(
            duration_seconds=duration_seconds,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url_view.download_url)
        response.raise_for_status()
        response.encoding = encoding
        return response.text

    async def delete(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self._client.objects.delete(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def upload_content(self, data: UploadData) -> None:
        url = self._ensure_upload_url()
        payload = read_upload_data(data)
        async with httpx.AsyncClient() as client:
            response = await client.put(url, content=payload)
        response.raise_for_status()

    def _ensure_upload_url(self) -> str:
        if not self._upload_url:
            raise RuntimeError("No upload URL available. Create a new object before uploading content.")
        return self._upload_url
