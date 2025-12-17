"""Synchronous SDK smoke tests for BenchmarkRun operations.

These tests validate the BenchmarkRun class against the real API.
Until BenchmarkOps is available (PR3), we use the raw API client to
find or create benchmark runs for testing.
"""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from runloop_api_client.sdk.scenario_run import ScenarioRun
from runloop_api_client.sdk.benchmark_run import BenchmarkRun

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120


class TestBenchmarkRunRetrieval:
    """Test BenchmarkRun retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_benchmark_run_from_existing(self, sdk_client: RunloopSDK) -> None:
        """Test creating BenchmarkRun from existing benchmark run.

        This test:
        1. Lists benchmark runs via raw API
        2. Creates a BenchmarkRun wrapper
        3. Validates get_info returns correct data
        """
        # List existing benchmark runs via raw API
        runs = sdk_client.api.benchmarks.runs.list(limit=1).runs

        if not runs:
            pytest.skip("No benchmark runs available to test")

        run_data = runs[0]

        # Create BenchmarkRun wrapper
        benchmark_run = BenchmarkRun(
            client=sdk_client.api,
            run_id=run_data.id,
            benchmark_id=run_data.benchmark_id,
        )

        assert benchmark_run.id == run_data.id
        assert benchmark_run.benchmark_id == run_data.benchmark_id

        # Test get_info
        info = benchmark_run.get_info()
        assert info.id == run_data.id
        assert info.benchmark_id == run_data.benchmark_id

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_benchmark_run_list_scenario_runs(self, sdk_client: RunloopSDK) -> None:
        """Test BenchmarkRun.list_scenario_runs method.

        This test:
        1. Finds an existing benchmark run
        2. Lists its scenario runs
        """
        # List existing benchmark runs via raw API
        runs = sdk_client.api.benchmarks.runs.list(limit=1).runs

        if not runs:
            pytest.skip("No benchmark runs available to test")

        run_data = runs[0]

        # Create BenchmarkRun wrapper
        benchmark_run = BenchmarkRun(
            client=sdk_client.api,
            run_id=run_data.id,
            benchmark_id=run_data.benchmark_id,
        )

        # List scenario runs (might be empty, that's okay)
        scenario_runs = benchmark_run.list_scenario_runs()
        assert isinstance(scenario_runs, list)

        # Verify returned items are ScenarioRun objects
        for scenario_run in scenario_runs:
            assert isinstance(scenario_run, ScenarioRun)
            assert scenario_run.id is not None
            assert scenario_run.devbox_id is not None


class TestBenchmarkRunLifecycle:
    """Test BenchmarkRun lifecycle operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_benchmark_run_create_and_cancel(self, sdk_client: RunloopSDK) -> None:
        """Test creating a benchmark run and canceling it.

        This test:
        1. Finds an existing benchmark
        2. Starts a new benchmark run
        3. Creates a BenchmarkRun wrapper
        4. Cancels the run
        """
        # Find an existing benchmark via raw API
        benchmarks = sdk_client.api.benchmarks.list(limit=1).benchmarks

        if not benchmarks:
            pytest.skip("No benchmarks available to test")

        benchmark = benchmarks[0]

        # Start a new benchmark run
        run_data = sdk_client.api.benchmarks.start_run(
            benchmark_id=benchmark.id,
            run_name="sdk-smoketest-benchmark-run",
        )

        try:
            # Create BenchmarkRun wrapper
            benchmark_run = BenchmarkRun(
                client=sdk_client.api,
                run_id=run_data.id,
                benchmark_id=run_data.benchmark_id,
            )

            assert benchmark_run.id == run_data.id

            # Get info
            info = benchmark_run.get_info()
            assert info.id == run_data.id
            assert info.state in ["running", "completed", "canceled"]

            # Cancel the run
            result = benchmark_run.cancel()
            assert result.state in ["canceled", "completed"]  # May already be completed

        except Exception:
            # Ensure cleanup on any error
            try:
                sdk_client.api.benchmarks.runs.cancel(run_data.id)
            except Exception:
                pass
            raise
