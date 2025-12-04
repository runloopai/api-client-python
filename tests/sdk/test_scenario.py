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
        result = scenario.update(name="new-name", metadata={"key": "value"})

        assert result == scenario_view
        mock_client.scenarios.update.assert_called_once_with(
            "scn_123",
            name="new-name",
            metadata={"key": "value"},
        )

    def test_run(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run method returns ScenarioRun wrapper."""
        mock_client.scenarios.start_run.return_value = scenario_run_view

        scenario = Scenario(mock_client, "scn_123")
        run = scenario.run_async(run_name="test-run")

        assert run.id == "run_123"
        assert run.devbox_id == "dev_123"
        mock_client.scenarios.start_run.assert_called_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )

    def test_run_and_await_env_ready(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run_and_await_env_ready method."""
        mock_client.scenarios.start_run_and_await_env_ready.return_value = scenario_run_view

        scenario = Scenario(mock_client, "scn_123")
        run = scenario.run(run_name="test-run")

        assert run.id == "run_123"
        assert run.devbox_id == "dev_123"
        mock_client.scenarios.start_run_and_await_env_ready.assert_called_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )
