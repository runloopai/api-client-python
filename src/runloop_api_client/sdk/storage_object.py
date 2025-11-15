"""Storage object resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import RequestOptions, LongRequestOptions, SDKObjectDownloadParams
from .._client import Runloop
from ..types.object_view import ObjectView
from ..types.object_download_url_view import ObjectDownloadURLView


class StorageObject:
    """
    Wrapper around storage object operations, including uploads and downloads.
    """

    def __init__(self, client: Runloop, object_id: str, upload_url: str | None) -> None:
        self._client = client
        self._id = object_id
        self._upload_url = upload_url

    @override
    def __repr__(self) -> str:
        return f"<StorageObject id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    @property
    def upload_url(self) -> str | None:
        return self._upload_url

    def refresh(
        self,
        **options: Unpack[RequestOptions],
    ) -> ObjectView:
        return self._client.objects.retrieve(
            self._id,
            **options,
        )

    def complete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ObjectView:
        result = self._client.objects.complete(
            self._id,
            **options,
        )
        self._upload_url = None
        return result

    def get_download_url(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> ObjectDownloadURLView:
        return self._client.objects.download(
            self._id,
            **params,
        )

    def download_as_bytes(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> bytes:
        url_view = self.get_download_url(
            **params,
        )
        response = self._client._client.get(url_view.download_url)
        response.raise_for_status()
        return response.content

    def download_as_text(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> str:
        url_view = self.get_download_url(
            **params,
        )
        response = self._client._client.get(url_view.download_url)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text

    def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ObjectView:
        return self._client.objects.delete(
            self._id,
            **options,
        )

    def upload_content(self, content: str | bytes) -> None:
        url = self._ensure_upload_url()
        response = self._client._client.put(url, content=content)
        response.raise_for_status()

    def _ensure_upload_url(self) -> str:
        if not self._upload_url:
            raise RuntimeError("No upload URL available. Create a new object before uploading content.")
        return self._upload_url
