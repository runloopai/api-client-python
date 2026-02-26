"""Synchronous SDK smoke tests for MCP Config operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30

MCP_CONFIG_TEST_ENDPOINT = "https://mcp.example.com"


class TestMcpConfigLifecycle:
    """Test MCP config lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_mcp_config_full_lifecycle(self, sdk_client: RunloopSDK) -> None:
        """Test complete MCP config lifecycle: create, get_info, update, delete."""
        name = unique_name("sdk-mcp-config")
        mcp_config = sdk_client.mcp_config.create(
            name=name,
            endpoint=MCP_CONFIG_TEST_ENDPOINT,
            allowed_tools=["*"],
            description="SDK smoke test MCP config",
        )

        try:
            assert mcp_config is not None
            assert mcp_config.id is not None
            assert len(mcp_config.id) > 0

            # Get info
            info = mcp_config.get_info()
            assert info.id == mcp_config.id
            assert info.name == name
            assert info.endpoint == MCP_CONFIG_TEST_ENDPOINT
            assert info.description == "SDK smoke test MCP config"
            assert info.allowed_tools is not None
            assert "*" in info.allowed_tools
            assert info.create_time_ms is not None
            assert info.create_time_ms > 0

            # Update name and description
            updated_name = unique_name("sdk-mcp-config-updated")
            result = mcp_config.update(
                name=updated_name,
                description="Updated description",
            )
            assert result.name == updated_name
            assert result.description == "Updated description"

            # Update endpoint
            result = mcp_config.update(
                endpoint="https://mcp.updated-example.com",
            )
            assert result.endpoint == "https://mcp.updated-example.com"

            # Update allowed_tools
            result = mcp_config.update(
                allowed_tools=["github.search_*", "github.get_*"],
            )
            assert "github.search_*" in result.allowed_tools
            assert "github.get_*" in result.allowed_tools
            assert len(result.allowed_tools) == 2

            # Verify all updates persisted
            info = mcp_config.get_info()
            assert info.name == updated_name
            assert info.description == "Updated description"
            assert info.endpoint == "https://mcp.updated-example.com"
            assert "github.search_*" in info.allowed_tools
            assert "github.get_*" in info.allowed_tools
        finally:
            result = mcp_config.delete()
            assert result is not None


class TestMcpConfigListing:
    """Test MCP config listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_mcp_config_list_and_retrieve(self, sdk_client: RunloopSDK) -> None:
        """Test listing MCP configs and retrieving by ID."""
        config1 = sdk_client.mcp_config.create(
            name=unique_name("sdk-mcp-config-list-1"),
            endpoint=MCP_CONFIG_TEST_ENDPOINT,
            allowed_tools=["*"],
        )
        config2 = sdk_client.mcp_config.create(
            name=unique_name("sdk-mcp-config-list-2"),
            endpoint=MCP_CONFIG_TEST_ENDPOINT,
            allowed_tools=["github.search_*"],
        )

        try:
            configs = sdk_client.mcp_config.list(limit=100)
            assert isinstance(configs, list)
            config_ids = [c.id for c in configs]
            assert config1.id in config_ids
            assert config2.id in config_ids

            # Retrieve by ID
            retrieved = sdk_client.mcp_config.from_id(config1.id)
            assert retrieved.id == config1.id
            info = retrieved.get_info()
            assert info.id == config1.id
        finally:
            config1.delete()
            config2.delete()
