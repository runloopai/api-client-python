"""Comprehensive tests for sync Agent class."""

from __future__ import annotations

from unittest.mock import Mock

from tests.sdk.conftest import MockAgentView
from runloop_api_client.sdk import Agent


class TestAgent:
    """Tests for Agent class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Agent initialization."""
        agent = Agent(mock_client, "agt_123")
        assert agent.id == "agt_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Agent string representation."""
        agent = Agent(mock_client, "agt_123")
        assert repr(agent) == "<Agent id='agt_123'>"

    def test_get_info(self, mock_client: Mock, agent_view: MockAgentView) -> None:
        """Test get_info method."""
        mock_client.agents.retrieve.return_value = agent_view

        agent = Agent(mock_client, "agt_123")
        result = agent.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == agent_view
        mock_client.agents.retrieve.assert_called_once_with(
            "agt_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )
