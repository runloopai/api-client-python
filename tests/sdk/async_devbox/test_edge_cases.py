"""Tests for AsyncDevbox error handling.

Tests async error scenarios including network errors.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from runloop_api_client.sdk import AsyncDevbox


class TestAsyncDevboxErrorHandling:
    """Tests for AsyncDevbox error handling scenarios."""

    @pytest.mark.asyncio
    async def test_async_network_error(self, mock_async_client: AsyncMock) -> None:
        """Test handling of network errors in async."""
        mock_async_client.devboxes.retrieve = AsyncMock(side_effect=httpx.NetworkError("Connection failed"))

        devbox = AsyncDevbox(mock_async_client, "dev_123")
        with pytest.raises(httpx.NetworkError):
            await devbox.get_info()
