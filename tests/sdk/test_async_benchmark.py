"""Comprehensive tests for async AsyncBenchmark class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

from tests.sdk.conftest import MockBenchmarkView, MockBenchmarkRunView
from runloop_api_client.sdk.async_benchmark import AsyncBenchmark
from runloop_api_client.sdk.async_benchmark_run import AsyncBenchmarkRun


class TestAsyncBenchmark:
    """Tests for AsyncBenchmark class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBenchmark initialization."""
        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        assert benchmark.id == "bmd_123"
        assert repr(benchmark) == "<AsyncBenchmark id='bmd_123'>"

    async def test_get_info(self, mock_async_client: AsyncMock, benchmark_view: MockBenchmarkView) -> None:
        """Test get_info method."""
        mock_async_client.benchmarks.retrieve = AsyncMock(return_value=benchmark_view)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.get_info()

        assert result == benchmark_view
        mock_async_client.benchmarks.retrieve.assert_awaited_once_with("bmd_123")

    async def test_update(self, mock_async_client: AsyncMock, benchmark_view: MockBenchmarkView) -> None:
        """Test update method."""
        benchmark_view.name = "updated-name"
        mock_async_client.benchmarks.update = AsyncMock(return_value=benchmark_view)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.update(name="updated-name")

        assert result == benchmark_view
        mock_async_client.benchmarks.update.assert_awaited_once_with("bmd_123", name="updated-name")

    async def test_run(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test run method."""
        mock_async_client.benchmarks.start_run = AsyncMock(return_value=benchmark_run_view)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.start_run(run_name="test-run", metadata={"key": "value"})

        assert isinstance(result, AsyncBenchmarkRun)
        assert result.id == benchmark_run_view.id
        assert result.benchmark_id == benchmark_run_view.benchmark_id
        mock_async_client.benchmarks.start_run.assert_awaited_once_with(
            benchmark_id="bmd_123", run_name="test-run", metadata={"key": "value"}
        )

    async def test_add_scenarios(self, mock_async_client: AsyncMock, benchmark_view: MockBenchmarkView) -> None:
        """Test add_scenarios method."""
        benchmark_view.scenario_ids = ["scn_001", "scn_002"]
        mock_async_client.benchmarks.update_scenarios = AsyncMock(return_value=benchmark_view)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.add_scenarios(["scn_001", "scn_002"])

        assert result == benchmark_view
        mock_async_client.benchmarks.update_scenarios.assert_awaited_once_with(
            "bmd_123", scenarios_to_add=["scn_001", "scn_002"]
        )

    async def test_remove_scenarios(self, mock_async_client: AsyncMock, benchmark_view: MockBenchmarkView) -> None:
        """Test remove_scenarios method."""
        mock_async_client.benchmarks.update_scenarios = AsyncMock(return_value=benchmark_view)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.remove_scenarios(["scn_001"])

        assert result == benchmark_view
        mock_async_client.benchmarks.update_scenarios.assert_awaited_once_with(
            "bmd_123", scenarios_to_remove=["scn_001"]
        )

    async def test_list_runs_single(
        self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView
    ) -> None:
        """Test list_runs method with single result."""
        page = SimpleNamespace(runs=[benchmark_run_view])
        mock_async_client.benchmark_runs.list = AsyncMock(return_value=page)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.list_runs()

        assert len(result) == 1
        assert isinstance(result[0], AsyncBenchmarkRun)
        assert result[0].id == benchmark_run_view.id
        assert result[0].benchmark_id == benchmark_run_view.benchmark_id
        mock_async_client.benchmark_runs.list.assert_awaited_once_with(benchmark_id="bmd_123")

    async def test_list_runs_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list_runs method with multiple results."""
        run_view1 = MockBenchmarkRunView(id="bmr_001")
        run_view2 = MockBenchmarkRunView(id="bmr_002")
        page = SimpleNamespace(runs=[run_view1, run_view2])
        mock_async_client.benchmark_runs.list = AsyncMock(return_value=page)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.list_runs()

        assert len(result) == 2
        assert isinstance(result[0], AsyncBenchmarkRun)
        assert isinstance(result[1], AsyncBenchmarkRun)
        assert result[0].id == run_view1.id
        assert result[0].benchmark_id == run_view1.benchmark_id
        assert result[1].id == run_view2.id
        assert result[1].benchmark_id == run_view2.benchmark_id
        mock_async_client.benchmark_runs.list.assert_awaited_once_with(benchmark_id="bmd_123")

    async def test_list_runs_with_params(
        self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView
    ) -> None:
        """Test list_runs method with filtering parameters."""
        page = SimpleNamespace(runs=[benchmark_run_view])
        mock_async_client.benchmark_runs.list = AsyncMock(return_value=page)

        benchmark = AsyncBenchmark(mock_async_client, "bmd_123")
        result = await benchmark.list_runs(limit=10, name="test-run")

        assert len(result) == 1
        mock_async_client.benchmark_runs.list.assert_awaited_once_with(
            benchmark_id="bmd_123", limit=10, name="test-run"
        )
