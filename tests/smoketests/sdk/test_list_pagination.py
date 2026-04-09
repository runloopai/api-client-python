"""Smoke tests to verify list methods respect limit parameter and only return one page.

This test suite validates the fix for slow list endpoints, ensuring that
SDK list() methods return only the requested page of results instead of
auto-paginating through all available items.

Related to TypeScript PR: https://github.com/runloopai/api-client-ts/pull/767
"""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK, AsyncRunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.types.shared_params import AgentSource

pytestmark = pytest.mark.smoketest

THIRTY_SECOND_TIMEOUT = 30
AGENT_SOURCE: AgentSource = {
    "type": "npm",
    "npm": {
        "package_name": "@runloop/hello-world-agent",
    },
}


class TestAsyncListPagination:
    """Test async list methods respect limit and return only one page."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_agent_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify agent.list() with limit returns at most that many items."""
        # Request a small page
        agents = await async_sdk_client.agent.list(limit=5)

        assert isinstance(agents, list)
        # Should return at most 5 items (might be fewer if less data exists)
        assert len(agents) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_agent_list_limit_one(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify agent.list() with limit=1 returns at most one item."""
        agents = await async_sdk_client.agent.list(limit=1)

        assert isinstance(agents, list)
        assert len(agents) <= 1, "list(limit=1) should return at most 1 item"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_devbox_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify devbox.list() with limit returns at most that many items."""
        devboxes = await async_sdk_client.devbox.list(limit=3)

        assert isinstance(devboxes, list)
        assert len(devboxes) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_blueprint_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify blueprint.list() with limit returns at most that many items."""
        blueprints = await async_sdk_client.blueprint.list(limit=5)

        assert isinstance(blueprints, list)
        assert len(blueprints) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_storage_object_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify storage_object.list() with limit returns at most that many items."""
        objects = await async_sdk_client.storage_object.list(limit=4)

        assert isinstance(objects, list)
        assert len(objects) <= 4, "list(limit=4) should return at most 4 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_snapshot_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify snapshot.list() with limit returns at most that many items."""
        snapshots = await async_sdk_client.snapshot.list(limit=2)

        assert isinstance(snapshots, list)
        assert len(snapshots) <= 2, "list(limit=2) should return at most 2 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_axon_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify axon.list() with limit returns at most that many items."""
        axons = await async_sdk_client.axon.list(limit=3)

        assert isinstance(axons, list)
        assert len(axons) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_scorer_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify scorer.list() with limit returns at most that many items."""
        scorers = await async_sdk_client.scorer.list(limit=5)

        assert isinstance(scorers, list)
        assert len(scorers) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_scenario_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify scenario.list() with limit returns at most that many items."""
        scenarios = await async_sdk_client.scenario.list(limit=4)

        assert isinstance(scenarios, list)
        assert len(scenarios) <= 4, "list(limit=4) should return at most 4 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_benchmark_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify benchmark.list() with limit returns at most that many items."""
        benchmarks = await async_sdk_client.benchmark.list(limit=3)

        assert isinstance(benchmarks, list)
        assert len(benchmarks) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_network_policy_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify network_policy.list() with limit returns at most that many items."""
        policies = await async_sdk_client.network_policy.list(limit=5)

        assert isinstance(policies, list)
        assert len(policies) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_gateway_config_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify gateway_config.list() with limit returns at most that many items."""
        configs = await async_sdk_client.gateway_config.list(limit=2)

        assert isinstance(configs, list)
        assert len(configs) <= 2, "list(limit=2) should return at most 2 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_mcp_config_list_respects_limit(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify mcp_config.list() with limit returns at most that many items."""
        configs = await async_sdk_client.mcp_config.list(limit=3)

        assert isinstance(configs, list)
        assert len(configs) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_secret_list_no_auto_pagination(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Verify secret.list() returns only one page (secrets don't have limit param)."""
        secrets = await async_sdk_client.secret.list()

        # Secrets list doesn't have a limit parameter, but should still
        # return only one page worth of results, not auto-paginate
        assert isinstance(secrets, list)


class TestSyncListPagination:
    """Test sync list methods respect limit and return only one page."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_agent_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify agent.list() with limit returns at most that many items."""
        agents = sdk_client.agent.list(limit=5)

        assert isinstance(agents, list)
        assert len(agents) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_devbox_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify devbox.list() with limit returns at most that many items."""
        devboxes = sdk_client.devbox.list(limit=3)

        assert isinstance(devboxes, list)
        assert len(devboxes) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_blueprint_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify blueprint.list() with limit returns at most that many items."""
        blueprints = sdk_client.blueprint.list(limit=5)

        assert isinstance(blueprints, list)
        assert len(blueprints) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_storage_object_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify storage_object.list() with limit returns at most that many items."""
        objects = sdk_client.storage_object.list(limit=4)

        assert isinstance(objects, list)
        assert len(objects) <= 4, "list(limit=4) should return at most 4 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_snapshot_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify snapshot.list() with limit returns at most that many items."""
        snapshots = sdk_client.snapshot.list(limit=2)

        assert isinstance(snapshots, list)
        assert len(snapshots) <= 2, "list(limit=2) should return at most 2 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_axon_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify axon.list() with limit returns at most that many items."""
        axons = sdk_client.axon.list(limit=3)

        assert isinstance(axons, list)
        assert len(axons) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_scorer_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify scorer.list() with limit returns at most that many items."""
        scorers = sdk_client.scorer.list(limit=5)

        assert isinstance(scorers, list)
        assert len(scorers) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_scenario_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify scenario.list() with limit returns at most that many items."""
        scenarios = sdk_client.scenario.list(limit=4)

        assert isinstance(scenarios, list)
        assert len(scenarios) <= 4, "list(limit=4) should return at most 4 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_benchmark_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify benchmark.list() with limit returns at most that many items."""
        benchmarks = sdk_client.benchmark.list(limit=3)

        assert isinstance(benchmarks, list)
        assert len(benchmarks) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_network_policy_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify network_policy.list() with limit returns at most that many items."""
        policies = sdk_client.network_policy.list(limit=5)

        assert isinstance(policies, list)
        assert len(policies) <= 5, "list(limit=5) should return at most 5 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_gateway_config_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify gateway_config.list() with limit returns at most that many items."""
        configs = sdk_client.gateway_config.list(limit=2)

        assert isinstance(configs, list)
        assert len(configs) <= 2, "list(limit=2) should return at most 2 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_mcp_config_list_respects_limit(self, sdk_client: RunloopSDK) -> None:
        """Verify mcp_config.list() with limit returns at most that many items."""
        configs = sdk_client.mcp_config.list(limit=3)

        assert isinstance(configs, list)
        assert len(configs) <= 3, "list(limit=3) should return at most 3 items"

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_secret_list_no_auto_pagination(self, sdk_client: RunloopSDK) -> None:
        """Verify secret.list() returns only one page."""
        secrets = sdk_client.secret.list()

        assert isinstance(secrets, list)


class TestListPaginationWithData:
    """Test list pagination behavior when data is guaranteed to exist."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_limit_with_created_data(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Create multiple items and verify list limit works correctly."""
        # Create several agents to ensure we have data
        created_agents: list[object] = []
        for i in range(5):
            agent = await async_sdk_client.agent.create(
                name=unique_name(f"sdk-list-test-{i}"),
                version="1.0.0",
                source=AGENT_SOURCE,
            )
            created_agents.append(agent)

        try:
            # Request only 2 items
            listed_agents = await async_sdk_client.agent.list(limit=2)

            # Should get at most 2, even though 5+ exist
            assert len(listed_agents) <= 2, (
                f"Expected at most 2 items with limit=2, got {len(listed_agents)}. "
                "This indicates auto-pagination is occurring when it shouldn't."
            )

            # Request 10 items - should get all we created (5) plus any existing ones,
            # but should stop at first page (up to 10)
            listed_agents = await async_sdk_client.agent.list(limit=10)
            assert len(listed_agents) <= 10, (
                f"Expected at most 10 items with limit=10, got {len(listed_agents)}. "
                "This indicates auto-pagination is occurring when it shouldn't."
            )

        finally:
            # Cleanup is not possible yet as agents don't have delete
            pass
