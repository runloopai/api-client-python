"""Comprehensive tests for async Axon class."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockAxonView, MockPublishResultView
from runloop_api_client.sdk import AsyncAxon


class TestAsyncAxon:
    """Tests for AsyncAxon class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncAxon initialization."""
        axon = AsyncAxon(mock_async_client, "axn_123")
        assert axon.id == "axn_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncAxon string representation."""
        axon = AsyncAxon(mock_async_client, "axn_123")
        assert repr(axon) == "<AsyncAxon id='axn_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, axon_view: MockAxonView) -> None:
        """Test get_info method."""
        mock_async_client.axons.retrieve = AsyncMock(return_value=axon_view)

        axon = AsyncAxon(mock_async_client, "axn_123")
        result = await axon.get_info(
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

        assert result == axon_view
        mock_async_client.axons.retrieve.assert_awaited_once_with(
            "axn_123",
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

    @pytest.mark.asyncio
    async def test_publish(self, mock_async_client: AsyncMock) -> None:
        """Test publish method."""
        mock_result = MockPublishResultView()
        mock_async_client.axons.publish = AsyncMock(return_value=mock_result)

        axon = AsyncAxon(mock_async_client, "axn_123")
        result = await axon.publish(
            event_type="test",
            origin="USER_EVENT",
            payload="{}",
            source="sdk",
        )

        assert result == mock_result
        mock_async_client.axons.publish.assert_awaited_once_with(
            "axn_123",
            event_type="test",
            origin="USER_EVENT",
            payload="{}",
            source="sdk",
        )

    @pytest.mark.asyncio
    async def test_subscribe_sse(self, mock_async_client: AsyncMock) -> None:
        """Test subscribe_sse method."""
        mock_stream = AsyncMock()
        mock_async_client.axons.subscribe_sse = AsyncMock(return_value=mock_stream)

        axon = AsyncAxon(mock_async_client, "axn_123")
        result = await axon.subscribe_sse()

        assert result == mock_stream
        mock_async_client.axons.subscribe_sse.assert_awaited_once_with("axn_123")
