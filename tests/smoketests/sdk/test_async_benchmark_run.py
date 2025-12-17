"""Asynchronous SDK smoke tests for AsyncBenchmarkRun operations.

These tests validate the AsyncBenchmarkRun class against the real API.
Until AsyncBenchmarkOps is available (PR3), we use the raw async API client
to find or create benchmark runs for testing.
"""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from runloop_api_client.sdk.async_scenario_run import AsyncScenarioRun
from runloop_api_client.sdk.async_benchmark_run import AsyncBenchmarkRun

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120


class TestAsyncBenchmarkRunRetrieval:
    """Test AsyncBenchmarkRun retrieval operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_benchmark_run_from_existing(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating AsyncBenchmarkRun from existing benchmark run.

        This test:
        1. Lists benchmark runs via raw async API
        2. Creates an AsyncBenchmarkRun wrapper
        3. Validates get_info returns correct data
        """
        # List existing benchmark runs via raw API
        runs_page = await async_sdk_client.api.benchmarks.runs.list(limit=1)
        runs = runs_page.runs

        if not runs:
            pytest.skip("No benchmark runs available to test")

        run_data = runs[0]

        # Create AsyncBenchmarkRun wrapper
        benchmark_run = AsyncBenchmarkRun(
            client=async_sdk_client.api,
            run_id=run_data.id,
            benchmark_id=run_data.benchmark_id,
        )

        assert benchmark_run.id == run_data.id
        assert benchmark_run.benchmark_id == run_data.benchmark_id

        # Test get_info
        info = await benchmark_run.get_info()
        assert info.id == run_data.id
        assert info.benchmark_id == run_data.benchmark_id

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_benchmark_run_list_scenario_runs(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test AsyncBenchmarkRun.list_scenario_runs method.

        This test:
        1. Finds an existing benchmark run
        2. Lists its scenario runs
        """
        # List existing benchmark runs via raw API
        runs_page = await async_sdk_client.api.benchmarks.runs.list(limit=1)
        runs = runs_page.runs

        if not runs:
            pytest.skip("No benchmark runs available to test")

        run_data = runs[0]

        # Create AsyncBenchmarkRun wrapper
        benchmark_run = AsyncBenchmarkRun(
            client=async_sdk_client.api,
            run_id=run_data.id,
            benchmark_id=run_data.benchmark_id,
        )

        # List scenario runs (might be empty, that's okay)
        scenario_runs = await benchmark_run.list_scenario_runs()
        assert isinstance(scenario_runs, list)

        # Verify returned items are AsyncScenarioRun objects
        for scenario_run in scenario_runs:
            assert isinstance(scenario_run, AsyncScenarioRun)
            assert scenario_run.id is not None
            assert scenario_run.devbox_id is not None


class TestAsyncBenchmarkRunLifecycle:
    """Test AsyncBenchmarkRun lifecycle operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_benchmark_run_create_and_cancel(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a benchmark run and canceling it.

        This test:
        1. Finds an existing benchmark
        2. Starts a new benchmark run
        3. Creates an AsyncBenchmarkRun wrapper
        4. Cancels the run
        """
        # Find an existing benchmark via raw API
        benchmarks_page = await async_sdk_client.api.benchmarks.list(limit=1)
        benchmarks = benchmarks_page.benchmarks

        if not benchmarks:
            pytest.skip("No benchmarks available to test")

        benchmark = benchmarks[0]

        # Start a new benchmark run
        run_data = await async_sdk_client.api.benchmarks.start_run(
            benchmark_id=benchmark.id,
            run_name="sdk-smoketest-async-benchmark-run",
        )

        try:
            # Create AsyncBenchmarkRun wrapper
            benchmark_run = AsyncBenchmarkRun(
                client=async_sdk_client.api,
                run_id=run_data.id,
                benchmark_id=run_data.benchmark_id,
            )

            assert benchmark_run.id == run_data.id

            # Get info
            info = await benchmark_run.get_info()
            assert info.id == run_data.id
            assert info.state in ["running", "completed", "canceled"]

            # Cancel the run
            result = await benchmark_run.cancel()
            assert result.state in ["canceled", "completed"]  # May already be completed

        except Exception:
            # Ensure cleanup on any error
            try:
                await async_sdk_client.api.benchmarks.runs.cancel(run_data.id)
            except Exception:
                pass
            raise
