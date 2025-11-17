"""Tests for Devbox error handling, edge cases, and Python-specific behavior.

Tests error scenarios, edge cases, and Python-specific features that don't
fit into other categories.
"""

from __future__ import annotations

import threading
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock

import httpx
import pytest

from tests.sdk.conftest import (
    NUM_CONCURRENT_THREADS,
    MockDevboxView,
    create_mock_httpx_response,
)
from runloop_api_client.sdk import Devbox, StorageObject
from runloop_api_client.types import DevboxView
from runloop_api_client._exceptions import APIStatusError


class TestDevboxErrorHandling:
    """Tests for Devbox error handling scenarios."""

    def test_network_error(self, mock_client: Mock) -> None:
        """Test handling of network errors."""
        mock_client.devboxes.retrieve.side_effect = httpx.NetworkError("Connection failed")

        devbox = Devbox(mock_client, "dev_123")
        with pytest.raises(httpx.NetworkError):
            devbox.get_info()

    @pytest.mark.parametrize(
        "status_code,message",
        [
            (404, "Not Found"),
            (500, "Internal Server Error"),
            (503, "Service Unavailable"),
        ],
    )
    def test_api_error(self, mock_client: Mock, status_code: int, message: str) -> None:
        """Test handling of API errors with various status codes."""
        response = create_mock_httpx_response(status_code=status_code, headers={}, text=message)
        error = APIStatusError(message=message, response=response, body=None)

        mock_client.devboxes.retrieve.side_effect = error

        devbox = Devbox(mock_client, "dev_123")
        with pytest.raises(APIStatusError):
            devbox.get_info()

    def test_timeout_error(self, mock_client: Mock) -> None:
        """Test handling of timeout errors."""
        mock_client.devboxes.retrieve.side_effect = httpx.TimeoutException("Request timed out")

        devbox = Devbox(mock_client, "dev_123")
        with pytest.raises(httpx.TimeoutException):
            devbox.get_info(timeout=1.0)


class TestDevboxEdgeCases:
    """Tests for Devbox edge cases."""

    def test_empty_responses(self, mock_client: Mock) -> None:
        """Test handling of empty responses."""
        empty_view = SimpleNamespace(id="dev_123", status="", name="")
        mock_client.devboxes.retrieve.return_value = empty_view

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.get_info()
        assert result == empty_view

    def test_none_values(self, mock_client: Mock) -> None:
        """Test handling of None values."""
        view_with_none = SimpleNamespace(id="dev_123", status=None, name=None)
        mock_client.devboxes.retrieve.return_value = view_with_none

        devbox = Devbox(mock_client, "dev_123")
        result = devbox.get_info()
        assert result.status is None
        assert result.name is None

    def test_concurrent_operations(
        self, mock_client: Mock, thread_cleanup: tuple[list[threading.Thread], list[threading.Event]]
    ) -> None:
        """Test concurrent operations."""
        mock_client.devboxes.retrieve.return_value = SimpleNamespace(id="dev_123", status="running")

        devbox = Devbox(mock_client, "dev_123")
        results: list[DevboxView] = []

        def get_info() -> None:
            results.append(devbox.get_info())

        threads = [threading.Thread(target=get_info) for _ in range(NUM_CONCURRENT_THREADS)]
        # Register threads for automatic cleanup
        cleanup_threads, _ = thread_cleanup
        cleanup_threads.extend(threads)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(results) == NUM_CONCURRENT_THREADS


class TestDevboxPythonSpecific:
    """Tests for Python-specific Devbox behavior."""

    def test_context_manager_vs_manual_cleanup(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test context manager provides automatic cleanup."""
        mock_client.devboxes.shutdown.return_value = devbox_view

        # Context manager approach (Pythonic)
        with Devbox(mock_client, "dev_123"):
            pass

        mock_client.devboxes.shutdown.assert_called_once()

        # Manual cleanup (TypeScript-like)
        devbox = Devbox(mock_client, "dev_123")
        devbox.shutdown()
        assert mock_client.devboxes.shutdown.call_count == 2

    def test_path_handling(self, mock_client: Mock, tmp_path: Path) -> None:
        """Test Path handling (Python-specific)."""
        object_view = SimpleNamespace(id="obj_123", upload_url="https://upload.example.com")
        mock_client.objects.create.return_value = object_view

        temp_file = tmp_path / "test_file.txt"
        temp_file.write_text("test")

        http_client = Mock()
        mock_response = create_mock_httpx_response()
        http_client.put.return_value = mock_response
        mock_client._client = http_client

        obj = StorageObject(mock_client, "obj_123", "https://upload.example.com")
        obj.upload_content(temp_file.read_text())
        obj.upload_content(temp_file.read_bytes())

        assert http_client.put.call_count == 2
