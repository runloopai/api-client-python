"""Benchmark resource class for synchronous operations."""

from __future__ import annotations

from typing import List
from typing_extensions import Unpack, override

from ..types import BenchmarkView
from ._types import (
    BaseRequestOptions,
    LongRequestOptions,
    SDKBenchmarkUpdateParams,
    SDKBenchmarkListRunsParams,
    SDKBenchmarkStartRunParams,
)
from .._types import SequenceNotStr
from .._client import Runloop
from .benchmark_run import BenchmarkRun


class Benchmark:
    """A benchmark for evaluating agent performance across scenarios.

    Provides methods for retrieving benchmark details, updating the benchmark,
    managing scenarios, and starting benchmark runs. Obtain instances via
    ``runloop.benchmark.from_id()`` or ``runloop.benchmark.list()``.

    Example:
        >>> benchmark = runloop.benchmark.from_id("bmd_xxx")
        >>> info = benchmark.get_info()
        >>> run = benchmark.start_run(run_name="evaluation-v1")
        >>> for scenario_id in info.scenario_ids:
        ...     scenario = runloop.scenario.from_id(scenario_id)
        ...     scenario_run = scenario.run(benchmark_run_id=run.id, run_name="evaluation-v1")
    """

    def __init__(self, client: Runloop, benchmark_id: str) -> None:
        """Create a Benchmark instance.

        :param client: Runloop client instance
        :type client: Runloop
        :param benchmark_id: Benchmark ID
        :type benchmark_id: str
        """
        self._client = client
        self._id = benchmark_id

    @override
    def __repr__(self) -> str:
        return f"<Benchmark id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the benchmark ID.

        :return: Unique benchmark ID
        :rtype: str
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> BenchmarkView:
        """Retrieve current benchmark details.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.BaseRequestOptions` for available options
        :return: Current benchmark info
        :rtype: BenchmarkView
        """
        return self._client.benchmarks.retrieve(
            self._id,
            **options,
        )

    def update(
        self,
        **params: Unpack[SDKBenchmarkUpdateParams],
    ) -> BenchmarkView:
        """Update the benchmark.

        Only provided fields will be updated.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkUpdateParams` for available parameters
        :return: Updated benchmark info
        :rtype: BenchmarkView
        """
        return self._client.benchmarks.update(
            self._id,
            **params,
        )

    def start_run(
        self,
        **params: Unpack[SDKBenchmarkStartRunParams],
    ) -> BenchmarkRun:
        """Start a new benchmark run.

        Creates a new benchmark run and returns a BenchmarkRun instance for
        managing the run lifecycle.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkStartRunParams` for available parameters
        :return: BenchmarkRun instance for managing the run
        :rtype: BenchmarkRun
        """
        run_view = self._client.benchmarks.start_run(
            benchmark_id=self._id,
            **params,
        )
        assert run_view.benchmark_id is not None, "benchmark_id should be set for runs created from a benchmark"
        return BenchmarkRun(self._client, run_view.id, run_view.benchmark_id)

    def add_scenarios(
        self,
        scenario_ids: SequenceNotStr[str],
        **options: Unpack[LongRequestOptions],
    ) -> BenchmarkView:
        """Add scenarios to the benchmark.

        :param scenario_ids: List of scenario IDs to add
        :type scenario_ids: SequenceNotStr[str]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Updated benchmark info
        :rtype: BenchmarkView
        """
        return self._client.benchmarks.update_scenarios(
            self._id,
            scenarios_to_add=scenario_ids,
            **options,
        )

    def remove_scenarios(
        self,
        scenario_ids: SequenceNotStr[str],
        **options: Unpack[LongRequestOptions],
    ) -> BenchmarkView:
        """Remove scenarios from the benchmark.

        :param scenario_ids: List of scenario IDs to remove
        :type scenario_ids: SequenceNotStr[str]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Updated benchmark info
        :rtype: BenchmarkView
        """
        return self._client.benchmarks.update_scenarios(
            self._id,
            scenarios_to_remove=scenario_ids,
            **options,
        )

    def list_runs(
        self,
        **params: Unpack[SDKBenchmarkListRunsParams],
    ) -> List[BenchmarkRun]:
        """List all runs for this benchmark.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkListRunsParams` for available parameters
        :return: List of benchmark runs
        :rtype: List[BenchmarkRun]
        """
        page = self._client.benchmark_runs.list(
            benchmark_id=self._id,
            **params,
        )
        return [
            BenchmarkRun(self._client, run.id, run.benchmark_id) for run in page.runs if run.benchmark_id is not None
        ]
