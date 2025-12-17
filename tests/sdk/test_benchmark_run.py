"""Comprehensive tests for sync BenchmarkRun class."""

from __future__ import annotations

from unittest.mock import Mock

from tests.sdk.conftest import MockScenarioRunView, MockBenchmarkRunView
from runloop_api_client.sdk.benchmark_run import BenchmarkRun


class TestBenchmarkRun:
    """Tests for BenchmarkRun class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test BenchmarkRun initialization."""
        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        assert run.id == "bench_run_123"
        assert run.benchmark_id == "bench_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test BenchmarkRun string representation."""
        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        assert repr(run) == "<BenchmarkRun id='bench_run_123'>"

    def test_get_info(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test get_info method."""
        mock_client.benchmarks.runs.retrieve.return_value = benchmark_run_view

        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        result = run.get_info()

        assert result == benchmark_run_view
        mock_client.benchmarks.runs.retrieve.assert_called_once_with("bench_run_123")

    def test_cancel(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test cancel method."""
        benchmark_run_view.state = "canceled"
        mock_client.benchmarks.runs.cancel.return_value = benchmark_run_view

        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        result = run.cancel()

        assert result == benchmark_run_view
        assert result.state == "canceled"
        mock_client.benchmarks.runs.cancel.assert_called_once_with("bench_run_123")

    def test_complete(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test complete method."""
        benchmark_run_view.state = "completed"
        mock_client.benchmarks.runs.complete.return_value = benchmark_run_view

        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        result = run.complete()

        assert result == benchmark_run_view
        assert result.state == "completed"
        mock_client.benchmarks.runs.complete.assert_called_once_with("bench_run_123")

    def test_list_scenario_runs(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test list_scenario_runs method."""
        mock_page = [scenario_run_view]
        mock_client.benchmarks.runs.list_scenario_runs.return_value = mock_page

        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        result = run.list_scenario_runs()

        assert len(result) == 1
        assert result[0] == scenario_run_view
        mock_client.benchmarks.runs.list_scenario_runs.assert_called_once_with("bench_run_123")

    def test_list_scenario_runs_with_params(self, mock_client: Mock, scenario_run_view: MockScenarioRunView) -> None:
        """Test list_scenario_runs method with filtering parameters."""
        mock_page = [scenario_run_view]
        mock_client.benchmarks.runs.list_scenario_runs.return_value = mock_page

        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        result = run.list_scenario_runs(limit=10, state="completed")

        assert len(result) == 1
        mock_client.benchmarks.runs.list_scenario_runs.assert_called_once_with(
            "bench_run_123", limit=10, state="completed"
        )

    def test_list_scenario_runs_empty(self, mock_client: Mock) -> None:
        """Test list_scenario_runs returns empty list when no scenario runs."""
        mock_client.benchmarks.runs.list_scenario_runs.return_value = []

        run = BenchmarkRun(mock_client, "bench_run_123", "bench_123")
        result = run.list_scenario_runs()

        assert result == []
        mock_client.benchmarks.runs.list_scenario_runs.assert_called_once_with("bench_run_123")
