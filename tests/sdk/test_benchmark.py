"""Comprehensive tests for sync Benchmark class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import MockBenchmarkView, MockBenchmarkRunView
from runloop_api_client.sdk.benchmark import Benchmark
from runloop_api_client.sdk.benchmark_run import BenchmarkRun


class TestBenchmark:
    """Tests for Benchmark class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Benchmark initialization."""
        benchmark = Benchmark(mock_client, "bmd_123")
        assert benchmark.id == "bmd_123"
        assert repr(benchmark) == "<Benchmark id='bmd_123'>"

    def test_get_info(self, mock_client: Mock, benchmark_view: MockBenchmarkView) -> None:
        """Test get_info method."""
        mock_client.benchmarks.retrieve.return_value = benchmark_view

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.get_info()

        assert result == benchmark_view
        mock_client.benchmarks.retrieve.assert_called_once_with("bmd_123")

    def test_update(self, mock_client: Mock, benchmark_view: MockBenchmarkView) -> None:
        """Test update method."""
        benchmark_view.name = "updated-name"
        mock_client.benchmarks.update.return_value = benchmark_view

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.update(name="updated-name")

        assert result == benchmark_view
        mock_client.benchmarks.update.assert_called_once_with("bmd_123", name="updated-name")

    def test_run(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test run method."""
        mock_client.benchmarks.start_run.return_value = benchmark_run_view

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.start_run(run_name="test-run", metadata={"key": "value"})

        assert isinstance(result, BenchmarkRun)
        assert result.id == benchmark_run_view.id
        assert result.benchmark_id == benchmark_run_view.benchmark_id
        mock_client.benchmarks.start_run.assert_called_once_with(
            benchmark_id="bmd_123", run_name="test-run", metadata={"key": "value"}
        )

    def test_add_scenarios(self, mock_client: Mock, benchmark_view: MockBenchmarkView) -> None:
        """Test add_scenarios method."""
        benchmark_view.scenario_ids = ["scn_001", "scn_002"]
        mock_client.benchmarks.update_scenarios.return_value = benchmark_view

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.add_scenarios(["scn_001", "scn_002"])

        assert result == benchmark_view
        mock_client.benchmarks.update_scenarios.assert_called_once_with(
            "bmd_123", scenarios_to_add=["scn_001", "scn_002"]
        )

    def test_remove_scenarios(self, mock_client: Mock, benchmark_view: MockBenchmarkView) -> None:
        """Test remove_scenarios method."""
        mock_client.benchmarks.update_scenarios.return_value = benchmark_view

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.remove_scenarios(["scn_001"])

        assert result == benchmark_view
        mock_client.benchmarks.update_scenarios.assert_called_once_with("bmd_123", scenarios_to_remove=["scn_001"])

    def test_list_runs_single(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test list_runs method with single result."""
        page = SimpleNamespace(runs=[benchmark_run_view])
        mock_client.benchmark_runs.list.return_value = page

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.list_runs()

        assert len(result) == 1
        assert isinstance(result[0], BenchmarkRun)
        assert result[0].id == benchmark_run_view.id
        assert result[0].benchmark_id == benchmark_run_view.benchmark_id
        mock_client.benchmark_runs.list.assert_called_once_with(benchmark_id="bmd_123")

    def test_list_runs_multiple(self, mock_client: Mock) -> None:
        """Test list_runs method with multiple results."""
        run_view1 = MockBenchmarkRunView(id="bmr_001")
        run_view2 = MockBenchmarkRunView(id="bmr_002")
        page = SimpleNamespace(runs=[run_view1, run_view2])
        mock_client.benchmark_runs.list.return_value = page

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.list_runs()

        assert len(result) == 2
        assert isinstance(result[0], BenchmarkRun)
        assert isinstance(result[1], BenchmarkRun)
        assert result[0].id == run_view1.id
        assert result[0].benchmark_id == run_view1.benchmark_id
        assert result[1].id == run_view2.id
        assert result[1].benchmark_id == run_view2.benchmark_id
        mock_client.benchmark_runs.list.assert_called_once_with(benchmark_id="bmd_123")

    def test_list_runs_with_params(self, mock_client: Mock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test list_runs method with filtering parameters."""
        page = SimpleNamespace(runs=[benchmark_run_view])
        mock_client.benchmark_runs.list.return_value = page

        benchmark = Benchmark(mock_client, "bmd_123")
        result = benchmark.list_runs(limit=10, name="test-run")

        assert len(result) == 1
        mock_client.benchmark_runs.list.assert_called_once_with(benchmark_id="bmd_123", limit=10, name="test-run")
