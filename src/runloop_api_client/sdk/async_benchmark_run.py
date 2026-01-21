"""AsyncBenchmarkRun resource class for asynchronous operations."""

from __future__ import annotations

from typing import List
from typing_extensions import Unpack, override

from ..types import BenchmarkRunView
from ._types import BaseRequestOptions, LongRequestOptions, SDKBenchmarkRunListScenarioRunsParams
from .._client import AsyncRunloop
from .async_scenario_run import AsyncScenarioRun


class AsyncBenchmarkRun:
    """A benchmark run for evaluating agent performance across scenarios (async).

    Provides async methods for monitoring run status, managing the run lifecycle,
    and accessing scenario run results. Obtain instances via
    ``benchmark.start_run()`` or ``benchmark.list_runs()``.

    Example:
        >>> benchmark = runloop.benchmark.from_id("bench-xxx")
        >>> run = await benchmark.start_run(run_name="evaluation-v1")
        >>> info = await run.get_info()
        >>> scenario_runs = await run.list_scenario_runs()
    """

    def __init__(self, client: AsyncRunloop, run_id: str, benchmark_id: str) -> None:
        """Create an AsyncBenchmarkRun instance.

        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        :param run_id: Benchmark run ID
        :type run_id: str
        :param benchmark_id: Parent benchmark ID
        :type benchmark_id: str
        """
        self._client = client
        self._id = run_id
        self._benchmark_id = benchmark_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncBenchmarkRun id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the benchmark run ID.

        :return: Unique benchmark run ID
        :rtype: str
        """
        return self._id

    @property
    def benchmark_id(self) -> str:
        """Return the parent benchmark ID.

        :return: Parent benchmark ID
        :rtype: str
        """
        return self._benchmark_id

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> BenchmarkRunView:
        """Retrieve current benchmark run status and metadata.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.BaseRequestOptions` for available options
        :return: Current benchmark run state info
        :rtype: BenchmarkRunView
        """
        return await self._client.benchmark_runs.retrieve(
            self._id,
            **options,
        )

    async def cancel(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> BenchmarkRunView:
        """Cancel the benchmark run.

        Stops all running scenarios and marks the run as canceled.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Updated benchmark run state
        :rtype: BenchmarkRunView
        """
        return await self._client.benchmark_runs.cancel(
            self._id,
            **options,
        )

    async def complete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> BenchmarkRunView:
        """Complete the benchmark run.

        Marks the run as completed. Call this after all scenarios have finished.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Completed benchmark run state
        :rtype: BenchmarkRunView
        """
        return await self._client.benchmark_runs.complete(
            self._id,
            **options,
        )

    async def list_scenario_runs(
        self,
        **params: Unpack[SDKBenchmarkRunListScenarioRunsParams],
    ) -> List[AsyncScenarioRun]:
        """List all scenario runs for this benchmark run.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKBenchmarkRunListScenarioRunsParams` for available parameters
        :return: List of async scenario run objects
        :rtype: List[AsyncScenarioRun]
        """
        page = await self._client.benchmark_runs.list_scenario_runs(
            self._id,
            **params,
        )
        return [AsyncScenarioRun(self._client, run.id, run.devbox_id) for run in page.runs]
