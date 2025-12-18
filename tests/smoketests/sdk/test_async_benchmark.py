"""Asynchronous SDK smoke tests for AsyncBenchmark operations.

These tests validate the AsyncBenchmark class against the real API.
Until AsyncBenchmarkOps is available (PR3), we use the raw async API client
to find or create benchmarks for testing.
"""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncBenchmark, AsyncRunloopSDK, AsyncScenarioRun, AsyncBenchmarkRun

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120


class TestAsyncBenchmarkRetrieval:
    """Test AsyncBenchmark retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_benchmark_from_existing(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating AsyncBenchmark from existing benchmark.

        This test:
        1. Lists benchmarks via raw async API
        2. Creates an AsyncBenchmark wrapper
        3. Validates get_info returns correct data
        """
        # List existing benchmarks via raw API
        benchmarks_page = await async_sdk_client.api.benchmarks.list_public(limit=1)
        benchmarks = benchmarks_page.benchmarks

        if not benchmarks:
            raise Exception("No benchmarks available to test")

        benchmark_data = benchmarks[0]

        # Create AsyncBenchmark wrapper
        benchmark = AsyncBenchmark(
            client=async_sdk_client.api,
            benchmark_id=benchmark_data.id,
        )

        assert benchmark.id == benchmark_data.id

        # Test get_info
        info = await benchmark.get_info()
        assert info.id == benchmark_data.id
        assert info.name == benchmark_data.name


class TestAsyncBenchmarkRun:
    """Test AsyncBenchmark run operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_benchmark_run_and_cancel(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test starting and canceling a benchmark run.

        This test:
        1. Finds an existing benchmark
        2. Starts a new benchmark run via the AsyncBenchmark class
        3. Validates the run object
        4. Cancels the run
        """
        # Find an existing benchmark via raw API
        benchmarks_page = await async_sdk_client.api.benchmarks.list_public(limit=1)
        benchmarks = benchmarks_page.benchmarks

        if not benchmarks:
            raise Exception("No benchmarks available to test")

        benchmark_data = benchmarks[0]
        if not benchmark_data.scenario_ids:
            raise Exception("No scenarios available to test")

        # Create AsyncBenchmark wrapper
        benchmark = AsyncBenchmark(
            client=async_sdk_client.api,
            benchmark_id=benchmark_data.id,
        )

        # Start a run
        run = await benchmark.run(run_name="sdk-smoketest-async-benchmark-run")
        scenario = async_sdk_client.scenario.from_id(benchmark_data.scenario_ids[0])
        scenario_run = None

        try:
            assert isinstance(run, AsyncBenchmarkRun)
            assert run.id is not None
            assert run.benchmark_id == benchmark.id

            # Get run info
            info = await run.get_info()
            assert info.id == run.id
            assert info.state in ["running", "completed", "canceled"]

            # Start a scenario run
            scenario_run = await scenario.run(
                benchmark_run_id=run.id, run_name="sdk-smoketest-async-benchmark-run-scenario"
            )
            scenario_runs = await run.list_scenario_runs()
            assert isinstance(scenario_runs, list)
            assert len(scenario_runs) == 1
            assert isinstance(scenario_runs[0], AsyncScenarioRun)
            assert scenario_runs[0].id == scenario_run.id
            assert scenario_runs[0].devbox_id == scenario_run.devbox_id

            # Cancel the scenario run
            scenario_result = await scenario_run.cancel()
            assert scenario_result.state in ["canceled", "completed"]

            # Cancel the benchmark run
            result = await run.cancel()
            assert result.state in ["canceled", "completed"]

        except Exception:
            # Ensure cleanup on any error
            if scenario_run:
                await async_sdk_client.api.scenarios.runs.cancel(scenario_run.id)
            await async_sdk_client.api.benchmarks.runs.cancel(run.id)
            raise


class TestAsyncBenchmarkListRuns:
    """Test AsyncBenchmark list_runs operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_list_runs(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing benchmark runs.

        This test:
        1. Finds an existing benchmark
        2. Lists its runs
        3. Validates returned objects are AsyncBenchmarkRun instances
        """
        # Find an existing benchmark via raw API
        benchmarks_page = await async_sdk_client.api.benchmarks.list(limit=1)
        benchmarks = benchmarks_page.benchmarks

        if not benchmarks:
            raise Exception("No benchmarks available to test")

        benchmark_data = benchmarks[0]

        # Create AsyncBenchmark wrapper
        benchmark = AsyncBenchmark(
            client=async_sdk_client.api,
            benchmark_id=benchmark_data.id,
        )

        # List runs (might be empty, that's okay)
        runs = await benchmark.list_runs()
        assert isinstance(runs, list)

        # Verify returned items are AsyncBenchmarkRun objects
        for run in runs:
            assert isinstance(run, AsyncBenchmarkRun)
            assert run.id is not None
            assert run.benchmark_id == benchmark.id
