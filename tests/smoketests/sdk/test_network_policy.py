"""Synchronous SDK smoke tests for Network Policy operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30


class TestNetworkPolicyLifecycle:
    """Test basic network policy lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_create(self, sdk_client: RunloopSDK) -> None:
        """Test creating a network policy."""
        name = unique_name("sdk-network-policy")
        network_policy = sdk_client.network_policy.create(
            name=name,
            description="SDK smoke test network policy",
            allowed_hostnames=["github.com", "*.npmjs.org"],
        )

        try:
            assert network_policy is not None
            assert network_policy.id is not None
            assert len(network_policy.id) > 0
        finally:
            network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_get_info(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving network policy information."""
        name = unique_name("sdk-network-policy-info")
        network_policy = sdk_client.network_policy.create(
            name=name,
            description="Test policy for get_info",
            allowed_hostnames=["example.com"],
        )

        try:
            info = network_policy.get_info()

            assert info.id == network_policy.id
            assert info.name == name
            assert info.description == "Test policy for get_info"
        finally:
            network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_update(self, sdk_client: RunloopSDK) -> None:
        """Test updating a network policy."""
        network_policy = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-update"),
            description="Original description",
            allowed_hostnames=["example.com"],
        )

        try:
            # Update the policy
            updated_name = unique_name("sdk-network-policy-updated")
            result = network_policy.update(
                name=updated_name,
                description="Updated description",
                allowed_hostnames=["example.com", "api.example.com"],
            )

            assert result is not None
            assert result.name == updated_name
            assert result.description == "Updated description"

            # Verify update persisted
            info = network_policy.get_info()
            assert info.name == updated_name
            assert info.description == "Updated description"
        finally:
            network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_delete(self, sdk_client: RunloopSDK) -> None:
        """Test deleting a network policy."""
        network_policy = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-delete"),
            allowed_hostnames=["example.com"],
        )

        result = network_policy.delete()

        assert result is not None


class TestNetworkPolicyCreationVariations:
    """Test different network policy creation scenarios."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_with_allow_all(self, sdk_client: RunloopSDK) -> None:
        """Test creating a network policy with allow_all enabled."""
        network_policy = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-allow-all"),
            description="Allow all egress traffic",
            allow_all=True,
        )

        try:
            info = network_policy.get_info()
            assert info.egress is not None
            assert info.egress.allow_all is True
        finally:
            network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_with_devbox_to_devbox(self, sdk_client: RunloopSDK) -> None:
        """Test creating a network policy with devbox-to-devbox traffic allowed."""
        network_policy = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-d2d"),
            description="Allow devbox to devbox traffic",
            allow_devbox_to_devbox=True,
            allowed_hostnames=["internal.example.com"],
        )

        try:
            info = network_policy.get_info()
            assert info.egress is not None
            assert info.egress.allow_devbox_to_devbox is True
        finally:
            network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_with_wildcard_hostnames(self, sdk_client: RunloopSDK) -> None:
        """Test creating a network policy with wildcard hostname patterns."""
        network_policy = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-wildcards"),
            allowed_hostnames=[
                "*.github.com",
                "*.githubusercontent.com",
                "registry.npmjs.org",
                "*.pypi.org",
            ],
        )

        try:
            info = network_policy.get_info()
            assert info.egress is not None
            assert info.egress.allowed_hostnames is not None
            assert len(info.egress.allowed_hostnames) == 4
        finally:
            network_policy.delete()


class TestNetworkPolicyListing:
    """Test network policy listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_network_policies(self, sdk_client: RunloopSDK) -> None:
        """Test listing network policies."""
        policies = sdk_client.network_policy.list(limit=10)

        assert isinstance(policies, list)
        # List might be empty, that's okay
        assert len(policies) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_get_network_policy_by_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving network policy by ID."""
        # Create a policy
        created = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-retrieve"),
            allowed_hostnames=["example.com"],
        )

        try:
            # Retrieve it by ID
            retrieved = sdk_client.network_policy.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same policy
            info = retrieved.get_info()
            assert info.id == created.id
        finally:
            created.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_network_policies_with_limit(self, sdk_client: RunloopSDK) -> None:
        """Test listing network policies with a limit."""
        # Create two policies
        policy1 = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-list-1"),
            allowed_hostnames=["example1.com"],
        )
        policy2 = sdk_client.network_policy.create(
            name=unique_name("sdk-network-policy-list-2"),
            allowed_hostnames=["example2.com"],
        )

        try:
            # List with limit
            policies = sdk_client.network_policy.list(limit=100)

            assert isinstance(policies, list)
            # Should find our policies
            policy_ids = [p.id for p in policies]
            assert policy1.id in policy_ids
            assert policy2.id in policy_ids
        finally:
            policy1.delete()
            policy2.delete()
