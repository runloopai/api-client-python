"""Comprehensive tests for async NetworkPolicy class."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockNetworkPolicyView
from runloop_api_client.sdk import AsyncNetworkPolicy


class TestAsyncNetworkPolicy:
    """Tests for AsyncNetworkPolicy class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncNetworkPolicy initialization."""
        network_policy = AsyncNetworkPolicy(mock_async_client, "np_123")
        assert network_policy.id == "np_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncNetworkPolicy string representation."""
        network_policy = AsyncNetworkPolicy(mock_async_client, "np_123")
        assert repr(network_policy) == "<AsyncNetworkPolicy id='np_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test get_info method."""
        mock_async_client.network_policies.retrieve = AsyncMock(return_value=network_policy_view)

        network_policy = AsyncNetworkPolicy(mock_async_client, "np_123")
        result = await network_policy.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == network_policy_view
        mock_async_client.network_policies.retrieve.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update(self, mock_async_client: AsyncMock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test update method."""
        mock_async_client.network_policies.update = AsyncMock(return_value=network_policy_view)

        network_policy = AsyncNetworkPolicy(mock_async_client, "np_123")
        result = await network_policy.update(
            name="updated-policy",
            description="Updated description",
            allowed_hostnames=["api.openai.com"],
            allow_all=False,
            allow_devbox_to_devbox=True,
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

        assert result == network_policy_view
        mock_async_client.network_policies.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_partial(
        self, mock_async_client: AsyncMock, network_policy_view: MockNetworkPolicyView
    ) -> None:
        """Test update method with partial fields."""
        mock_async_client.network_policies.update = AsyncMock(return_value=network_policy_view)

        network_policy = AsyncNetworkPolicy(mock_async_client, "np_123")
        result = await network_policy.update(
            name="renamed-policy",
        )

        assert result == network_policy_view
        mock_async_client.network_policies.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_delete(self, mock_async_client: AsyncMock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test delete method."""
        mock_async_client.network_policies.delete = AsyncMock(return_value=network_policy_view)

        network_policy = AsyncNetworkPolicy(mock_async_client, "np_123")
        result = await network_policy.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == network_policy_view
        mock_async_client.network_policies.delete.assert_awaited_once()
