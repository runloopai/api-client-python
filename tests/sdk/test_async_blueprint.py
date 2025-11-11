"""Comprehensive tests for async Blueprint class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockDevboxView, MockBlueprintView
from runloop_api_client.sdk import AsyncBlueprint


class TestAsyncBlueprint:
    """Tests for AsyncBlueprint class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBlueprint initialization."""
        blueprint = AsyncBlueprint(mock_async_client, "bp_123")
        assert blueprint.id == "bp_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBlueprint string representation."""
        blueprint = AsyncBlueprint(mock_async_client, "bp_123")
        assert repr(blueprint) == "<AsyncBlueprint id='bp_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, blueprint_view: MockBlueprintView) -> None:
        """Test get_info method."""
        mock_async_client.blueprints.retrieve = AsyncMock(return_value=blueprint_view)

        blueprint = AsyncBlueprint(mock_async_client, "bp_123")
        result = await blueprint.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == blueprint_view
        mock_async_client.blueprints.retrieve.assert_called_once()

    @pytest.mark.asyncio
    async def test_logs(self, mock_async_client: AsyncMock) -> None:
        """Test logs method."""
        logs_view = SimpleNamespace(logs=[])
        mock_async_client.blueprints.logs = AsyncMock(return_value=logs_view)

        blueprint = AsyncBlueprint(mock_async_client, "bp_123")
        result = await blueprint.logs(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == logs_view
        mock_async_client.blueprints.logs.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete(self, mock_async_client: AsyncMock) -> None:
        """Test delete method."""
        mock_async_client.blueprints.delete = AsyncMock(return_value=object())

        blueprint = AsyncBlueprint(mock_async_client, "bp_123")
        result = await blueprint.delete(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result is not None  # Verify return value is propagated
        mock_async_client.blueprints.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_devbox(self, mock_async_client: AsyncMock, devbox_view: MockDevboxView) -> None:
        """Test create_devbox method."""
        mock_async_client.devboxes.create_and_await_running = AsyncMock(return_value=devbox_view)

        blueprint = AsyncBlueprint(mock_async_client, "bp_123")
        devbox = await blueprint.create_devbox(
            name="test-devbox",
            metadata={"key": "value"},
            polling_config=None,
            extra_headers={"X-Custom": "value"},
        )

        assert devbox.id == "dev_123"
        mock_async_client.devboxes.create_and_await_running.assert_called_once()
