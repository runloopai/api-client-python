"""Comprehensive tests for sync StorageObject class."""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tests.sdk.conftest import MockObjectView, create_mock_httpx_response
from runloop_api_client.sdk import StorageObject
from runloop_api_client.sdk.sync import StorageObjectClient


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

    @patch("httpx.get")
    def test_download_as_bytes(self, mock_get: Mock, mock_client: Mock) -> None:
        """Test download_as_bytes method."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        mock_response = create_mock_httpx_response(content=b"file content")
        mock_get.return_value = mock_response

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.download_as_bytes(
            duration_seconds=3600,
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == b"file content"
        mock_get.assert_called_once_with("https://download.example.com/obj_123")
        mock_response.raise_for_status.assert_called_once()

    @patch("httpx.get")
    def test_download_as_text_default_encoding(self, mock_get: Mock, mock_client: Mock) -> None:
        """Test download_as_text with default encoding."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        mock_response = create_mock_httpx_response(text="file content", encoding="utf-8")
        mock_get.return_value = mock_response

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.download_as_text()

        assert result == "file content"
        assert mock_response.encoding == "utf-8"
        mock_get.assert_called_once()

    @patch("httpx.get")
    def test_download_as_text_custom_encoding(self, mock_get: Mock, mock_client: Mock) -> None:
        """Test download_as_text with custom encoding."""
        download_url_view = SimpleNamespace(download_url="https://download.example.com/obj_123")
        mock_client.objects.download.return_value = download_url_view

        mock_response = create_mock_httpx_response(text="file content", encoding="utf-8")
        mock_get.return_value = mock_response

        obj = StorageObject(mock_client, "obj_123", None)
        result = obj.download_as_text(encoding="latin-1")

        assert result == "file content"
        assert mock_response.encoding == "latin-1"
        mock_get.assert_called_once()

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

    @patch("httpx.put")
    def test_upload_content_string(self, mock_put: Mock, mock_client: Mock) -> None:
        """Test upload_content with string."""
        mock_response = create_mock_httpx_response()
        mock_put.return_value = mock_response

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        obj.upload_content("test content")

        mock_put.assert_called_once_with("https://upload.example.com", content=b"test content")
        mock_response.raise_for_status.assert_called_once()

    @patch("httpx.put")
    def test_upload_content_bytes(self, mock_put: Mock, mock_client: Mock) -> None:
        """Test upload_content with bytes."""
        mock_response = create_mock_httpx_response()
        mock_put.return_value = mock_response

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        obj.upload_content(b"test content")

        mock_put.assert_called_once_with("https://upload.example.com", content=b"test content")
        mock_response.raise_for_status.assert_called_once()

    @patch("httpx.put")
    def test_upload_content_path(self, mock_put: Mock, mock_client: Mock, tmp_path: Path) -> None:
        """Test upload_content with Path."""
        mock_response = create_mock_httpx_response()
        mock_put.return_value = mock_response

        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test content")

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        obj.upload_content(temp_file)

        mock_put.assert_called_once()
        call_args = mock_put.call_args
        assert call_args[0][0] == "https://upload.example.com"
        assert call_args[1]["content"] == b"test content"
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

        with patch("httpx.put") as mock_put:
            mock_response = create_mock_httpx_response()
            mock_put.return_value = mock_response

            obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
            large_content = b"x" * LARGE_FILE_SIZE  # 10MB
            obj.upload_content(large_content)

            mock_put.assert_called_once()
            call_args = mock_put.call_args
            assert len(call_args[1]["content"]) == LARGE_FILE_SIZE


class TestStorageObjectPythonSpecific:
    """Tests for Python-specific StorageObject behavior."""

    def test_content_type_detection(self, mock_client: Mock, object_view: MockObjectView) -> None:
        """Test content type detection differences."""
        mock_client.objects.create.return_value = object_view

        client = StorageObjectClient(mock_client)

        # Python detects from extension
        client.create("test.txt")
        call1 = mock_client.objects.create.call_args[1]
        assert call1["content_type"] == "text"

        # Explicit content type
        client.create("test.bin", content_type="binary")
        call2 = mock_client.objects.create.call_args[1]
        assert call2["content_type"] == "binary"

    def test_upload_data_types(self, mock_client: Mock, tmp_path: Path) -> None:
        """Test Python supports more upload data types."""
        with patch("httpx.put") as mock_put:
            mock_response = create_mock_httpx_response()
            mock_put.return_value = mock_response

            obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")

            # String
            obj.upload_content("string content")

            # Bytes
            obj.upload_content(b"bytes content")

            # Path (Python-specific)
            temp_file = tmp_path / "test_file.txt"
            temp_file.write_text("file content")
            obj.upload_content(temp_file)

            assert mock_put.call_count == 3
