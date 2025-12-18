"""Comprehensive tests for async AsyncAgent class."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockAgentView
from runloop_api_client.sdk import AsyncAgent


class TestAsyncAgent:
    """Tests for AsyncAgent class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncAgent initialization."""
        agent = AsyncAgent(mock_async_client, "agt_123")
        assert agent.id == "agt_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncAgent string representation."""
        agent = AsyncAgent(mock_async_client, "agt_123")
        assert repr(agent) == "<AsyncAgent id='agt_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, agent_view: MockAgentView) -> None:
        """Test get_info method."""
        mock_async_client.agents.retrieve = AsyncMock(return_value=agent_view)

        agent = AsyncAgent(mock_async_client, "agt_123")
        result = await agent.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == agent_view
        mock_async_client.agents.retrieve.assert_called_once_with(
            "agt_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )
