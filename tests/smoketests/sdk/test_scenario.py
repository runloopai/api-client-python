"""Synchronous SDK smoke tests for Scenario operations."""

from __future__ import annotations

import datetime
from typing import Optional

import pytest

from runloop_api_client.sdk import RunloopSDK
from runloop_api_client.sdk.scenario import Scenario

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120
FIVE_MINUTE_TIMEOUT = 300


def find_scenario_by_name(sdk_client: RunloopSDK, name: str) -> Optional[Scenario]:
    """Find an existing scenario by name, returns None if not found."""
    scenarios = sdk_client.scenario.list(limit=100)
    for scenario in scenarios:
        info = scenario.get_info()
        if info.name == name:
            return scenario
    return None


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
    def test_scenario_run_lifecycle(self, sdk_client: RunloopSDK) -> None:
        """Test running a scenario and accessing the devbox.

        This test:
        1. Lists scenarios to find one to run
        2. Starts a scenario run
        3. Waits for environment to be ready
        4. Accesses the devbox
        5. Cancels the run
        """
        # Find a scenario to run
        scenarios = sdk_client.scenario.list(limit=5)
        if not scenarios:
            pytest.skip("No scenarios available to test run")

        # Pick the first scenario
        scenario = scenarios[0]

        # Start a run
        run = scenario.run(run_name="sdk-smoketest-run")

        try:
            assert run.id is not None
            assert run.devbox_id is not None

            # Wait for environment to be ready
            run.await_env_ready()

            # Access devbox
            devbox = run.devbox
            assert devbox.id == run.devbox_id

            # Get run info
            info = run.get_info()
            assert info.id == run.id
            assert info.state in ["running", "scoring", "scored", "completed"]

        finally:
            # Clean up - cancel the run
            try:
                run.cancel()
            except Exception:
                pass  # Best effort cleanup

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_scenario_run_and_await_env_ready(self, sdk_client: RunloopSDK) -> None:
        """Test run_and_await_env_ready convenience method."""
        # Find a scenario to run
        scenarios = sdk_client.scenario.list(limit=5)
        if not scenarios:
            pytest.skip("No scenarios available to test run")

        scenario = scenarios[0]

        # Start a run and wait for environment in one call
        run = scenario.run_and_await_env_ready(run_name="sdk-smoketest-await")

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
                pass


class TestScenarioBuilder:
    """Test scenario builder operations.

    These tests use fixed scenario names and reuse existing scenarios when possible
    to avoid accumulating test scenarios (since scenario deletion is not yet available).
    """

    # Metadata for identifying test scenarios that can be cleaned up later
    CLEANUP_METADATA = {"smoketest": "true", "sdk_smoketest": "true", "cleanup_safe": "true"}

    # Fixed scenario names for reuse across test runs
    BASIC_SCENARIO_NAME = "sdk-smoketest-builder-basic"
    ENV_SCENARIO_NAME = "sdk-smoketest-builder-env"
    FLUENT_SCENARIO_NAME = "sdk-smoketest-builder-fluent"

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_builder_create_scenario(self, sdk_client: RunloopSDK) -> None:
        """Test creating a scenario with the builder.

        Uses a fixed name and reuses existing scenario if found.
        """
        # Check if scenario already exists
        existing = find_scenario_by_name(sdk_client, self.BASIC_SCENARIO_NAME)
        if existing:
            # Scenario exists, update metadata to exercise update path
            updated_metadata = {
                **self.CLEANUP_METADATA,
                "last_smoketest_run": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            existing.update(metadata=updated_metadata)
            info = existing.get_info()
            assert info.name == self.BASIC_SCENARIO_NAME
            assert info.input_context is not None
            return

        # Create new scenario
        builder = sdk_client.scenario.builder(self.BASIC_SCENARIO_NAME)
        builder.with_problem_statement("This is a test scenario created by the SDK builder smoke test.")
        builder.add_bash_scorer(
            "test-scorer",
            bash_script="echo 'score=1.0'",
            weight=1.0,
        )
        builder.with_metadata(self.CLEANUP_METADATA)

        scenario = builder.push()

        assert scenario.id is not None
        info = scenario.get_info()
        assert info.name == self.BASIC_SCENARIO_NAME
        assert info.input_context is not None

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_builder_with_environment(self, sdk_client: RunloopSDK) -> None:
        """Test creating a scenario with environment configuration.

        Uses a fixed name and reuses existing scenario if found.
        """
        # Check if scenario already exists
        existing = find_scenario_by_name(sdk_client, self.ENV_SCENARIO_NAME)
        if existing:
            # Update metadata to exercise update path
            updated_metadata = {
                **self.CLEANUP_METADATA,
                "last_smoketest_run": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            existing.update(metadata=updated_metadata)
            info = existing.get_info()
            assert info.name == self.ENV_SCENARIO_NAME
            return

        # Get a blueprint to use
        blueprints = sdk_client.blueprint.list(limit=1)
        if not blueprints:
            pytest.skip("No blueprints available for environment test")

        blueprint_id = blueprints[0].id

        builder = (
            sdk_client.scenario.builder(self.ENV_SCENARIO_NAME)
            .from_blueprint_id(blueprint_id)
            .with_working_directory("/workspace")
            .with_problem_statement("Test scenario with environment configuration.")
            .add_command_scorer("check", command="echo 'score=1.0'", weight=1.0)
            .with_metadata(self.CLEANUP_METADATA)
        )

        scenario = builder.push()

        info = scenario.get_info()
        assert info.name == self.ENV_SCENARIO_NAME
        if info.environment:
            assert info.environment.blueprint_id == blueprint_id

    @pytest.mark.timeout(FIVE_MINUTE_TIMEOUT)
    def test_builder_fluent_api(self, sdk_client: RunloopSDK) -> None:
        """Test builder fluent API chaining.

        Uses a fixed name and reuses existing scenario if found.
        """
        # Check if scenario already exists
        existing = find_scenario_by_name(sdk_client, self.FLUENT_SCENARIO_NAME)
        if existing:
            # Update metadata to exercise update path
            updated_metadata = {
                **self.CLEANUP_METADATA,
                "last_smoketest_run": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "test_type": "fluent_api",
            }
            existing.update(metadata=updated_metadata)
            info = existing.get_info()
            assert info.name == self.FLUENT_SCENARIO_NAME
            if info.scoring_contract and info.scoring_contract.scoring_function_parameters:
                assert len(info.scoring_contract.scoring_function_parameters) == 2
            return

        # Create new scenario with fluent API
        scenario = (
            sdk_client.scenario.builder(self.FLUENT_SCENARIO_NAME)
            .with_problem_statement("Fluent API test scenario.")
            .with_additional_context({"hint": "This is a hint"})
            .add_bash_scorer("scorer1", bash_script="echo 'score=0.5'", weight=1.0)
            .add_command_scorer("scorer2", command="echo 'score=1.0'", weight=2.0)
            .with_metadata({**self.CLEANUP_METADATA, "test_type": "fluent_api"})
            .push()
        )

        info = scenario.get_info()
        assert info.name == self.FLUENT_SCENARIO_NAME
        if info.scoring_contract and info.scoring_contract.scoring_function_parameters:
            assert len(info.scoring_contract.scoring_function_parameters) == 2
