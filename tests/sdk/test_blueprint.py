"""Comprehensive tests for sync Blueprint class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import MockDevboxView, MockBlueprintView
from runloop_api_client.sdk import Blueprint


class TestBlueprint:
    """Tests for Blueprint class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Blueprint initialization."""
        blueprint = Blueprint(mock_client, "bp_123")
        assert blueprint.id == "bp_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Blueprint string representation."""
        blueprint = Blueprint(mock_client, "bp_123")
        assert repr(blueprint) == "<Blueprint id='bp_123'>"

    def test_get_info(self, mock_client: Mock, blueprint_view: MockBlueprintView) -> None:
        """Test get_info method."""
        mock_client.blueprints.retrieve.return_value = blueprint_view

        blueprint = Blueprint(mock_client, "bp_123")
        result = blueprint.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == blueprint_view
        mock_client.blueprints.retrieve.assert_called_once_with(
            "bp_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_logs(self, mock_client: Mock) -> None:
        """Test logs method."""
        logs_view = SimpleNamespace(logs=[])
        mock_client.blueprints.logs.return_value = logs_view

        blueprint = Blueprint(mock_client, "bp_123")
        result = blueprint.logs(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == logs_view
        mock_client.blueprints.logs.assert_called_once_with(
            "bp_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_delete(self, mock_client: Mock) -> None:
        """Test delete method."""
        mock_client.blueprints.delete.return_value = object()

        blueprint = Blueprint(mock_client, "bp_123")
        result = blueprint.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result is not None  # Verify return value is propagated
        mock_client.blueprints.delete.assert_called_once_with(
            "bp_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_create_devbox(self, mock_client: Mock, devbox_view: MockDevboxView) -> None:
        """Test create_devbox method."""
        mock_client.devboxes.create_and_await_running.return_value = devbox_view

        blueprint = Blueprint(mock_client, "bp_123")
        devbox = blueprint.create_devbox(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=None,
            extra_headers={"X-Custom": "value"},
        )

        assert devbox.id == "dev_123"
        mock_client.devboxes.create_and_await_running.assert_called_once()
        call_kwargs = mock_client.devboxes.create_and_await_running.call_args[1]
        assert call_kwargs["blueprint_id"] == "bp_123"
        assert call_kwargs["name"] == "test-devbox"
        assert call_kwargs["metadata"] == {"key": "value"}
