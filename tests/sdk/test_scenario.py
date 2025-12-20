"""Comprehensive tests for sync Scenario class."""

from __future__ import annotations

from unittest.mock import Mock

from tests.sdk.conftest import MockScenarioView, MockScenarioRunView
from runloop_api_client.sdk import Scenario


class TestScenario:
    """Tests for Scenario class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Scenario initialization."""
        scenario = Scenario(mock_client, "scn_123")
        assert scenario.id == "scn_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Scenario string representation."""
        scenario = Scenario(mock_client, "scn_123")
        assert repr(scenario) == "<Scenario id='scn_123'>"

    def test_get_info(self, mock_client: Mock, scenario_view: MockScenarioView) -> None:
        """Test get_info method."""
        mock_client.scenarios.retrieve.return_value = scenario_view

        scenario = Scenario(mock_client, "scn_123")
        result = scenario.get_info()

        assert result == scenario_view
        mock_client.scenarios.retrieve.assert_called_once_with("scn_123")

    def test_update(self, mock_client: Mock, scenario_view: MockScenarioView) -> None:
        """Test update method."""
        mock_client.scenarios.update.return_value = scenario_view

        scenario = Scenario(mock_client, "scn_123")
        result = scenario.update(
            name="updated-scenario",
            metadata={"env": "test"},
            environment_parameters={
                "blueprint_id": "bp_456",
            },
            input_context={
                "problem_statement": "Updated problem statement",
            },
            reference_output="--- a/main.py\n+++ b/main.py\n@@ -1 +1 @@\n-old\n+new",
            required_environment_variables=["API_KEY", "DEBUG"],
            required_secret_names=["DB_PASSWORD", "JWT_SECRET"],
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "test-scorer",
                        "scorer": {
                            "type": "command_scorer",
                            "command": "echo 'score=1.0'",
                        },
                        "weight": 1.0,
                    }
                ],
            },
            validation_type="FORWARD",
        )

        assert result == scenario_view
        mock_client.scenarios.update.assert_called_once_with(
            "scn_123",
            name="updated-scenario",
            metadata={"env": "test"},
            environment_parameters={
                "blueprint_id": "bp_456",
            },
            input_context={
                "problem_statement": "Updated problem statement",
            },
            reference_output="--- a/main.py\n+++ b/main.py\n@@ -1 +1 @@\n-old\n+new",
            required_environment_variables=["API_KEY", "DEBUG"],
            required_secret_names=["DB_PASSWORD", "JWT_SECRET"],
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "test-scorer",
                        "scorer": {
                            "type": "command_scorer",
                            "command": "echo 'score=1.0'",
                        },
                        "weight": 1.0,
                    }
                ],
            },
            validation_type="FORWARD",
        )

    def test_run_async(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run_async method returns ScenarioRun wrapper."""
        mock_client.scenarios.start_run.return_value = scenario_run_view

        scenario = Scenario(mock_client, "scn_123")
        run = scenario.run_async(run_name="test-run")

        assert run.id == "scr_123"
        assert run.devbox_id == "dbx_123"
        mock_client.scenarios.start_run.assert_called_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )

    def test_run(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run method."""
        mock_client.scenarios.start_run_and_await_env_ready.return_value = scenario_run_view

        scenario = Scenario(mock_client, "scn_123")
        run = scenario.run(run_name="test-run")

        assert run.id == "scr_123"
        assert run.devbox_id == "dbx_123"
        mock_client.scenarios.start_run_and_await_env_ready.assert_called_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )
