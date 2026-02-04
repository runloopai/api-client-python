"""Synchronous SDK smoke tests for Gateway Config operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.types.gateway_config_create_params import AuthMechanism

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30


class TestGatewayConfigLifecycle:
    """Test basic gateway config lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_create(self, sdk_client: RunloopSDK) -> None:
        """Test creating a gateway config."""
        name = unique_name("sdk-gateway-config")
        gateway_config = sdk_client.gateway_config.create(
            name=name,
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
            description="SDK smoke test gateway config",
        )

        try:
            assert gateway_config is not None
            assert gateway_config.id is not None
            assert len(gateway_config.id) > 0
        finally:
            gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_get_info(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving gateway config information."""
        name = unique_name("sdk-gateway-config-info")
        gateway_config = sdk_client.gateway_config.create(
            name=name,
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
            description="Test gateway config for get_info",
        )

        try:
            info = gateway_config.get_info()

            assert info.id == gateway_config.id
            assert info.name == name
            assert info.endpoint == "https://api.example.com"
            assert info.description == "Test gateway config for get_info"
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == "bearer"
        finally:
            gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_update(self, sdk_client: RunloopSDK) -> None:
        """Test updating a gateway config."""
        gateway_config = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-update"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
            description="Original description",
        )

        try:
            # Update the gateway config
            updated_name = unique_name("sdk-gateway-config-updated")
            result = gateway_config.update(
                name=updated_name,
                description="Updated description",
            )

            assert result is not None
            assert result.name == updated_name
            assert result.description == "Updated description"

            # Verify update persisted
            info = gateway_config.get_info()
            assert info.name == updated_name
            assert info.description == "Updated description"
        finally:
            gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_update_endpoint(self, sdk_client: RunloopSDK) -> None:
        """Test updating gateway config endpoint."""
        gateway_config = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-endpoint"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            result = gateway_config.update(
                endpoint="https://api.updated-example.com",
            )

            assert result.endpoint == "https://api.updated-example.com"

            # Verify update persisted
            info = gateway_config.get_info()
            assert info.endpoint == "https://api.updated-example.com"
        finally:
            gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_update_auth_mechanism(self, sdk_client: RunloopSDK) -> None:
        """Test updating gateway config auth mechanism."""
        gateway_config = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-auth"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            result = gateway_config.update(
                auth_mechanism={"type": "header", "key": "x-api-key"},
            )

            assert result.auth_mechanism.type == "header"
            assert result.auth_mechanism.key == "x-api-key"

            # Verify update persisted
            info = gateway_config.get_info()
            assert info.auth_mechanism.type == "header"
            assert info.auth_mechanism.key == "x-api-key"
        finally:
            gateway_config.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_delete(self, sdk_client: RunloopSDK) -> None:
        """Test deleting a gateway config."""
        gateway_config = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-delete"),
            endpoint="https://api.example.com",
            auth_mechanism={"type": "bearer"},
        )

        result = gateway_config.delete()

        assert result is not None


class TestGatewayConfigAuthMechanisms:
    """Test different gateway config auth mechanism types."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    @pytest.mark.parametrize(
        "auth_mechanism,expected_type,expected_key",
        [
            ({"type": "bearer"}, "bearer", None),
            ({"type": "header", "key": "x-api-key"}, "header", "x-api-key"),
        ],
    )
    def test_gateway_config_auth_mechanisms(
        self, sdk_client: RunloopSDK, auth_mechanism: AuthMechanism, expected_type: str, expected_key: str | None
    ) -> None:
        """Test creating gateway configs with different auth mechanisms."""
        gateway_config = sdk_client.gateway_config.create(
            name=unique_name(f"sdk-gateway-{expected_type}"),
            endpoint=f"https://api.{expected_type}-test.com",
            auth_mechanism=auth_mechanism,
        )

        try:
            info = gateway_config.get_info()
            assert info.auth_mechanism is not None
            assert info.auth_mechanism.type == expected_type
            if expected_key is not None:
                assert info.auth_mechanism.key == expected_key
        finally:
            gateway_config.delete()


class TestGatewayConfigListing:
    """Test gateway config listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_gateway_configs(self, sdk_client: RunloopSDK) -> None:
        """Test listing gateway configs."""
        configs = sdk_client.gateway_config.list(limit=10)

        assert isinstance(configs, list)
        # List might be empty or have system configs, that's okay
        assert len(configs) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_get_gateway_config_by_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving gateway config by ID."""
        # Create a gateway config
        created = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-retrieve"),
            endpoint="https://api.retrieve-test.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            # Retrieve it by ID
            retrieved = sdk_client.gateway_config.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same gateway config
            info = retrieved.get_info()
            assert info.id == created.id
        finally:
            created.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_gateway_configs_with_limit(self, sdk_client: RunloopSDK) -> None:
        """Test listing gateway configs with a limit."""
        # Create two gateway configs
        config1 = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-list-1"),
            endpoint="https://api.list-test-1.com",
            auth_mechanism={"type": "bearer"},
        )
        config2 = sdk_client.gateway_config.create(
            name=unique_name("sdk-gateway-config-list-2"),
            endpoint="https://api.list-test-2.com",
            auth_mechanism={"type": "bearer"},
        )

        try:
            # List with limit
            configs = sdk_client.gateway_config.list(limit=100)

            assert isinstance(configs, list)
            # Should find our gateway configs
            config_ids = [c.id for c in configs]
            assert config1.id in config_ids
            assert config2.id in config_ids
        finally:
            config1.delete()
            config2.delete()
