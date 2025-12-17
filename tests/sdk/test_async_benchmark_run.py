"""Comprehensive tests for async AsyncBenchmarkRun class."""

from __future__ import annotations

from unittest.mock import AsyncMock

from tests.sdk.conftest import AsyncIterableMock, MockScenarioRunView, MockBenchmarkRunView
from runloop_api_client.sdk.async_benchmark_run import AsyncBenchmarkRun


class TestAsyncBenchmarkRun:
    """Tests for AsyncBenchmarkRun class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBenchmarkRun initialization."""
        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        assert run.id == "bench_run_123"
        assert run.benchmark_id == "bench_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBenchmarkRun string representation."""
        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        assert repr(run) == "<AsyncBenchmarkRun id='bench_run_123'>"

    async def test_get_info(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test get_info method."""
        mock_async_client.benchmarks.runs.retrieve = AsyncMock(return_value=benchmark_run_view)

        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        result = await run.get_info()

        assert result == benchmark_run_view
        mock_async_client.benchmarks.runs.retrieve.assert_awaited_once_with("bench_run_123")

    async def test_cancel(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test cancel method."""
        benchmark_run_view.state = "canceled"
        mock_async_client.benchmarks.runs.cancel = AsyncMock(return_value=benchmark_run_view)

        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        result = await run.cancel()

        assert result == benchmark_run_view
        assert result.state == "canceled"
        mock_async_client.benchmarks.runs.cancel.assert_awaited_once_with("bench_run_123")

    async def test_complete(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test complete method."""
        benchmark_run_view.state = "completed"
        mock_async_client.benchmarks.runs.complete = AsyncMock(return_value=benchmark_run_view)

        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        result = await run.complete()

        assert result == benchmark_run_view
        assert result.state == "completed"
        mock_async_client.benchmarks.runs.complete.assert_awaited_once_with("bench_run_123")

    async def test_list_scenario_runs(
        self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView
    ) -> None:
        """Test list_scenario_runs method."""
        mock_async_client.benchmarks.runs.list_scenario_runs.return_value = AsyncIterableMock([scenario_run_view])

        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        result = await run.list_scenario_runs()

        assert len(result) == 1
        assert result[0] == scenario_run_view
        mock_async_client.benchmarks.runs.list_scenario_runs.assert_called_once_with("bench_run_123")

    async def test_list_scenario_runs_with_params(
        self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView
    ) -> None:
        """Test list_scenario_runs method with filtering parameters."""
        mock_async_client.benchmarks.runs.list_scenario_runs.return_value = AsyncIterableMock([scenario_run_view])

        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        result = await run.list_scenario_runs(limit=10, state="completed")

        assert len(result) == 1
        mock_async_client.benchmarks.runs.list_scenario_runs.assert_called_once_with(
            "bench_run_123", limit=10, state="completed"
        )

    async def test_list_scenario_runs_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list_scenario_runs returns empty list when no scenario runs."""
        mock_async_client.benchmarks.runs.list_scenario_runs.return_value = AsyncIterableMock([])

        run = AsyncBenchmarkRun(mock_async_client, "bench_run_123", "bench_123")
        result = await run.list_scenario_runs()

        assert result == []
        mock_async_client.benchmarks.runs.list_scenario_runs.assert_called_once_with("bench_run_123")
