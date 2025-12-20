"""Comprehensive tests for sync ScenarioRun class."""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock

from tests.sdk.conftest import MockDevboxView, MockScenarioRunView
from runloop_api_client.sdk import ScenarioRun


class TestScenarioRun:
    """Tests for ScenarioRun class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test ScenarioRun initialization."""
        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        assert run.id == "scr_123"
        assert run.devbox_id == "dbx_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test ScenarioRun string representation."""
        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        assert repr(run) == "<ScenarioRun id='scr_123'>"

    def test_devbox_property(self, mock_client: Mock) -> None:
        """Test devbox property returns Devbox wrapper."""
        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        devbox = run.devbox

        assert devbox.id == "dbx_123"

    def test_get_info(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test get_info method."""
        mock_client.scenarios.runs.retrieve.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.get_info()

        assert result == scenario_run_view
        mock_client.scenarios.runs.retrieve.assert_called_once_with("scr_123")

    def test_await_env_ready(
        self, mock_client: Mock, scenario_run_view: MockScenarioRunView, devbox_view: MockDevboxView
    ) -> None:
        """Test await_env_ready method."""
        mock_client.devboxes.await_running.return_value = devbox_view
        mock_client.scenarios.runs.retrieve.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.await_env_ready()

        mock_client.devboxes.await_running.assert_called_once_with("dbx_123", polling_config=None)
        assert result == scenario_run_view

    def test_score(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score method."""
        scenario_run_view.state = "scoring"
        mock_client.scenarios.runs.score.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.score()

        assert result == scenario_run_view
        mock_client.scenarios.runs.score.assert_called_once_with("scr_123")

    def test_await_scored(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test await_scored method."""
        scenario_run_view.state = "scored"
        mock_client.scenarios.runs.await_scored.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.await_scored()

        assert result == scenario_run_view
        mock_client.scenarios.runs.await_scored.assert_called_once_with("scr_123")

    def test_score_and_await(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score_and_await method."""
        scenario_run_view.state = "scored"
        mock_client.scenarios.runs.score_and_await.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.score_and_await()

        assert result == scenario_run_view
        mock_client.scenarios.runs.score_and_await.assert_called_once_with("scr_123")

    def test_score_and_complete(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score_and_complete method."""
        scenario_run_view.state = "completed"
        mock_client.scenarios.runs.score_and_complete.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.score_and_complete()

        assert result == scenario_run_view
        mock_client.scenarios.runs.score_and_complete.assert_called_once_with("scr_123")

    def test_complete(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test complete method."""
        scenario_run_view.state = "completed"
        mock_client.scenarios.runs.complete.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.complete()

        assert result == scenario_run_view
        mock_client.scenarios.runs.complete.assert_called_once_with("scr_123")

    def test_cancel(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test cancel method."""
        scenario_run_view.state = "canceled"
        mock_client.scenarios.runs.cancel.return_value = scenario_run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.cancel()

        assert result == scenario_run_view
        mock_client.scenarios.runs.cancel.assert_called_once_with("scr_123")

    def test_download_logs(self, mock_client: Mock, tmp_path: Path) -> None:
        """Test download_logs method writes to file."""
        mock_response = Mock()
        mock_response.write_to_file = Mock()
        mock_client.scenarios.runs.download_logs.return_value = mock_response

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        output_path = tmp_path / "logs.zip"
        run.download_logs(output_path)

        mock_client.scenarios.runs.download_logs.assert_called_once_with("scr_123")
        mock_response.write_to_file.assert_called_once_with(output_path)

    def test_get_score_when_scored(self, mock_client: Mock) -> None:
        """Test get_score returns scoring result when scored."""
        scoring_result = SimpleNamespace(score=0.95, scoring_function_results=[])
        run_view = MockScenarioRunView(state="scored", scoring_contract_result=scoring_result)
        mock_client.scenarios.runs.retrieve.return_value = run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.get_score()

        assert result == scoring_result
        mock_client.scenarios.runs.retrieve.assert_called_once_with("scr_123")

    def test_get_score_when_not_scored(self, mock_client: Mock) -> None:
        """Test get_score returns None when not scored."""
        run_view = MockScenarioRunView(state="running", scoring_contract_result=None)
        mock_client.scenarios.runs.retrieve.return_value = run_view

        run = ScenarioRun(mock_client, "scr_123", "dbx_123")
        result = run.get_score()

        assert result is None
        mock_client.scenarios.runs.retrieve.assert_called_once_with("scr_123")
