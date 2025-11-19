"""Storage object resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import RequestOptions, LongRequestOptions, SDKObjectDownloadParams
from .._client import Runloop
from ..types.object_view import ObjectView
from ..types.object_download_url_view import ObjectDownloadURLView


class StorageObject:
    """Wrapper around storage object operations, including uploads and downloads."""

    def __init__(self, client: Runloop, object_id: str, upload_url: str | None) -> None:
        """Initialize the wrapper.

        Args:
            client: Generated Runloop client.
            object_id: Storage object identifier returned by the API.
            upload_url: Pre-signed upload URL, if the object is in draft state.
        """
        self._client = client
        self._id = object_id
        self._upload_url = upload_url

    @override
    def __repr__(self) -> str:
        return f"<StorageObject id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the storage object identifier.

        Returns:
            str: Unique object ID.
        """
        return self._id

    @property
    def upload_url(self) -> str | None:
        """Return the pre-signed upload URL, if available.

        Returns:
            str | None: Upload URL when the object is pending completion.
        """
        return self._upload_url

    def refresh(
        self,
        **options: Unpack[RequestOptions],
    ) -> ObjectView:
        """Fetch the latest metadata for the object.

        Args:
            **options: Optional request configuration.

        Returns:
            ObjectView: Updated object metadata.
        """
        return self._client.objects.retrieve(
            self._id,
            **options,
        )

    def complete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ObjectView:
        """Mark the object as fully uploaded.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            ObjectView: Finalized object metadata.
        """
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
        """Request a signed download URL for the object.

        Args:
            **params: Parameters controlling the download URL (e.g., expiry).

        Returns:
            ObjectDownloadURLView: URL + metadata describing the download.
        """
        return self._client.objects.download(
            self._id,
            **params,
        )

    def download_as_bytes(
        self,
        **params: Unpack[SDKObjectDownloadParams],
    ) -> bytes:
        """Download the object contents as bytes.

        Args:
            **params: Parameters forwarded to ``get_download_url``.

        Returns:
            bytes: Entire object payload.
        """
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
        """Download the object contents as UTF-8 text.

        Args:
            **params: Parameters forwarded to ``get_download_url``.

        Returns:
            str: Entire object payload decoded as UTF-8.
        """
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
        """Delete the storage object.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            ObjectView: API response for the deleted object.
        """
        return self._client.objects.delete(
            self._id,
            **options,
        )

    def upload_content(self, content: str | bytes) -> None:
        """Upload content to the object's pre-signed URL.

        Args:
            content: Bytes or text payload to upload.

        Raises:
            RuntimeError: If no upload URL is available.
            httpx.HTTPStatusError: Propagated from the underlying ``httpx`` client when the upload fails.
        """
        url = self._ensure_upload_url()
        response = self._client._client.put(url, content=content)
        response.raise_for_status()

    def _ensure_upload_url(self) -> str:
        """Return the upload URL, ensuring it is present.

        Returns:
            str: Upload URL ready for use.

        Raises:
            RuntimeError: If no upload URL is available.
        """
        if not self._upload_url:
            raise RuntimeError("No upload URL available. Create a new object before uploading content.")
        return self._upload_url
