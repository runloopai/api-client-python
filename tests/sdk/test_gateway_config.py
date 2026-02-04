"""Comprehensive tests for sync GatewayConfig class."""

from __future__ import annotations

from unittest.mock import Mock

from tests.sdk.conftest import MockGatewayConfigView
from runloop_api_client.sdk import GatewayConfig


class TestGatewayConfig:
    """Tests for GatewayConfig class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test GatewayConfig initialization."""
        gateway_config = GatewayConfig(mock_client, "gwc_123")
        assert gateway_config.id == "gwc_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test GatewayConfig string representation."""
        gateway_config = GatewayConfig(mock_client, "gwc_123")
        assert repr(gateway_config) == "<GatewayConfig id='gwc_123'>"

    def test_get_info(self, mock_client: Mock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test get_info method."""
        mock_client.gateway_configs.retrieve.return_value = gateway_config_view

        gateway_config = GatewayConfig(mock_client, "gwc_123")
        result = gateway_config.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == gateway_config_view
        mock_client.gateway_configs.retrieve.assert_called_once_with(
            "gwc_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_update(self, mock_client: Mock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test update method."""
        mock_client.gateway_configs.update.return_value = gateway_config_view

        gateway_config = GatewayConfig(mock_client, "gwc_123")
        result = gateway_config.update(
            name="updated-gateway",
            description="Updated description",
            endpoint="https://api.updated.com",
            auth_mechanism={"type": "header", "key": "x-api-key"},
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

        assert result == gateway_config_view
        mock_client.gateway_configs.update.assert_called_once_with(
            "gwc_123",
            name="updated-gateway",
            description="Updated description",
            endpoint="https://api.updated.com",
            auth_mechanism={"type": "header", "key": "x-api-key"},
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

    def test_update_partial(self, mock_client: Mock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test update method with partial fields."""
        mock_client.gateway_configs.update.return_value = gateway_config_view

        gateway_config = GatewayConfig(mock_client, "gwc_123")
        result = gateway_config.update(
            name="renamed-gateway",
        )

        assert result == gateway_config_view
        mock_client.gateway_configs.update.assert_called_once_with(
            "gwc_123",
            name="renamed-gateway",
        )

    def test_delete(self, mock_client: Mock, gateway_config_view: MockGatewayConfigView) -> None:
        """Test delete method."""
        mock_client.gateway_configs.delete.return_value = gateway_config_view

        gateway_config = GatewayConfig(mock_client, "gwc_123")
        result = gateway_config.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == gateway_config_view
        mock_client.gateway_configs.delete.assert_called_once_with(
            "gwc_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )
