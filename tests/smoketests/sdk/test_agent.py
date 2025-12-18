"""Synchronous SDK smoke tests for Agent operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.types.shared_params import AgentSource

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120
AGENT_VERSION = "1.2.3"


class TestAgentLifecycle:
    """Test basic agent lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_agent_create_basic(self, sdk_client: RunloopSDK) -> None:
        """Test creating a basic agent."""
        name = unique_name("sdk-agent-test-basic")
        agent = sdk_client.agent.create(
            name=name,
            version=AGENT_VERSION,
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/hello-world-agent",
                },
            },
        )

        try:
            assert agent is not None
            assert agent.id is not None
            assert len(agent.id) > 0

            # Verify agent information
            info = agent.get_info()
            assert info.id == agent.id
            assert info.name == name
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            # Currently agents don't have a delete method - they persist after tests
            # Once implemented, add: agent.delete()
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_agent_get_info(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving agent information."""
        name = unique_name("sdk-agent-test-info")
        agent = sdk_client.agent.create(
            name=name,
            version=AGENT_VERSION,
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/hello-world-agent",
                },
            },
        )

        try:
            info = agent.get_info()

            assert info.id == agent.id
            assert info.name == name
            assert info.create_time_ms > 0
            assert isinstance(info.is_public, bool)
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass


class TestAgentListing:
    """Test agent listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_agents(self, sdk_client: RunloopSDK) -> None:
        """Test listing agents."""
        agents = sdk_client.agent.list(limit=10)

        assert isinstance(agents, list)
        # List might be empty, that's okay
        assert len(agents) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_get_agent_by_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving agent by ID."""
        # Create an agent
        created = sdk_client.agent.create(
            name=unique_name("sdk-agent-test-retrieve"),
            version=AGENT_VERSION,
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/hello-world-agent",
                },
            },
        )

        try:
            # Retrieve it by ID
            retrieved = sdk_client.agent.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same agent
            info = retrieved.get_info()
            assert info.id == created.id
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_multiple_agents(self, sdk_client: RunloopSDK) -> None:
        """Test listing multiple agents after creation."""
        source_config: AgentSource = {
            "type": "npm",
            "npm": {
                "package_name": "@runloop/hello-world-agent",
            },
        }

        # Create multiple agents
        agent1 = sdk_client.agent.create(
            name=unique_name("sdk-agent-test-list-1"), source=source_config, version=AGENT_VERSION
        )
        agent2 = sdk_client.agent.create(
            name=unique_name("sdk-agent-test-list-2"), source=source_config, version=AGENT_VERSION
        )
        agent3 = sdk_client.agent.create(
            name=unique_name("sdk-agent-test-list-3"), source=source_config, version=AGENT_VERSION
        )

        try:
            # List agents
            agents = sdk_client.agent.list(limit=100)

            assert isinstance(agents, list)
            assert len(agents) >= 3

            # Verify our agents are in the list
            agent_ids = [a.id for a in agents]
            assert agent1.id in agent_ids
            assert agent2.id in agent_ids
            assert agent3.id in agent_ids
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            # Should delete: agent1, agent2, agent3
            pass


class TestAgentCreationVariations:
    """Test different agent creation scenarios."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_agent_with_source_npm(self, sdk_client: RunloopSDK) -> None:
        """Test creating an agent with npm source."""
        name = unique_name("sdk-agent-test-npm")

        agent = sdk_client.agent.create(
            name=name,
            version=AGENT_VERSION,
            source={
                "type": "npm",
                "npm": {
                    "package_name": "@runloop/example-agent",
                },
            },
        )

        try:
            assert agent.id is not None
            info = agent.get_info()
            assert info.name == name
            assert info.source is not None
            assert info.source.type == "npm"
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_agent_with_source_git(self, sdk_client: RunloopSDK) -> None:
        """Test creating an agent with git source."""
        name = unique_name("sdk-agent-test-git")

        agent = sdk_client.agent.create(
            name=name,
            version=AGENT_VERSION,
            source={
                "type": "git",
                "git": {
                    "repository": "https://github.com/runloop/example-agent",
                    "ref": "main",
                },
            },
        )

        try:
            assert agent.id is not None
            info = agent.get_info()
            assert info.name == name
            assert info.source is not None
            assert info.source.type == "git"
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass
