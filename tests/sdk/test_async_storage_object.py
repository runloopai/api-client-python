"""Comprehensive tests for async StorageObject class."""

from __future__ import annotations

import tempfile
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

import pytest

from tests.sdk.conftest import create_mock_httpx_client, create_mock_httpx_response
from runloop_api_client.sdk import AsyncStorageObject


class TestAsyncStorageObject:
    """Tests for AsyncStorageObject class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncStorageObject initialization."""
        obj = AsyncStorageObject(mock_async_client, "obj_123", "https://upload.example.com")
        assert obj.id == "obj_123"
        assert obj.upload_url == "https://upload.example.com"

    def test_init_no_upload_url(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncStorageObject initialization without upload URL."""
        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        assert obj.id == "obj_123"
        assert obj.upload_url is None

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncStorageObject string representation."""
        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        assert repr(obj) == "<AsyncStorageObject id='obj_123'>"

    @pytest.mark.asyncio
    async def test_refresh(self, mock_async_client: AsyncMock, object_view: SimpleNamespace) -> None:
        """Test refresh method."""
        mock_async_client.objects.retrieve = AsyncMock(return_value=object_view)

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.refresh(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == object_view
        mock_async_client.objects.retrieve.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete(self, mock_async_client: AsyncMock) -> None:
        """Test complete method updates upload_url to None."""
        completed_view = SimpleNamespace(id="obj_123", upload_url=None)
        mock_async_client.objects.complete = AsyncMock(return_value=completed_view)

        obj = AsyncStorageObject(mock_async_client, "obj_123", "https://upload.example.com")
        assert obj.upload_url == "https://upload.example.com"

        result = await obj.complete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == completed_view
        assert obj.upload_url is None
        mock_async_client.objects.complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_download_url_without_duration(self, mock_async_client: AsyncMock) -> None:
        """Test get_download_url without duration_seconds."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_async_client.objects.download = AsyncMock(return_value=download_url_view)

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.get_download_url(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == download_url_view
        mock_async_client.objects.download.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_download_url_with_duration(self, mock_async_client: AsyncMock) -> None:
        """Test get_download_url with duration_seconds."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_async_client.objects.download = AsyncMock(return_value=download_url_view)

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.get_download_url(
            duration_seconds=3600,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == download_url_view
        mock_async_client.objects.download.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_download_as_bytes(self, mock_client_class: Mock, mock_async_client: AsyncMock) -> None:
        """Test download_as_bytes method."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_async_client.objects.download = AsyncMock(return_value=download_url_view)

        mock_response = create_mock_httpx_response(content=b"file content")
        mock_http_client = create_mock_httpx_client(methods={"get": mock_response})
        mock_client_class.return_value = mock_http_client

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.download_as_bytes(
            duration_seconds=3600,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == b"file content"
        # Verify get was called
        mock_http_client.get.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_download_as_text_default_encoding(
        self, mock_client_class: Mock, mock_async_client: AsyncMock
    ) -> None:
        """Test download_as_text with default encoding."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_async_client.objects.download = AsyncMock(return_value=download_url_view)

        mock_response = create_mock_httpx_response(text="file content", encoding="utf-8")
        mock_http_client = create_mock_httpx_client(methods={"get": mock_response})
        mock_client_class.return_value = mock_http_client

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.download_as_text()

        assert result == "file content"
        assert mock_response.encoding == "utf-8"
        # Verify get was called
        mock_http_client.get.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_download_as_text_custom_encoding(
        self, mock_client_class: Mock, mock_async_client: AsyncMock
    ) -> None:
        """Test download_as_text with custom encoding."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_async_client.objects.download = AsyncMock(return_value=download_url_view)

        mock_response = create_mock_httpx_response(text="file content", encoding="utf-8")
        mock_http_client = create_mock_httpx_client(methods={"get": mock_response})
        mock_client_class.return_value = mock_http_client

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.download_as_text(encoding="latin-1")

        assert result == "file content"
        assert mock_response.encoding == "latin-1"
        mock_http_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete(self, mock_async_client: AsyncMock, object_view: SimpleNamespace) -> None:
        """Test delete method."""
        mock_async_client.objects.delete = AsyncMock(return_value=object_view)

        obj = AsyncStorageObject(mock_async_client, "obj_123", None)
        result = await obj.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == object_view
        mock_async_client.objects.delete.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_upload_content_string(self, mock_client_class: Mock, mock_async_client: AsyncMock) -> None:
        """Test upload_content with string."""
        mock_response = create_mock_httpx_response()
        mock_http_client = create_mock_httpx_client(methods={"put": mock_response})
        mock_client_class.return_value = mock_http_client

        obj = AsyncStorageObject(mock_async_client, "obj_123", "https://upload.example.com")
        await obj.upload_content("test content")

        # Verify put was called with correct URL
        mock_http_client.put.assert_called_once()
        call_args = mock_http_client.put.call_args
        assert call_args[0][0] == "https://upload.example.com"
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_upload_content_bytes(self, mock_client_class: Mock, mock_async_client: AsyncMock) -> None:
        """Test upload_content with bytes."""
        mock_response = create_mock_httpx_response()
        mock_http_client = create_mock_httpx_client(methods={"put": mock_response})
        mock_client_class.return_value = mock_http_client

        obj = AsyncStorageObject(mock_async_client, "obj_123", "https://upload.example.com")
        await obj.upload_content(b"test content")

        # Verify put was called with correct URL
        mock_http_client.put.assert_called_once()
        call_args = mock_http_client.put.call_args
        assert call_args[0][0] == "https://upload.example.com"
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_upload_content_path(self, mock_client_class: Mock, mock_async_client: AsyncMock) -> None:
        """Test upload_content with Path."""
        mock_response = create_mock_httpx_response()
        mock_http_client = create_mock_httpx_client(methods={"put": mock_response})
        mock_client_class.return_value = mock_http_client

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            temp_path = Path(f.name)

        try:
            obj = AsyncStorageObject(mock_async_client, "obj_123", "https://upload.example.com")
            await obj.upload_content(temp_path)

            # Verify put was called
            mock_http_client.put.assert_called_once()
            call_args = mock_http_client.put.call_args
            assert call_args[0][0] == "https://upload.example.com"
            assert call_args[1]["content"] == b"test content"
            mock_response.raise_for_status.assert_called_once()
        finally:
            temp_path.unlink()

    @pytest.mark.asyncio
    async def test_upload_content_no_url(self, mock_async_client: AsyncMock) -> None:
        """Test upload_content raises error when no upload URL."""
        obj = AsyncStorageObject(mock_async_client, "obj_123", None)

        with pytest.raises(RuntimeError, match="No upload URL available"):
            await obj.upload_content("test content")

    def test_ensure_upload_url_with_url(self, mock_async_client: AsyncMock) -> None:
        """Test _ensure_upload_url returns URL when available."""
        obj = AsyncStorageObject(mock_async_client, "obj_123", "https://upload.example.com")
        url = obj._ensure_upload_url()
        assert url == "https://upload.example.com"

    def test_ensure_upload_url_no_url(self, mock_async_client: AsyncMock) -> None:
        """Test _ensure_upload_url raises error when no URL."""
        obj = AsyncStorageObject(mock_async_client, "obj_123", None)

        with pytest.raises(RuntimeError, match="No upload URL available"):
            obj._ensure_upload_url()
