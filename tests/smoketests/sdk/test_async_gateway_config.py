"""Asynchronous SDK smoke tests for Gateway Config operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30


class TestAsyncGatewayConfigLifecycle:
    """Test async gateway config lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_full_lifecycle(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test complete gateway config lifecycle: create, get_info, update, delete."""
        # Create
        name = unique_name("sdk-async-gateway-config")
        gateway_config = await async_sdk_client.gateway_config.create(
            name=name,
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
            description="SDK async smoke test gateway config",
        )

        try:
            assert gateway_config is not None
            assert gateway_config.id is not None
            assert len(gateway_config.id) > 0

            # Get info
            info = await gateway_config.get_info()
            assert info.id == gateway_config.id
            assert info.name == name
            assert info.endpoint == "https://api.example.com"
            assert info.description == "SDK async smoke test gateway config"
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == "bearer"

            # Update name and description
            updated_name = unique_name("sdk-async-gateway-config-updated")
            result = await gateway_config.update(
                name=updated_name,
                description="Updated async description",
            )
            assert result.name == updated_name
            assert result.description == "Updated async description"

            # Update endpoint
            result = await gateway_config.update(
                endpoint="https://api.updated-example.com",
            )
            assert result.endpoint == "https://api.updated-example.com"

            # Update auth mechanism
            result = await gateway_config.update(
                auth_mechanism={"type": "header", "key": "x-api-key"},
            )
            assert result.auth_mechanism.type == "header"
            assert result.auth_mechanism.key == "x-api-key"

            # Verify all updates persisted
            info = await gateway_config.get_info()
            assert info.name == updated_name
            assert info.description == "Updated async description"
            assert info.endpoint == "https://api.updated-example.com"
            assert info.auth_mechanism.type == "header"
            assert info.auth_mechanism.key == "x-api-key"
        finally:
            # Delete
            result = await gateway_config.delete()
            assert result is not None


class TestAsyncGatewayConfigListing:
    """Test async gateway config listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_list_and_retrieve(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing gateway configs and retrieving by ID."""
        # Create two gateway configs
        config1 = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-list-1"),
            endpoint="https://api.list-test-1.com",
            auth_mechanism={"type": "bearer"},
        )
        config2 = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-list-2"),
            endpoint="https://api.list-test-2.com",
            auth_mechanism={"type": "header", "key": "x-api-key"},
        )

        try:
            # List gateway configs
            configs = await async_sdk_client.gateway_config.list(limit=100)
            assert isinstance(configs, list)
            config_ids = [c.id for c in configs]
            assert config1.id in config_ids
            assert config2.id in config_ids

            # Retrieve by ID
            retrieved = async_sdk_client.gateway_config.from_id(config1.id)
            assert retrieved.id == config1.id
            info = await retrieved.get_info()
            assert info.id == config1.id
        finally:
            await config1.delete()
            await config2.delete()
