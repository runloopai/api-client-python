"""Storage object resource class for asynchronous operations."""

from __future__ import annotations

from typing import Iterable
from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions, SDKObjectDownloadParams
from .._client import AsyncRunloop
from ..types.object_view import ObjectView
from ..types.blueprint_create_params import BuildContext
from ..types.object_download_url_view import ObjectDownloadURLView


class AsyncStorageObject:
    """Async wrapper around storage object operations, including uploads and downloads."""

    def __init__(self, client: AsyncRunloop, object_id: str, upload_url: str | None) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param object_id: Storage object identifier returned by the API
        :type object_id: str
        :param upload_url: Optional pre-signed upload URL if the object is still open, defaults to None
        :type upload_url: str | None, optional
        """
        self._client = client
        self._id = object_id
        self._upload_url = upload_url

    @override
    def __repr__(self) -> str:
        return f"<AsyncStorageObject id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the storage object identifier.

        :return: Unique object ID
        :rtype: str
        """
        return self._id

    @property
    def upload_url(self) -> str | None:
        """Return the pre-signed upload URL, if available.

        :return: Upload URL when the object is pending completion
        :rtype: str | None
        """
        return self._upload_url

    async def refresh(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> ObjectView:
        """Fetch the latest metadata for the object.

        :param options: Optional request configuration
        :return: Updated object metadata
        :rtype: ObjectView
        """
        return await self._client.objects.retrieve(
            self._id,
            **options,
        )

    async def complete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ObjectView:
        """Mark the object as fully uploaded.

        :param options: Optional long-running request configuration
        :return: Finalized object metadata
        :rtype: ObjectView
        """
        result = await self._client.objects.complete(
            self._id,
            **options,
        )
        self._upload_url = None
        return result

    async def get_download_url(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> ObjectDownloadURLView:
        """Request a signed download URL for the object.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectDownloadParams` for available parameters
        :return: URL + metadata describing the download
        :rtype: ObjectDownloadURLView
        """
        return await self._client.objects.download(
            self._id,
            **params,
        )

    async def download_as_bytes(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> bytes:
        """Download the object contents as bytes.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectDownloadParams` for available parameters
        :return: Entire object payload
        :rtype: bytes
        """
        url_view = await self.get_download_url(
            **params,
        )
        response = await self._client._client.get(url_view.download_url)
        response.raise_for_status()
        return response.content

    async def download_as_text(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> str:
        """Download the object contents as UTF-8 text.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKObjectDownloadParams` for available parameters
        :return: Entire object payload decoded as UTF-8
        :rtype: str
        """
        url_view = await self.get_download_url(
            **params,
        )
        response = await self._client._client.get(url_view.download_url)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ObjectView:
        """Delete the storage object.

        :param options: Optional long-running request configuration
        :return: API response for the deleted object
        :rtype: ObjectView
        """
        return await self._client.objects.delete(
            self._id,
            **options,
        )

    async def upload_content(self, content: str | bytes | Iterable[bytes]) -> None:
        """Upload content to the object's pre-signed URL.

        :param content: Bytes payload, text payload, or an iterable streaming bytes
        :type content: str | bytes | Iterable[bytes]
        :return: None
        :rtype: None
        :raises RuntimeError: If no upload URL is available
        :raises httpx.HTTPStatusError: Propagated from the underlying ``httpx`` client when the upload fails
        """
        url = self._ensure_upload_url()
        response = await self._client._client.put(url, content=content)
        response.raise_for_status()

    def as_build_context(self) -> BuildContext:
        """Return this object in the shape expected for a Blueprint build context.

        The returned mapping can be passed directly to ``build_context``
        when creating a blueprint.

        :return: Mapping suitable for use as a blueprint build context
        :rtype: BuildContext
        """
        return {
            "object_id": self._id,
            "type": "object",
        }

    def _ensure_upload_url(self) -> str:
        """Return the upload URL, ensuring it exists.

        :return: Upload URL ready for use
        :rtype: str
        :raises RuntimeError: If no upload URL is available
        """
        if not self._upload_url:
            raise RuntimeError("No upload URL available. Create a new object before uploading content.")
        return self._upload_url
