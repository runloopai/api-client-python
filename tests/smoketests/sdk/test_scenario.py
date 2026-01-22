"""Synchronous SDK smoke tests for Scenario operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK, ScenarioBuilder
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


def push_or_update_scenario(sdk_client: RunloopSDK, builder: ScenarioBuilder) -> ScenarioView:
    """Push a new scenario or update existing one with the same name.

    This is a workaround until scenario delete endpoint is available.
    Uses fixed scenario names to avoid littering the platform with test scenarios.

    When updating an existing scenario, this function will delete the OLD blueprint/snapshot
    that's no longer needed (if different from the new one). The NEW blueprint/snapshot
    is kept so the scenario remains runnable.
    """
    # Check if scenario already exists
    scenarios = sdk_client.scenario.list(name=builder.name, limit=1)

    if scenarios:
        # Get old scenario info to find old blueprint/snapshot IDs
        scenario = scenarios[0]
        env = scenario.get_info().environment
        old_blueprint_id = env.blueprint_id if env else None
        old_snapshot_id = env.snapshot_id if env else None

        # Get new blueprint/snapshot IDs from builder
        new_blueprint_id = builder._blueprint.id if builder._blueprint else None
        new_snapshot_id = builder._snapshot.id if builder._snapshot else None

        # Update existing scenario with builder's params
        params = builder.build()
        result = scenario.update(**filter_params(params, SDKScenarioUpdateParams))

        # Delete OLD blueprint/snapshot if they're being replaced
        if old_blueprint_id and old_blueprint_id != new_blueprint_id:
            sdk_client.blueprint.from_id(old_blueprint_id).delete()

        if old_snapshot_id and old_snapshot_id != new_snapshot_id:
            sdk_client.snapshot.from_id(old_snapshot_id).delete()

        return result
    else:
        # Create new scenario - keep the blueprint/snapshot (scenario needs them)
        scenario = builder.push()
        return scenario.get_info()


class TestScenarioRetrieval:
    """Test scenario retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_list_scenarios(self, sdk_client: RunloopSDK) -> None:
        """Test listing scenarios."""
        scenarios = sdk_client.scenario.list(limit=10)

        assert isinstance(scenarios, list)
        # List might be empty, that's okay
        assert len(scenarios) >= 0


class TestScenarioFromId:
    """Test scenario from_id operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_from_id_get_info(self, sdk_client: RunloopSDK) -> None:
        """Test from_id followed by get_info on an existing scenario."""
        # First list to get an existing scenario
        scenarios = sdk_client.scenario.list(limit=1)
        if not scenarios:
            pytest.skip("No scenarios available to test from_id")

        scenario_id = scenarios[0].id

        # Get scenario by ID
        scenario = sdk_client.scenario.from_id(scenario_id)
        assert scenario.id == scenario_id

        # Verify we can get info
        info = scenario.get_info()
        assert info.id == scenario_id
        assert info.name is not None


class TestScenarioRun:
    """Test scenario run operations."""

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_scenario_run_async_lifecycle(self, sdk_client: RunloopSDK) -> None:
        """Test running a scenario and accessing the devbox.

        This test:
        1. Lists scenarios to find one to run
        2. Starts a scenario run
        3. Waits for environment to be ready
        4. Accesses the devbox
        5. Cancels the run
        """
        # Find a scenario to run
        scenarios = sdk_client.scenario.list(limit=1)
        if not scenarios:
            pytest.skip("No scenarios available to test run")

        # Pick the first scenario
        scenario = scenarios[0]

        # Start a run
        run = scenario.run_async(run_name="sdk-smoketest-run")
        devbox = None

        try:
            assert run.id is not None
            assert run.devbox_id is not None

            # Wait for environment to be ready
            run.await_env_ready()

            # Access devbox
            devbox = run.devbox
            info = devbox.get_info()
            assert info.status == "running"

            # Get run info
            info = run.get_info()
            assert info.id == run.id
            assert info.state in ["running", "scoring", "scored", "completed"]

        finally:
            # Clean up - cancel the run
            try:
                run.cancel()
            except Exception:
                if devbox:
                    devbox.shutdown()

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_scenario_run(self, sdk_client: RunloopSDK) -> None:
        """Test run convenience method."""
        # Find a scenario to run
        scenarios = sdk_client.scenario.list(limit=1)
        if not scenarios:
            pytest.skip("No scenarios available to test run")

        scenario = scenarios[0]

        # Start a run and wait for environment in one call
        run = scenario.run(run_name="sdk-smoketest-await")
        devbox = None

        try:
            assert run.id is not None
            assert run.devbox_id is not None

            # Devbox should be ready
            devbox = run.devbox
            info = devbox.get_info()
            assert info.status == "running"

        finally:
            # Clean up
            try:
                run.cancel()
            except Exception:
                if devbox:
                    devbox.shutdown()


class TestScenarioBuilder:
    """Test ScenarioBuilder operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_scenario_builder_minimal(self, sdk_client: RunloopSDK) -> None:
        """Test creating/updating a minimal scenario with just problem statement and scorer."""
        builder = (
            sdk_client.scenario.builder("sdk-smoketest-builder-minimal")
            .with_problem_statement("Minimal test problem statement")
            .with_metadata(SMOKETEST_METADATA)
            .add_shell_command_scorer("minimal-scorer", command="echo 1.0")
        )

        info = push_or_update_scenario(sdk_client, builder)

        assert info.name == "sdk-smoketest-builder-minimal"
        assert info.input_context.problem_statement == "Minimal test problem statement"
        assert len(info.scoring_contract.scoring_function_parameters) == 1
        assert info.scoring_contract.scoring_function_parameters[0].name == "minimal-scorer"

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_scenario_builder_with_blueprint(self, sdk_client: RunloopSDK) -> None:
        """Test creating/updating a scenario from a blueprint."""
        blueprint = sdk_client.blueprint.create(
            name=unique_name("sdk-smoketest-scenario-bp"),
            dockerfile="FROM ubuntu:22.04",
        )

        builder = (
            sdk_client.scenario.builder("sdk-smoketest-builder-blueprint")
            .from_blueprint(blueprint)
            .with_working_directory("/home/user")
            .with_problem_statement("Blueprint test problem")
            .with_metadata(SMOKETEST_METADATA)
            .add_shell_command_scorer("blueprint-scorer", command="echo 1.0")
        )

        info = push_or_update_scenario(sdk_client, builder)

        assert info.name == "sdk-smoketest-builder-blueprint"
        assert info.input_context.problem_statement == "Blueprint test problem"
        assert info.environment is not None
        assert info.environment.blueprint_id == blueprint.id
        assert info.environment.working_directory == "/home/user"

    @pytest.mark.timeout(TEN_MINUTE_TIMEOUT)
    def test_scenario_builder_with_snapshot(self, sdk_client: RunloopSDK) -> None:
        """Test creating/updating a scenario from a snapshot."""
        # Create blueprint -> devbox -> snapshot chain
        blueprint = sdk_client.blueprint.create(
            name=unique_name("sdk-smoketest-scenario-snap-bp"),
            dockerfile="FROM ubuntu:22.04",
        )
        devbox = sdk_client.devbox.create(blueprint_id=blueprint.id)
        snapshot = devbox.snapshot_disk(name=unique_name("sdk-smoketest-scenario-snap"))

        # Shut down the devbox - it's not needed after creating the snapshot
        try:
            devbox.shutdown()
        except Exception:
            pass

        builder = (
            sdk_client.scenario.builder("sdk-smoketest-builder-snapshot")
            .from_snapshot(snapshot)
            .with_problem_statement("Snapshot test problem")
            .with_metadata(SMOKETEST_METADATA)
            .add_shell_command_scorer("snapshot-scorer", command="echo 1.0")
        )

        info = push_or_update_scenario(sdk_client, builder)

        assert info.name == "sdk-smoketest-builder-snapshot"
        assert info.input_context.problem_statement == "Snapshot test problem"
        assert info.environment is not None
        assert info.environment.snapshot_id == snapshot.id
