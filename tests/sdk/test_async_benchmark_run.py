"""Comprehensive tests for async AsyncBenchmarkRun class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

from tests.sdk.conftest import MockScenarioRunView, MockBenchmarkRunView
from runloop_api_client.sdk.async_scenario_run import AsyncScenarioRun
from runloop_api_client.sdk.async_benchmark_run import AsyncBenchmarkRun


class TestAsyncBenchmarkRun:
    """Tests for AsyncBenchmarkRun class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBenchmarkRun initialization."""
        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        assert run.id == "bmr_123"
        assert run.benchmark_id == "bmd_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncBenchmarkRun string representation."""
        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        assert repr(run) == "<AsyncBenchmarkRun id='bmr_123'>"

    async def test_get_info(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test get_info method."""
        mock_async_client.benchmark_runs.retrieve = AsyncMock(return_value=benchmark_run_view)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.get_info()

        assert result == benchmark_run_view
        mock_async_client.benchmark_runs.retrieve.assert_awaited_once_with("bmr_123")

    async def test_cancel(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test cancel method."""
        benchmark_run_view.state = "canceled"
        mock_async_client.benchmark_runs.cancel = AsyncMock(return_value=benchmark_run_view)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.cancel()

        assert result == benchmark_run_view
        assert result.state == "canceled"
        mock_async_client.benchmark_runs.cancel.assert_awaited_once_with("bmr_123")

    async def test_complete(self, mock_async_client: AsyncMock, benchmark_run_view: MockBenchmarkRunView) -> None:
        """Test complete method."""
        benchmark_run_view.state = "completed"
        mock_async_client.benchmark_runs.complete = AsyncMock(return_value=benchmark_run_view)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.complete()

        assert result == benchmark_run_view
        assert result.state == "completed"
        mock_async_client.benchmark_runs.complete.assert_awaited_once_with("bmr_123")

    async def test_list_scenario_runs_empty(self, mock_async_client: AsyncMock) -> None:
        """Test list_scenario_runs method with empty results."""
        page = SimpleNamespace(runs=[])
        mock_async_client.benchmark_runs.list_scenario_runs = AsyncMock(return_value=page)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.list_scenario_runs()

        assert len(result) == 0
        mock_async_client.benchmark_runs.list_scenario_runs.assert_awaited_once_with("bmr_123")

    async def test_list_scenario_runs_single(
        self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView
    ) -> None:
        """Test list_scenario_runs method with single result."""
        page = SimpleNamespace(runs=[scenario_run_view])
        mock_async_client.benchmark_runs.list_scenario_runs = AsyncMock(return_value=page)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.list_scenario_runs()

        assert len(result) == 1
        assert isinstance(result[0], AsyncScenarioRun)
        assert result[0].id == scenario_run_view.id
        assert result[0].devbox_id == scenario_run_view.devbox_id
        mock_async_client.benchmark_runs.list_scenario_runs.assert_awaited_once_with("bmr_123")

    async def test_list_scenario_runs_multiple(self, mock_async_client: AsyncMock) -> None:
        """Test list_scenario_runs method with multiple results."""
        scenario_run_view1 = MockScenarioRunView(id="scr_001", devbox_id="dev_001")
        scenario_run_view2 = MockScenarioRunView(id="scr_002", devbox_id="dev_002")
        page = SimpleNamespace(runs=[scenario_run_view1, scenario_run_view2])
        mock_async_client.benchmark_runs.list_scenario_runs = AsyncMock(return_value=page)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.list_scenario_runs()

        assert len(result) == 2
        assert isinstance(result[0], AsyncScenarioRun)
        assert isinstance(result[1], AsyncScenarioRun)
        assert result[0].id == "scr_001"
        assert result[1].id == "scr_002"
        mock_async_client.benchmark_runs.list_scenario_runs.assert_awaited_once_with("bmr_123")

    async def test_list_scenario_runs_with_params(
        self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView
    ) -> None:
        """Test list_scenario_runs method with filtering parameters."""
        page = SimpleNamespace(runs=[scenario_run_view])
        mock_async_client.benchmark_runs.list_scenario_runs = AsyncMock(return_value=page)

        run = AsyncBenchmarkRun(mock_async_client, "bmr_123", "bmd_123")
        result = await run.list_scenario_runs(limit=10, state="completed")

        assert len(result) == 1
        assert isinstance(result[0], AsyncScenarioRun)
        assert result[0].id == scenario_run_view.id
        mock_async_client.benchmark_runs.list_scenario_runs.assert_awaited_once_with(
            "bmr_123", limit=10, state="completed"
        )
