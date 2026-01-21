"""Comprehensive tests for sync BenchmarkRun class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import MockScenarioRunView, MockBenchmarkRunView
from runloop_api_client.sdk.scenario_run import ScenarioRun
from runloop_api_client.sdk.benchmark_run import BenchmarkRun


class TestBenchmarkRun:
    """Tests for BenchmarkRun class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test BenchmarkRun initialization."""
        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        assert run.id == "bmr_123"
        assert run.benchmark_id == "bmd_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test BenchmarkRun string representation."""
        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        assert repr(run) == "<BenchmarkRun id='bmr_123'>"

    def test_get_info(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test get_info method."""
        mock_client.benchmark_runs.retrieve.return_value = benchmark_run_view

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.get_info()

        assert result == benchmark_run_view
        mock_client.benchmark_runs.retrieve.assert_called_once_with("bmr_123")

    def test_cancel(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test cancel method."""
        benchmark_run_view.state = "canceled"
        mock_client.benchmark_runs.cancel.return_value = benchmark_run_view

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.cancel()

        assert result == benchmark_run_view
        assert result.state == "canceled"
        mock_client.benchmark_runs.cancel.assert_called_once_with("bmr_123")

    def test_complete(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test complete method."""
        benchmark_run_view.state = "completed"
        mock_client.benchmark_runs.complete.return_value = benchmark_run_view

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.complete()

        assert result == benchmark_run_view
        assert result.state == "completed"
        mock_client.benchmark_runs.complete.assert_called_once_with("bmr_123")

    def test_list_scenario_runs_empty(self, mock_client: Mock) -> None:
        """Test list_scenario_runs method with empty results."""
        page = SimpleNamespace(runs=[])
        mock_client.benchmark_runs.list_scenario_runs.return_value = page

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.list_scenario_runs()

        assert len(result) == 0
        mock_client.benchmark_runs.list_scenario_runs.assert_called_once_with("bmr_123")

    def test_list_scenario_runs_single(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test list_scenario_runs method with single result."""
        page = SimpleNamespace(runs=[scenario_run_view])
        mock_client.benchmark_runs.list_scenario_runs.return_value = page

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.list_scenario_runs()

        assert len(result) == 1
        assert isinstance(result[0], ScenarioRun)
        assert result[0].id == scenario_run_view.id
        assert result[0].devbox_id == scenario_run_view.devbox_id
        mock_client.benchmark_runs.list_scenario_runs.assert_called_once_with("bmr_123")

    def test_list_scenario_runs_multiple(self, mock_client: Mock) -> None:
        """Test list_scenario_runs method with multiple results."""
        scenario_run_view1 = MockScenarioRunView(id="scr_001", devbox_id="dev_001")
        scenario_run_view2 = MockScenarioRunView(id="scr_002", devbox_id="dev_002")
        page = SimpleNamespace(runs=[scenario_run_view1, scenario_run_view2])
        mock_client.benchmark_runs.list_scenario_runs.return_value = page

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.list_scenario_runs()

        assert len(result) == 2
        assert isinstance(result[0], ScenarioRun)
        assert isinstance(result[1], ScenarioRun)
        assert result[0].id == "scr_001"
        assert result[1].id == "scr_002"
        mock_client.benchmark_runs.list_scenario_runs.assert_called_once_with("bmr_123")

    def test_list_scenario_runs_with_params(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test list_scenario_runs method with filtering parameters."""
        page = SimpleNamespace(runs=[scenario_run_view])
        mock_client.benchmark_runs.list_scenario_runs.return_value = page

        run = BenchmarkRun(mock_client, "bmr_123", "bmd_123")
        result = run.list_scenario_runs(limit=10, state="completed")

        assert len(result) == 1
        assert isinstance(result[0], ScenarioRun)
        assert result[0].id == scenario_run_view.id
        mock_client.benchmark_runs.list_scenario_runs.assert_called_once_with("bmr_123", limit=10, state="completed")
