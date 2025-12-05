"""Synchronous SDK smoke tests for Scenario operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120
FIVE_MINUTE_TIMEOUT = 300


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
        run = scenario.run_async(run_name="sdk-smoketest-run")

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
        run = scenario.run(run_name="sdk-smoketest-await")

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
