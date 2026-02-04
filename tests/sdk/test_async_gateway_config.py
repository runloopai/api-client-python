"""Comprehensive tests for async GatewayConfig class."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockGatewayConfigView
from runloop_api_client.sdk import AsyncGatewayConfig


class TestAsyncGatewayConfig:
    """Tests for AsyncGatewayConfig class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncGatewayConfig initialization."""
        gateway_config = AsyncGatewayConfig(mock_async_client, "gwc_123")
        assert gateway_config.id == "gwc_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncGatewayConfig string representation."""
        gateway_config = AsyncGatewayConfig(mock_async_client, "gwc_123")
        assert repr(gateway_config) == "<AsyncGatewayConfig id='gwc_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test get_info method."""
        mock_async_client.gateway_configs.retrieve = AsyncMock(return_value=gateway_config_view)

        gateway_config = AsyncGatewayConfig(mock_async_client, "gwc_123")
        result = await gateway_config.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == gateway_config_view
        mock_async_client.gateway_configs.retrieve.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update(self, mock_async_client: AsyncMock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test update method."""
        mock_async_client.gateway_configs.update = AsyncMock(return_value=gateway_config_view)

        gateway_config = AsyncGatewayConfig(mock_async_client, "gwc_123")
        result = await gateway_config.update(
            name="updated-gateway",
            description="Updated description",
            endpoint="https://api.updated.com",
            auth_mechanism={"type": "header", "key": "x-api-key"},
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

        assert result == gateway_config_view
        mock_async_client.gateway_configs.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_partial(
        self, mock_async_client: AsyncMock, gateway_config_view: MockGatewayConfigView
    ) -> None:
        """Test update method with partial fields."""
        mock_async_client.gateway_configs.update = AsyncMock(return_value=gateway_config_view)

        gateway_config = AsyncGatewayConfig(mock_async_client, "gwc_123")
        result = await gateway_config.update(
            name="renamed-gateway",
        )

        assert result == gateway_config_view
        mock_async_client.gateway_configs.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_delete(self, mock_async_client: AsyncMock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test delete method."""
        mock_async_client.gateway_configs.delete = AsyncMock(return_value=gateway_config_view)

        gateway_config = AsyncGatewayConfig(mock_async_client, "gwc_123")
        result = await gateway_config.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == gateway_config_view
        mock_async_client.gateway_configs.delete.assert_awaited_once()
