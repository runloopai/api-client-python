"""Synchronous SDK smoke tests for Benchmark operations.

These tests validate the Benchmark class against the real API.
We create a dedicated smoketest benchmark and scenarios with consistent names
so that resources are reused across test runs (since there's no delete endpoint).
"""

from __future__ import annotations

from typing import List, Tuple

import pytest

from runloop_api_client import RunloopSDK
from runloop_api_client.sdk import Scenario, Benchmark, ScenarioRun, BenchmarkRun

pytestmark = [pytest.mark.smoketest]

TWO_MINUTE_TIMEOUT = 120

# Consistent names for smoketest resources
SMOKETEST_BENCHMARK_NAME = "sdk-smoketest-benchmark"
SMOKETEST_SCENARIO_1_NAME = "sdk-smoketest-scenario-1"
SMOKETEST_SCENARIO_2_NAME = "sdk-smoketest-scenario-2"


def get_or_create_scenario(
    sdk_client: RunloopSDK,
    name: str,
    problem_statement: str,
) -> Scenario:
    """Get an existing scenario by name or create a new one."""
    # Check if scenario already exists
    scenarios = sdk_client.scenario.list(name=name, limit=1)
    for scenario in scenarios:
        # Return the first matching scenario
        return scenario

    # Create a new scenario using the SDK builder
    return (
        sdk_client.scenario.builder(name)
        .with_problem_statement(problem_statement)
        .add_shell_command_scorer("pass-scorer", command="exit 0")
        .push()
    )


def get_or_create_benchmark(
    sdk_client: RunloopSDK,
    name: str,
    scenario_ids: List[str],
) -> Benchmark:
    """Get an existing benchmark by name or create a new one."""
    # Check if benchmark already exists
    benchmarks = sdk_client.benchmark.list(name=name, limit=1)
    for benchmark in benchmarks:
        # Return the first matching benchmark
        return benchmark

    # Create a new benchmark
    return sdk_client.benchmark.create(
        name=name,
        scenario_ids=scenario_ids,
        description="Smoketest benchmark for SDK testing",
    )


@pytest.fixture(scope="module")
def smoketest_benchmark(
    sdk_client: RunloopSDK,
) -> Tuple[Benchmark, List[str]]:
    """Create or retrieve the smoketest benchmark and scenarios."""
    # Create or get scenarios
    scenario_1 = get_or_create_scenario(
        sdk_client,
        SMOKETEST_SCENARIO_1_NAME,
        "Smoketest scenario 1 - basic validation",
    )
    scenario_2 = get_or_create_scenario(
        sdk_client,
        SMOKETEST_SCENARIO_2_NAME,
        "Smoketest scenario 2 - basic validation",
    )

    scenario_ids = [scenario_1.id, scenario_2.id]

    # Create or get benchmark
    benchmark = get_or_create_benchmark(
        sdk_client,
        SMOKETEST_BENCHMARK_NAME,
        scenario_ids,
    )

    return benchmark, scenario_ids


class TestBenchmarkRun:
    """Test Benchmark run operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_benchmark_run_lifecycle(
        self,
        sdk_client: RunloopSDK,
        smoketest_benchmark: Tuple[Benchmark, List[str]],
    ) -> None:
        """Test starting and canceling a benchmark run.

        This test:
        1. Uses the smoketest benchmark fixture
        2. Starts a new benchmark run via the Benchmark class
        3. Validates the run object
        4. Cancels the run
        """
        benchmark, scenario_ids = smoketest_benchmark

        # Start a run
        run = benchmark.start_run(run_name="sdk-smoketest-benchmark-run")
        scenario_runs: List[ScenarioRun] = []

        try:
            assert isinstance(run, BenchmarkRun)
            assert run.id is not None
            assert run.benchmark_id == benchmark.id

            # Get run info
            info = run.get_info()
            assert info.id == run.id
            assert info.state == "running"

            # Start a scenario run
            for scenario_id in scenario_ids:
                scenario = sdk_client.scenario.from_id(scenario_id)
                scenario_runs.append(
                    scenario.run(benchmark_run_id=run.id, run_name="sdk-smoketest-benchmark-run-scenario")
                )

            benchmark_scenario_runs = run.list_scenario_runs()
            assert isinstance(benchmark_scenario_runs, list)
            assert len(benchmark_scenario_runs) == len(scenario_runs)
            for scenario_run in benchmark_scenario_runs:
                assert isinstance(scenario_run, ScenarioRun)
                assert any(
                    scenario_run.id == scenario_run.id and scenario_run.devbox_id == scenario_run.devbox_id
                    for scenario_run in scenario_runs
                )

            # Cancel the scenario runs
            for scenario_run in scenario_runs:
                scenario_result = scenario_run.cancel()
                assert scenario_result.state in ["canceled", "completed"]

            # Cancel the benchmark run
            result = run.cancel()
            assert result.state in ["canceled", "completed"]

        except Exception:
            # Ensure cleanup on any error
            for scenario_run in scenario_runs:
                scenario_run.cancel()
            run.cancel()
            raise


class TestBenchmarkListRuns:
    """Test Benchmark list_runs operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_list_runs(
        self,
        smoketest_benchmark: Tuple[Benchmark, List[str]],
    ) -> None:
        """Test listing benchmark runs.

        This test:
        1. Uses the smoketest benchmark fixture
        2. Lists its runs
        3. Validates returned objects are BenchmarkRun instances
        """
        benchmark, _ = smoketest_benchmark

        runs = benchmark.list_runs()
        assert isinstance(runs, list)
        if not runs:
            pytest.skip("No runs available to test")

        # Verify returned items are BenchmarkRun objects
        for run in runs:
            assert isinstance(run, BenchmarkRun)
            assert run.id is not None
            assert run.benchmark_id == benchmark.id
