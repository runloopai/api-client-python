"""Comprehensive tests for sync StorageObject class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from tests.sdk.conftest import MockObjectView, create_mock_httpx_response
from runloop_api_client.sdk import StorageObject


class TestStorageObject:
    """Tests for StorageObject class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test StorageObject initialization."""
        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        assert obj.id == "obj_123"
        assert obj.upload_url == "https://upload.example.com"

    def test_init_no_upload_url(self, mock_client: Mock) -> None:
        """Test StorageObject initialization without upload URL."""
        obj = StorageObject(mock_client, "obj_123", None)
        assert obj.id == "obj_123"
        assert obj.upload_url is None

    def test_repr(self, mock_client: Mock) -> None:
        """Test StorageObject string representation."""
        obj = StorageObject(mock_client, "obj_123", None)
        assert repr(obj) == "<StorageObject id='obj_123'>"

    def test_refresh(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test refresh method."""
        mock_client.objects.retrieve.return_value = object_view

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.refresh(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == object_view
        mock_client.objects.retrieve.assert_called_once_with(
            "obj_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_complete(self, mock_client: Mock) -> None:
        """Test complete method updates upload_url to None."""
        completed_view = SimpleNamespace(id="obj_123", upload_url=None)
        mock_client.objects.complete.return_value = completed_view

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        assert obj.upload_url == "https://upload.example.com"

        result = obj.complete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == completed_view
        assert obj.upload_url is None
        mock_client.objects.complete.assert_called_once_with(
            "obj_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_get_download_url_without_duration(self, mock_client: Mock) -> None:
        """Test get_download_url without duration_seconds."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.get_download_url(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == download_url_view
        mock_client.objects.download.assert_called_once_with(
            "obj_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_get_download_url_with_duration(self, mock_client: Mock) -> None:
        """Test get_download_url with duration_seconds."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.get_download_url(
            duration_seconds=3600,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == download_url_view
        mock_client.objects.download.assert_called_once_with(
            "obj_123",
            duration_seconds=3600,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_download_as_bytes(self, mock_client: Mock) -> None:
        """Test download_as_bytes method."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        mock_response = create_mock_httpx_response(content=b"file content")
        http_client = Mock()
        http_client.get.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.download_as_bytes(
            duration_seconds=3600,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == b"file content"
        http_client.get.assert_called_once_with("https://download.example.com/obj_123")
        mock_response.raise_for_status.assert_called_once()

    def test_download_as_text(self, mock_client: Mock) -> None:
        """Test download_as_text forces UTF-8 encoding."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        mock_response = create_mock_httpx_response(text="file content", encoding="latin-1")
        http_client = Mock()
        http_client.get.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.download_as_text()

        assert result == "file content"
        assert mock_response.encoding == "utf-8"
        http_client.get.assert_called_once_with("https://download.example.com/obj_123")

    def test_delete(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test delete method."""
        mock_client.objects.delete.return_value = object_view

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

        assert result == object_view
        mock_client.objects.delete.assert_called_once_with(
            "obj_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
            idempotency_key="key-123",
        )

    def test_upload_content_string(self, mock_client: Mock) -> None:
        """Test upload_content with string."""
        mock_response = create_mock_httpx_response()
        http_client = Mock()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        obj.upload_content("test content")

        http_client.put.assert_called_once_with("https://upload.example.com", content="test content")
        mock_response.raise_for_status.assert_called_once()

    def test_upload_content_bytes(self, mock_client: Mock) -> None:
        """Test upload_content with bytes."""
        mock_response = create_mock_httpx_response()
        http_client = Mock()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        obj.upload_content(b"test content")

        http_client.put.assert_called_once_with("https://upload.example.com", content=b"test content")
        mock_response.raise_for_status.assert_called_once()

    def test_upload_content_no_url(self, mock_client: Mock) -> None:
        """Test upload_content raises error when no upload URL."""
        obj = StorageObject(mock_client, "obj_123", None)

        with pytest.raises(RuntimeError, match="No upload URL available"):
            obj.upload_content("test content")

    def test_ensure_upload_url_with_url(self, mock_client: Mock) -> None:
        """Test _ensure_upload_url returns URL when available."""
        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        url = obj._ensure_upload_url()
        assert url == "https://upload.example.com"

    def test_ensure_upload_url_no_url(self, mock_client: Mock) -> None:
        """Test _ensure_upload_url raises error when no URL."""
        obj = StorageObject(mock_client, "obj_123", None)

        with pytest.raises(RuntimeError, match="No upload URL available"):
            obj._ensure_upload_url()


class TestStorageObjectEdgeCases:
    """Tests for StorageObject edge cases."""

    def test_large_file_upload(self, mock_client: Mock) -> None:
        """Test handling of large file uploads."""
        LARGE_FILE_SIZE = 10 * 1024 * 1024  # 10MB

        object_view = SimpleNamespace(id="obj_123", upload_url="https://upload.example.com")
        mock_client.objects.create.return_value = object_view

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        large_content = b"x" * LARGE_FILE_SIZE  # 10MB
        obj.upload_content(large_content)

        http_client.put.assert_called_once_with("https://upload.example.com", content=large_content)


class TestStorageObjectPythonSpecific:
    """Tests for Python-specific StorageObject behavior."""

    def test_upload_data_types(self, mock_client: Mock) -> None:
        """Test Python supports more upload data types."""
        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")

        # String
        obj.upload_content("string content")

        # Bytes
        obj.upload_content(b"bytes content")

        assert http_client.put.call_count == 2
