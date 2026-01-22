"""Asynchronous SDK smoke tests for Scenario operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK, AsyncScenarioBuilder
from tests.smoketests.utils import unique_name
from runloop_api_client.types import ScenarioView
from runloop_api_client.sdk._types import SDKScenarioUpdateParams
from runloop_api_client.sdk._helpers import filter_params

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120
FIVE_MINUTE_TIMEOUT = 300
TEN_MINUTE_TIMEOUT = 600

# Metadata tag for all smoketest scenarios (for easy identification/cleanup)
SMOKETEST_METADATA = {"smoketest": "true"}


async def push_or_update_scenario(sdk_client: AsyncRunloopSDK, builder: AsyncScenarioBuilder) -> ScenarioView:
    """Push a new scenario or update existing one with the same name.

    This is a workaround until scenario delete endpoint is available.
    Uses fixed scenario names to avoid littering the platform with test scenarios.

    When updating an existing scenario, this function will delete the OLD blueprint/snapshot
    that's no longer needed (if different from the new one). The NEW blueprint/snapshot
    is kept so the scenario remains runnable.
    """
    # Check if scenario already exists
    scenarios = await sdk_client.scenario.list(name=builder.name, limit=1)

    if scenarios:
        # Get old scenario info to find old blueprint/snapshot IDs
        scenario = scenarios[0]
        old_scenario_info = await scenario.get_info()
        old_env = old_scenario_info.environment
        old_blueprint_id = old_env.blueprint_id if old_env else None
        old_snapshot_id = old_env.snapshot_id if old_env else None

        # Get new blueprint/snapshot IDs from builder
        new_blueprint_id = builder._blueprint.id if builder._blueprint else None
        new_snapshot_id = builder._snapshot.id if builder._snapshot else None

        # Update existing scenario with builder's params
        params = builder.build()
        result = await scenario.update(**filter_params(params, SDKScenarioUpdateParams))

        # Delete OLD blueprint/snapshot if they're being replaced
        if old_blueprint_id and old_blueprint_id != new_blueprint_id:
            await sdk_client.blueprint.from_id(old_blueprint_id).delete()

        if old_snapshot_id and old_snapshot_id != new_snapshot_id:
            await sdk_client.snapshot.from_id(old_snapshot_id).delete()

        return result
    else:
        # Create new scenario - keep the blueprint/snapshot (scenario needs them)
        scenario = await builder.push()
        return await scenario.get_info()


class TestAsyncScenarioRetrieval:
    """Test async scenario retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_list_scenarios(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing scenarios."""
        scenarios = await async_sdk_client.scenario.list(limit=10)

        assert isinstance(scenarios, list)
        # List might be empty, that's okay
        assert len(scenarios) >= 0


class TestAsyncScenarioFromId:
    """Test async scenario from_id operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_from_id_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test from_id followed by get_info on an existing scenario."""
        # First list to get an existing scenario
        scenarios = await async_sdk_client.scenario.list(limit=1)
        if not scenarios:
            pytest.skip("No scenarios available to test from_id")

        scenario_id = scenarios[0].id

        # Get scenario by ID
        scenario = async_sdk_client.scenario.from_id(scenario_id)
        assert scenario.id == scenario_id

        # Verify we can get info
        info = await scenario.get_info()
        assert info.id == scenario_id
        assert info.name is not None


class TestAsyncScenarioRun:
    """Test async scenario run operations."""

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    async def test_scenario_run_async_lifecycle(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test running a scenario and accessing the devbox.

        This test:
        1. Lists scenarios to find one to run
        2. Starts a scenario run
        3. Waits for environment to be ready
        4. Accesses the devbox
        5. Cancels the run
        """
        # Find a scenario to run
        scenarios = await async_sdk_client.scenario.list(limit=1)
        if not scenarios:
            pytest.skip("No scenarios available to test run")

        # Pick the first scenario
        scenario = scenarios[0]

        # Start a run
        run = await scenario.run_async(run_name="sdk-smoketest-async-run")
        devbox = None

        try:
            assert run.id is not None
            assert run.devbox_id is not None

            # Wait for environment to be ready
            await run.await_env_ready()

            # Access devbox
            devbox = run.devbox
            info = await devbox.get_info()
            assert info.status == "running"

            # Get run info
            info = await run.get_info()
            assert info.id == run.id
            assert info.state in ["running", "scoring", "scored", "completed"]

        finally:
            # Clean up - cancel the run
            try:
                await run.cancel()
            except Exception:
                if devbox:
                    await devbox.shutdown()

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    async def test_scenario_run(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test run convenience method."""
        # Find a scenario to run
        scenarios = await async_sdk_client.scenario.list(limit=1)
        if not scenarios:
            pytest.skip("No scenarios available to test run")

        scenario = scenarios[0]

        # Start a run and wait for environment in one call
        run = await scenario.run(run_name="sdk-smoketest-async-await")
        devbox = None

        try:
            assert run.id is not None
            assert run.devbox_id is not None

            # Devbox should be ready
            devbox = run.devbox
            info = await devbox.get_info()
            assert info.status == "running"

        finally:
            # Clean up
            try:
                await run.cancel()
            except Exception:
                if devbox:
                    await devbox.shutdown()


class TestAsyncScenarioBuilder:
    """Test AsyncScenarioBuilder operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_scenario_builder_minimal(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating/updating a minimal scenario with just problem statement and scorer."""
        builder = (
            async_sdk_client.scenario.builder("sdk-smoketest-async-builder-minimal")
            .with_problem_statement("Async minimal test problem statement")
            .with_metadata(SMOKETEST_METADATA)
            .add_shell_command_scorer("async-minimal-scorer", command="echo 1.0")
        )

        info = await push_or_update_scenario(async_sdk_client, builder)

        assert info.name == "sdk-smoketest-async-builder-minimal"
        assert info.input_context.problem_statement == "Async minimal test problem statement"
        assert len(info.scoring_contract.scoring_function_parameters) == 1
        assert info.scoring_contract.scoring_function_parameters[0].name == "async-minimal-scorer"

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    async def test_scenario_builder_with_blueprint(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating/updating a scenario from a blueprint."""
        blueprint = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-smoketest-async-scenario-bp"),
            dockerfile="FROM ubuntu:22.04",
        )

        builder = (
            async_sdk_client.scenario.builder("sdk-smoketest-async-builder-blueprint")
            .from_blueprint(blueprint)
            .with_working_directory("/home/user")
            .with_problem_statement("Async blueprint test problem")
            .with_metadata(SMOKETEST_METADATA)
            .add_shell_command_scorer("async-blueprint-scorer", command="echo 1.0")
        )

        info = await push_or_update_scenario(async_sdk_client, builder)

        assert info.name == "sdk-smoketest-async-builder-blueprint"
        assert info.input_context.problem_statement == "Async blueprint test problem"
        assert info.environment is not None
        assert info.environment.blueprint_id == blueprint.id
        assert info.environment.working_directory == "/home/user"

    @pytest.mark.timeout(TEN_MINUTE_TIMEOUT)
    async def test_scenario_builder_with_snapshot(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating/updating a scenario from a snapshot."""
        # Create blueprint -> devbox -> snapshot chain
        blueprint = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-smoketest-async-scenario-snap-bp"),
            dockerfile="FROM ubuntu:22.04",
        )
        devbox = await async_sdk_client.devbox.create(blueprint_id=blueprint.id)
        snapshot = await devbox.snapshot_disk(name=unique_name("sdk-smoketest-async-scenario-snap"))

        # Shut down the devbox - it's not needed after creating the snapshot
        try:
            await devbox.shutdown()
        except Exception:
            pass

        builder = (
            async_sdk_client.scenario.builder("sdk-smoketest-async-builder-snapshot")
            .from_snapshot(snapshot)
            .with_problem_statement("Async snapshot test problem")
            .with_metadata(SMOKETEST_METADATA)
            .add_shell_command_scorer("async-snapshot-scorer", command="echo 1.0")
        )

        info = await push_or_update_scenario(async_sdk_client, builder)

        assert info.name == "sdk-smoketest-async-builder-snapshot"
        assert info.input_context.problem_statement == "Async snapshot test problem"
        assert info.environment is not None
        assert info.environment.snapshot_id == snapshot.id
