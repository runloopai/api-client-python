"""Synchronous SDK smoke tests for Benchmark operations.

These tests validate the Benchmark class against the real API.
Until BenchmarkOps is available (PR3), we use the raw API client to
find or create benchmarks for testing.
"""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import Benchmark, RunloopSDK, ScenarioRun, BenchmarkRun

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120


class TestBenchmarkRetrieval:
    """Test Benchmark retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_benchmark_from_existing(self, sdk_client: RunloopSDK) -> None:
        """Test creating Benchmark from existing benchmark.

        This test:
        1. Lists benchmarks via raw API
        2. Creates a Benchmark wrapper
        3. Validates get_info returns correct data
        """
        # List existing benchmarks via raw API
        benchmarks = sdk_client.api.benchmarks.list_public(limit=1).benchmarks

        if not benchmarks:
            pytest.skip("No benchmarks available to test")

        benchmark_data = benchmarks[0]

        # Create Benchmark wrapper
        benchmark = Benchmark(
            client=sdk_client.api,
            benchmark_id=benchmark_data.id,
        )

        assert benchmark.id == benchmark_data.id

        # Test get_info
        info = benchmark.get_info()
        assert info.id == benchmark_data.id
        assert info.name == benchmark_data.name


class TestBenchmarkRun:
    """Test Benchmark run operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_benchmark_run_lifecycle(self, sdk_client: RunloopSDK) -> None:
        """Test starting and canceling a benchmark run.

        This test:
        1. Finds an existing benchmark
        2. Starts a new benchmark run via the Benchmark class
        3. Validates the run object
        4. Cancels the run
        """
        # Find an existing benchmark via raw API
        benchmarks = sdk_client.api.benchmarks.list_public(limit=1).benchmarks

        if not benchmarks:
            pytest.skip("No benchmarks available to test")

        benchmark_data = benchmarks[0]

        # Create Benchmark wrapper
        benchmark = Benchmark(
            client=sdk_client.api,
            benchmark_id=benchmark_data.id,
        )

        # Start a run
        run = benchmark.run(run_name="sdk-smoketest-benchmark-run")

        # If the benchmark has scenarios, run one
        scenario_runs: list[ScenarioRun] = []
        if benchmark_data.scenario_ids:
            scenario = sdk_client.scenario.from_id(benchmark_data.scenario_ids[0])
            scenario_runs.append(scenario.run(benchmark_run_id=run.id, run_name="sdk-smoketest-benchmark-run-scenario"))

        try:
            assert isinstance(run, BenchmarkRun)
            assert run.id is not None
            assert run.benchmark_id == benchmark.id

            # Get run info
            info = run.get_info()
            assert info.id == run.id
            assert info.state in ["running", "completed", "canceled"]

            bench_scenario_runs = run.list_scenario_runs()
            assert isinstance(bench_scenario_runs, list)
            assert len(bench_scenario_runs) == len(scenario_runs)
            for bench_scenario_run in bench_scenario_runs:
                assert isinstance(bench_scenario_run, ScenarioRun)
                assert bench_scenario_run.id == scenario_runs[0].id
                assert bench_scenario_run.devbox_id == scenario_runs[0].devbox_id

                # Cancel the scenario run
                scenario_result = bench_scenario_run.cancel()
                assert scenario_result.state in ["canceled", "completed"]

            # Cancel the benchmark run
            result = run.cancel()
            assert result.state in ["canceled", "completed"]

        except Exception:
            # Ensure cleanup on any error
            try:
                for scenario_run in scenario_runs:
                    sdk_client.api.scenarios.runs.cancel(scenario_run.id)
                sdk_client.api.benchmarks.runs.cancel(run.id)
            except Exception:
                pass
            raise


class TestBenchmarkListRuns:
    """Test Benchmark list_runs operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_list_runs(self, sdk_client: RunloopSDK) -> None:
        """Test listing benchmark runs.

        This test:
        1. Finds an existing benchmark
        2. Lists its runs
        3. Validates returned objects are BenchmarkRun instances
        """
        # Find an existing benchmark via raw API
        benchmarks = sdk_client.api.benchmarks.list(limit=1).benchmarks

        if not benchmarks:
            pytest.skip("No benchmarks available to test")

        benchmark_data = benchmarks[0]

        # Create Benchmark wrapper
        benchmark = Benchmark(
            client=sdk_client.api,
            benchmark_id=benchmark_data.id,
        )

        # List runs (might be empty, that's okay)
        runs = benchmark.list_runs()
        assert isinstance(runs, list)

        # Verify returned items are BenchmarkRun objects
        for run in runs:
            assert isinstance(run, BenchmarkRun)
            assert run.id is not None
            assert run.benchmark_id == benchmark.id
