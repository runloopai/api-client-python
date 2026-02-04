"""Asynchronous SDK smoke tests for Gateway Config operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30


class TestAsyncGatewayConfigLifecycle:
    """Test basic async gateway config lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_create(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a gateway config."""
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
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving gateway config information."""
        name = unique_name("sdk-async-gateway-config-info")
        gateway_config = await async_sdk_client.gateway_config.create(
            name=name,
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
            description="Async test gateway config for get_info",
        )

        try:
            info = await gateway_config.get_info()

            assert info.id == gateway_config.id
            assert info.name == name
            assert info.endpoint == "https://api.example.com"
            assert info.description == "Async test gateway config for get_info"
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == "bearer"
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_update(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test updating a gateway config."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-update"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
            description="Original async description",
        )

        try:
            # Update the gateway config
            updated_name = unique_name("sdk-async-gateway-config-updated")
            result = await gateway_config.update(
                name=updated_name,
                description="Updated async description",
            )

            assert result is not None
            assert result.name == updated_name
            assert result.description == "Updated async description"

            # Verify update persisted
            info = await gateway_config.get_info()
            assert info.name == updated_name
            assert info.description == "Updated async description"
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_update_endpoint(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test updating gateway config endpoint."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-endpoint"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            result = await gateway_config.update(
                endpoint="https://api.updated-example.com",
            )

            assert result.endpoint == "https://api.updated-example.com"

            # Verify update persisted
            info = await gateway_config.get_info()
            assert info.endpoint == "https://api.updated-example.com"
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_update_auth_mechanism(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test updating gateway config auth mechanism."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-auth"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            result = await gateway_config.update(
                auth_mechanism={"type": "header", "key": "x-api-key"},
            )

            assert result.auth_mechanism.type == "header"
            assert result.auth_mechanism.key == "x-api-key"

            # Verify update persisted
            info = await gateway_config.get_info()
            assert info.auth_mechanism.type == "header"
            assert info.auth_mechanism.key == "x-api-key"
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_delete(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test deleting a gateway config."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-delete"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
        )

        result = await gateway_config.delete()

        assert result is not None


class TestAsyncGatewayConfigAuthMechanisms:
    """Test different async gateway config auth mechanism types."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_with_bearer_auth(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a gateway config with bearer auth."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-bearer"),
            endpoint="https://api.bearer-test.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            info = await gateway_config.get_info()
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == "bearer"
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_with_header_auth(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a gateway config with header auth."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-header"),
            endpoint="https://api.header-test.com",
            auth_mechanism={"type": "header", "key": "x-api-key"},
        )

        try:
            info = await gateway_config.get_info()
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == "header"
            assert info.auth_mechanism.key == "x-api-key"
        finally:
            await gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_with_authorization_header(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a gateway config with Authorization header."""
        gateway_config = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-auth-header"),
            endpoint="https://api.auth-header-test.com",
            auth_mechanism={"type": "header", "key": "Authorization"},
        )

        try:
            info = await gateway_config.get_info()
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == "header"
            assert info.auth_mechanism.key == "Authorization"
        finally:
            await gateway_config.delete()


class TestAsyncGatewayConfigListing:
    """Test async gateway config listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_gateway_configs(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing gateway configs."""
        configs = await async_sdk_client.gateway_config.list(limit=10)

        assert isinstance(configs, list)
        # List might be empty or have system configs, that's okay
        assert len(configs) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_get_gateway_config_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving gateway config by ID."""
        # Create a gateway config
        created = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-retrieve"),
            endpoint="https://api.retrieve-test.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            # Retrieve it by ID
            retrieved = async_sdk_client.gateway_config.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same gateway config
            info = await retrieved.get_info()
            assert info.id == created.id
        finally:
            await created.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_gateway_configs_with_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing gateway configs with a limit."""
        # Create two gateway configs
        config1 = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-list-1"),
            endpoint="https://api.list-test-1.com",
            auth_mechanism={"type": "bearer"},
        )
        config2 = await async_sdk_client.gateway_config.create(
            name=unique_name("sdk-async-gateway-config-list-2"),
            endpoint="https://api.list-test-2.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            # List with limit
            configs = await async_sdk_client.gateway_config.list(limit=100)

            assert isinstance(configs, list)
            # Should find our gateway configs
            config_ids = [c.id for c in configs]
            assert config1.id in config_ids
            assert config2.id in config_ids
        finally:
            await config1.delete()
            await config2.delete()
