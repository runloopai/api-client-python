"""Comprehensive tests for sync NetworkPolicy class."""

from __future__ import annotations

from unittest.mock import Mock

from tests.sdk.conftest import MockNetworkPolicyView
from runloop_api_client.sdk import NetworkPolicy


class TestNetworkPolicy:
    """Tests for NetworkPolicy class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test NetworkPolicy initialization."""
        network_policy = NetworkPolicy(mock_client, "np_123")
        assert network_policy.id == "np_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test NetworkPolicy string representation."""
        network_policy = NetworkPolicy(mock_client, "np_123")
        assert repr(network_policy) == "<NetworkPolicy id='np_123'>"

    def test_get_info(self, mock_client: Mock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test get_info method."""
        mock_client.network_policies.retrieve.return_value = network_policy_view

        network_policy = NetworkPolicy(mock_client, "np_123")
        result = network_policy.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == network_policy_view
        mock_client.network_policies.retrieve.assert_called_once_with(
            "np_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_update(self, mock_client: Mock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test update method."""
        mock_client.network_policies.update.return_value = network_policy_view

        network_policy = NetworkPolicy(mock_client, "np_123")
        result = network_policy.update(
            name="updated-policy",
            description="Updated description",
            allowed_hostnames=["api.openai.com"],
            allow_all=False,
            allow_devbox_to_devbox=True,
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

        assert result == network_policy_view
        mock_client.network_policies.update.assert_called_once_with(
            "np_123",
            allow_all=False,
            allow_devbox_to_devbox=True,
            allowed_hostnames=["api.openai.com"],
            description="Updated description",
            name="updated-policy",
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

    def test_update_partial(self, mock_client: Mock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test update method with partial fields."""
        mock_client.network_policies.update.return_value = network_policy_view

        network_policy = NetworkPolicy(mock_client, "np_123")
        result = network_policy.update(
            name="renamed-policy",
        )

        assert result == network_policy_view
        mock_client.network_policies.update.assert_called_once_with(
            "np_123",
            name="renamed-policy",
        )

    def test_delete(self, mock_client: Mock, network_policy_view: MockNetworkPolicyView) -> None:
        """Test delete method."""
        mock_client.network_policies.delete.return_value = network_policy_view

        network_policy = NetworkPolicy(mock_client, "np_123")
        result = network_policy.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == network_policy_view
        mock_client.network_policies.delete.assert_called_once_with(
            "np_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )
