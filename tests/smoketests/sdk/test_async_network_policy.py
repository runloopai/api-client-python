"""Asynchronous SDK smoke tests for Network Policy operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30


class TestAsyncNetworkPolicyLifecycle:
    """Test basic async network policy lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_create(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a network policy."""
        name = unique_name("sdk-async-network-policy")
        network_policy = await async_sdk_client.network_policy.create(
            name=name,
            description="SDK async smoke test network policy",
            allowed_hostnames=["github.com", "*.npmjs.org"],
        )

        try:
            assert network_policy is not None
            assert network_policy.id is not None
            assert len(network_policy.id) > 0
        finally:
            await network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving network policy information."""
        name = unique_name("sdk-async-network-policy-info")
        network_policy = await async_sdk_client.network_policy.create(
            name=name,
            description="Async test policy for get_info",
            allowed_hostnames=["example.com"],
        )

        try:
            info = await network_policy.get_info()

            assert info.id == network_policy.id
            assert info.name == name
            assert info.description == "Async test policy for get_info"
        finally:
            await network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_update(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test updating a network policy."""
        network_policy = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-update"),
            description="Original async description",
            allowed_hostnames=["example.com"],
        )

        try:
            # Update the policy
            updated_name = unique_name("sdk-async-network-policy-updated")
            result = await network_policy.update(
                name=updated_name,
                description="Updated async description",
                allowed_hostnames=["example.com", "api.example.com"],
            )

            assert result is not None
            assert result.name == updated_name
            assert result.description == "Updated async description"

            # Verify update persisted
            info = await network_policy.get_info()
            assert info.name == updated_name
            assert info.description == "Updated async description"
        finally:
            await network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_delete(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test deleting a network policy."""
        network_policy = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-delete"),
            allowed_hostnames=["example.com"],
        )

        result = await network_policy.delete()

        assert result is not None


class TestAsyncNetworkPolicyCreationVariations:
    """Test different async network policy creation scenarios."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_with_allow_all(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a network policy with allow_all enabled."""
        network_policy = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-allow-all"),
            description="Allow all egress traffic",
            allow_all=True,
        )

        try:
            info = await network_policy.get_info()
            assert info.egress is not None
            assert info.egress.allow_all is True
        finally:
            await network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_with_devbox_to_devbox(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a network policy with devbox-to-devbox traffic allowed."""
        network_policy = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-d2d"),
            description="Allow devbox to devbox traffic",
            allow_devbox_to_devbox=True,
            allowed_hostnames=["internal.example.com"],
        )

        try:
            info = await network_policy.get_info()
            assert info.egress is not None
            assert info.egress.allow_devbox_to_devbox is True
        finally:
            await network_policy.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_with_wildcard_hostnames(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a network policy with wildcard hostname patterns."""
        network_policy = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-wildcards"),
            allowed_hostnames=[
                "*.github.com",
                "*.githubusercontent.com",
                "registry.npmjs.org",
                "*.pypi.org",
            ],
        )

        try:
            info = await network_policy.get_info()
            assert info.egress is not None
            assert info.egress.allowed_hostnames is not None
            assert len(info.egress.allowed_hostnames) == 4
        finally:
            await network_policy.delete()


class TestAsyncNetworkPolicyListing:
    """Test async network policy listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_network_policies(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing network policies."""
        policies = await async_sdk_client.network_policy.list(limit=10)

        assert isinstance(policies, list)
        # List might be empty, that's okay
        assert len(policies) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_get_network_policy_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving network policy by ID."""
        # Create a policy
        created = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-retrieve"),
            allowed_hostnames=["example.com"],
        )

        try:
            # Retrieve it by ID
            retrieved = async_sdk_client.network_policy.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same policy
            info = await retrieved.get_info()
            assert info.id == created.id
        finally:
            await created.delete()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_network_policies_with_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing network policies with a limit."""
        # Create two policies
        policy1 = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-list-1"),
            allowed_hostnames=["example1.com"],
        )
        policy2 = await async_sdk_client.network_policy.create(
            name=unique_name("sdk-async-network-policy-list-2"),
            allowed_hostnames=["example2.com"],
        )

        try:
            # List with limit
            policies = await async_sdk_client.network_policy.list(limit=100)

            assert isinstance(policies, list)
            # Should find our policies
            policy_ids = [p.id for p in policies]
            assert policy1.id in policy_ids
            assert policy2.id in policy_ids
        finally:
            await policy1.delete()
            await policy2.delete()
