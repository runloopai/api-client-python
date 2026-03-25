"""Comprehensive tests for sync Axon class."""

from __future__ import annotations

from unittest.mock import Mock

from tests.sdk.conftest import MockAxonView, MockPublishResultView
from runloop_api_client.sdk import Axon


class TestAxon:
    """Tests for Axon class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Axon initialization."""
        axon = Axon(mock_client, "axn_123")
        assert axon.id == "axn_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Axon string representation."""
        axon = Axon(mock_client, "axn_123")
        assert repr(axon) == "<Axon id='axn_123'>"

    def test_get_info(self, mock_client: Mock, axon_view: MockAxonView) -> None:
        """Test get_info method."""
        mock_client.axons.retrieve.return_value = axon_view

        axon = Axon(mock_client, "axn_123")
        result = axon.get_info(
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

        assert result == axon_view
        mock_client.axons.retrieve.assert_called_once_with(
            "axn_123",
            extra_headers={"X-Custom": "value"},
            timeout=30.0,
        )

    def test_publish(self, mock_client: Mock) -> None:
        """Test publish method."""
        mock_result = MockPublishResultView()
        mock_client.axons.publish.return_value = mock_result

        axon = Axon(mock_client, "axn_123")
        result = axon.publish(
            event_type="test",
            origin="USER_EVENT",
            payload="{}",
            source="sdk",
        )

        assert result == mock_result
        mock_client.axons.publish.assert_called_once_with(
            "axn_123",
            event_type="test",
            origin="USER_EVENT",
            payload="{}",
            source="sdk",
        )

    def test_subscribe_sse(self, mock_client: Mock) -> None:
        """Test subscribe_sse method."""
        mock_stream = Mock()
        mock_client.axons.subscribe_sse.return_value = mock_stream

        axon = Axon(mock_client, "axn_123")
        result = axon.subscribe_sse()

        assert result == mock_stream
        mock_client.axons.subscribe_sse.assert_called_once_with("axn_123")
