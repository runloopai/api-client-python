"""Asynchronous SDK smoke tests for Agent operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.types.shared_params import AgentSource

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120
AGENT_VERSION = "1.2.3"


class TestAsyncAgentLifecycle:
    """Test basic async agent lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_agent_create_basic(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a basic agent."""
        name = unique_name("sdk-async-agent-test-basic")
        agent = await async_sdk_client.agent.create(
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
            info = await agent.get_info()
            assert info.id == agent.id
            assert info.name == name
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            # Currently agents don't have a delete method - they persist after tests
            # Once implemented, add: await agent.delete()
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_agent_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving agent information."""
        name = unique_name("sdk-async-agent-test-info")
        agent = await async_sdk_client.agent.create(
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
            info = await agent.get_info()

            assert info.id == agent.id
            assert info.name == name
            assert info.create_time_ms > 0
            assert isinstance(info.is_public, bool)
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass


class TestAsyncAgentListing:
    """Test async agent listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_agents(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing agents."""
        agents = await async_sdk_client.agent.list(limit=10)

        assert isinstance(agents, list)
        # List might be empty, that's okay
        assert len(agents) >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_get_agent_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving agent by ID."""
        # Create an agent
        created = await async_sdk_client.agent.create(
            name=unique_name("sdk-async-agent-test-retrieve"),
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
            retrieved = async_sdk_client.agent.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same agent
            info = await retrieved.get_info()
            assert info.id == created.id
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_multiple_agents(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing multiple agents after creation."""
        source_config: AgentSource = {
            "type": "npm",
            "npm": {
                "package_name": "@runloop/hello-world-agent",
            },
        }

        # Create multiple agents
        agent1 = await async_sdk_client.agent.create(
            name=unique_name("sdk-async-agent-test-list-1"), source=source_config, version=AGENT_VERSION
        )
        agent2 = await async_sdk_client.agent.create(
            name=unique_name("sdk-async-agent-test-list-2"), source=source_config, version=AGENT_VERSION
        )
        agent3 = await async_sdk_client.agent.create(
            name=unique_name("sdk-async-agent-test-list-3"), source=source_config, version=AGENT_VERSION
        )

        try:
            # List agents
            agents = await async_sdk_client.agent.list(limit=100)

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


class TestAsyncAgentCreationVariations:
    """Test different async agent creation scenarios."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_agent_with_source_npm(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating an agent with npm source."""
        name = unique_name("sdk-async-agent-test-npm")

        agent = await async_sdk_client.agent.create(
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
            info = await agent.get_info()
            assert info.name == name
            assert info.source is not None
            assert info.source.type == "npm"
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_agent_with_source_git(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating an agent with git source."""
        name = unique_name("sdk-async-agent-test-git")

        agent = await async_sdk_client.agent.create(
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
            info = await agent.get_info()
            assert info.name == name
            assert info.source is not None
            assert info.source.type == "git"
        finally:
            # TODO: Add agent cleanup once delete endpoint is implemented
            pass
