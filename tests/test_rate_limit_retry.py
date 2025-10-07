"""Tests for rate limit retry behavior on file write operations."""

from __future__ import annotations

import time
from typing import Any
from unittest.mock import Mock, patch

import httpx
import pytest
import respx

from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client._exceptions import RateLimitError
from runloop_api_client.types import DevboxExecutionDetailView

base_url = "http://127.0.0.1:4010"


class TestRateLimitRetry:
    """Test rate limit retry behavior for file write operations."""

    def test_write_file_contents_retries_on_429(self, respx_mock: respx.MockRouter) -> None:
        """Test that write_file_contents retries when encountering 429 errors."""
        client = Runloop(base_url=base_url, bearer_token="test-token", max_retries=3)

        # Mock the first two requests to return 429, then succeed
        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")

        route.side_effect = [
            # First attempt: 429
            httpx.Response(
                status_code=429,
                json={
                    "error": {
                        "message": "Write operations for this devbox are currently rate limited. Please retry in a few seconds."
                    }
                },
            ),
            # Second attempt: 429
            httpx.Response(
                status_code=429,
                json={
                    "error": {
                        "message": "Write operations for this devbox are currently rate limited. Please retry in a few seconds."
                    }
                },
            ),
            # Third attempt: success
            httpx.Response(
                status_code=200,
                json={
                    "id": "exec-123",
                    "devbox_id": "test-devbox-id",
                    "status": "completed",
                    "exit_status": 0,
                },
            ),
        ]

        start_time = time.time()
        result = client.devboxes.write_file_contents(
            id="test-devbox-id",
            contents="test content",
            file_path="/tmp/test.txt",
        )
        elapsed_time = time.time() - start_time

        # Verify the request succeeded
        assert result.id == "exec-123"
        assert result.status == "completed"

        # Verify retry happened (should have taken at least some time due to backoff)
        assert elapsed_time > 0.1  # At least some delay from retries

        # Verify all three requests were made
        assert route.call_count == 3

    def test_write_file_contents_respects_retry_after_header(self, respx_mock: respx.MockRouter) -> None:
        """Test that write_file_contents respects Retry-After header."""
        client = Runloop(base_url=base_url, bearer_token="test-token", max_retries=2)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")

        route.side_effect = [
            # First attempt: 429 with Retry-After header
            httpx.Response(
                status_code=429,
                headers={"Retry-After": "1"},  # Retry after 1 second
                json={
                    "error": {
                        "message": "Write operations for this devbox are currently rate limited."
                    }
                },
            ),
            # Second attempt: success
            httpx.Response(
                status_code=200,
                json={
                    "id": "exec-456",
                    "devbox_id": "test-devbox-id",
                    "status": "completed",
                    "exit_status": 0,
                },
            ),
        ]

        start_time = time.time()
        result = client.devboxes.write_file_contents(
            id="test-devbox-id",
            contents="test content",
            file_path="/tmp/test.txt",
        )
        elapsed_time = time.time() - start_time

        # Verify the request succeeded
        assert result.id == "exec-456"

        # Verify it waited approximately 1 second (Retry-After value)
        assert elapsed_time >= 0.9  # Allow slight timing variance
        assert elapsed_time < 2.0  # Should not take too long

        # Verify two requests were made
        assert route.call_count == 2

    def test_write_file_contents_exhausts_retries(self, respx_mock: respx.MockRouter) -> None:
        """Test that write_file_contents fails after exhausting retries."""
        client = Runloop(base_url=base_url, bearer_token="test-token", max_retries=2)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")

        # All attempts return 429
        for _ in range(3):  # max_retries + 1
            route.mock(
                return_value=httpx.Response(
                    status_code=429,
                    json={
                        "error": {
                            "message": "Write operations for this devbox are currently rate limited."
                        }
                    },
                )
            )

        # Should raise RateLimitError after exhausting retries
        with pytest.raises(RateLimitError) as exc_info:
            client.devboxes.write_file_contents(
                id="test-devbox-id",
                contents="test content",
                file_path="/tmp/test.txt",
            )

        # Verify error message
        assert "rate limit" in str(exc_info.value).lower()

        # Verify all retry attempts were made
        assert route.call_count == 3  # initial + 2 retries

    def test_upload_file_retries_on_429(self, respx_mock: respx.MockRouter) -> None:
        """Test that upload_file retries when encountering 429 errors."""
        client = Runloop(base_url=base_url, bearer_token="test-token", max_retries=3)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/upload_file")

        route.side_effect = [
            # First attempt: 429
            httpx.Response(
                status_code=429,
                json={
                    "error": {
                        "message": "Write operations for this devbox are currently rate limited."
                    }
                },
            ),
            # Second attempt: success
            httpx.Response(
                status_code=200,
                json={"success": True},
            ),
        ]

        result = client.devboxes.upload_file(
            id="test-devbox-id",
            path="/tmp/test.bin",
            file=b"binary content",
        )

        # Verify the request succeeded
        assert result == {"success": True}

        # Verify retry happened
        assert route.call_count == 2

    def test_write_file_contents_with_custom_max_retries(self, respx_mock: respx.MockRouter) -> None:
        """Test that custom max_retries configuration is respected."""
        client = Runloop(base_url=base_url, bearer_token="test-token", max_retries=5)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")

        # Return 429 for first 4 attempts, then succeed
        route.side_effect = [
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            httpx.Response(
                status_code=200,
                json={
                    "id": "exec-789",
                    "devbox_id": "test-devbox-id",
                    "status": "completed",
                    "exit_status": 0,
                },
            ),
        ]

        result = client.devboxes.write_file_contents(
            id="test-devbox-id",
            contents="test content",
            file_path="/tmp/test.txt",
        )

        # Verify success after 5 attempts (initial + 4 retries)
        assert result.id == "exec-789"
        assert route.call_count == 5

    def test_write_file_contents_no_retry_when_disabled(self, respx_mock: respx.MockRouter) -> None:
        """Test that retries can be disabled by setting max_retries=0."""
        client = Runloop(base_url=base_url, bearer_token="test-token", max_retries=0)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")
        route.mock(
            return_value=httpx.Response(
                status_code=429,
                json={"error": {"message": "Rate limited"}},
            )
        )

        # Should fail immediately without retry
        with pytest.raises(RateLimitError):
            client.devboxes.write_file_contents(
                id="test-devbox-id",
                contents="test content",
                file_path="/tmp/test.txt",
            )

        # Verify only one request was made (no retries)
        assert route.call_count == 1


class TestAsyncRateLimitRetry:
    """Test async rate limit retry behavior for file write operations."""

    @pytest.mark.asyncio
    async def test_write_file_contents_retries_on_429(self, respx_mock: respx.MockRouter) -> None:
        """Test that async write_file_contents retries when encountering 429 errors."""
        client = AsyncRunloop(base_url=base_url, bearer_token="test-token", max_retries=3)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")

        route.side_effect = [
            # First two attempts: 429
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            # Third attempt: success
            httpx.Response(
                status_code=200,
                json={
                    "id": "exec-async-123",
                    "devbox_id": "test-devbox-id",
                    "status": "completed",
                    "exit_status": 0,
                },
            ),
        ]

        start_time = time.time()
        result = await client.devboxes.write_file_contents(
            id="test-devbox-id",
            contents="test content",
            file_path="/tmp/test.txt",
        )
        elapsed_time = time.time() - start_time

        # Verify the request succeeded
        assert result.id == "exec-async-123"

        # Verify retry happened (should have taken some time)
        assert elapsed_time > 0.1

        # Verify all three requests were made
        assert route.call_count == 3

    @pytest.mark.asyncio
    async def test_upload_file_retries_on_429(self, respx_mock: respx.MockRouter) -> None:
        """Test that async upload_file retries when encountering 429 errors."""
        client = AsyncRunloop(base_url=base_url, bearer_token="test-token", max_retries=2)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/upload_file")

        route.side_effect = [
            # First attempt: 429
            httpx.Response(status_code=429, json={"error": {"message": "Rate limited"}}),
            # Second attempt: success
            httpx.Response(status_code=200, json={"success": True}),
        ]

        result = await client.devboxes.upload_file(
            id="test-devbox-id",
            path="/tmp/test.bin",
            file=b"binary content",
        )

        # Verify the request succeeded
        assert result == {"success": True}
        assert route.call_count == 2

    @pytest.mark.asyncio
    async def test_write_file_contents_exhausts_retries(self, respx_mock: respx.MockRouter) -> None:
        """Test that async write_file_contents fails after exhausting retries."""
        client = AsyncRunloop(base_url=base_url, bearer_token="test-token", max_retries=2)

        route = respx_mock.post(f"{base_url}/v1/devboxes/test-devbox-id/write_file_contents")

        # All attempts return 429
        for _ in range(3):
            route.mock(
                return_value=httpx.Response(
                    status_code=429,
                    json={"error": {"message": "Rate limited"}},
                )
            )

        # Should raise RateLimitError
        with pytest.raises(RateLimitError):
            await client.devboxes.write_file_contents(
                id="test-devbox-id",
                contents="test content",
                file_path="/tmp/test.txt",
            )

        # Verify all retry attempts were made
        assert route.call_count == 3
