"""Comprehensive tests for async AsyncScenarioRun class."""

from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
from unittest.mock import AsyncMock

from tests.sdk.conftest import MockDevboxView, MockScenarioRunView
from runloop_api_client.sdk import AsyncScenarioRun


class TestAsyncScenarioRun:
    """Tests for AsyncScenarioRun class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncScenarioRun initialization."""
        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        assert run.id == "scr_123"
        assert run.devbox_id == "dbx_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncScenarioRun string representation."""
        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        assert repr(run) == "<AsyncScenarioRun id='scr_123'>"

    def test_devbox_property(self, mock_async_client: AsyncMock) -> None:
        """Test devbox property returns AsyncDevbox wrapper."""
        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        devbox = run.devbox

        assert devbox.id == "dbx_123"

    async def test_get_info(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test get_info method."""
        mock_async_client.scenarios.runs.retrieve = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.get_info()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.retrieve.assert_awaited_once_with("scr_123")

    async def test_await_env_ready(
        self,
        mock_async_client: AsyncMock,
        scenario_run_view: MockScenarioRunView,
        devbox_view: MockDevboxView,
    ) -> None:
        """Test await_env_ready method."""
        mock_async_client.devboxes.await_running = AsyncMock(return_value=devbox_view)
        mock_async_client.scenarios.runs.retrieve = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.await_env_ready()

        mock_async_client.devboxes.await_running.assert_awaited_once_with("dbx_123", polling_config=None)
        assert result == scenario_run_view

    async def test_score(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score method."""
        scenario_run_view.state = "scoring"
        mock_async_client.scenarios.runs.score = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.score()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.score.assert_awaited_once_with("scr_123")

    async def test_await_scored(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test await_scored method."""
        scenario_run_view.state = "scored"
        mock_async_client.scenarios.runs.await_scored = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.await_scored()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.await_scored.assert_awaited_once_with("scr_123")

    async def test_score_and_await(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score_and_await method."""
        scenario_run_view.state = "scored"
        mock_async_client.scenarios.runs.score_and_await = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.score_and_await()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.score_and_await.assert_awaited_once_with("scr_123")

    async def test_score_and_complete(
        self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView
    ) -> None:
        """Test score_and_complete method."""
        scenario_run_view.state = "completed"
        mock_async_client.scenarios.runs.score_and_complete = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.score_and_complete()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.score_and_complete.assert_awaited_once_with("scr_123")

    async def test_complete(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test complete method."""
        scenario_run_view.state = "completed"
        mock_async_client.scenarios.runs.complete = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.complete()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.complete.assert_awaited_once_with("scr_123")

    async def test_cancel(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test cancel method."""
        scenario_run_view.state = "canceled"
        mock_async_client.scenarios.runs.cancel = AsyncMock(return_value=scenario_run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.cancel()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.cancel.assert_awaited_once_with("scr_123")

    async def test_download_logs(self, mock_async_client: AsyncMock, tmp_path: Path) -> None:
        """Test download_logs method writes to file."""
        mock_response = AsyncMock()
        mock_response.write_to_file = AsyncMock()
        mock_async_client.scenarios.runs.download_logs = AsyncMock(return_value=mock_response)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        output_path = tmp_path / "logs.zip"
        await run.download_logs(output_path)

        mock_async_client.scenarios.runs.download_logs.assert_awaited_once_with("scr_123")
        mock_response.write_to_file.assert_awaited_once_with(output_path)

    async def test_get_score_when_scored(self, mock_async_client: AsyncMock) -> None:
        """Test get_score returns scoring result when scored."""
        scoring_result = SimpleNamespace(score=0.95, scoring_function_results=[])
        run_view = MockScenarioRunView(state="scored", scoring_contract_result=scoring_result)
        mock_async_client.scenarios.runs.retrieve = AsyncMock(return_value=run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.get_score()

        assert result == scoring_result
        mock_async_client.scenarios.runs.retrieve.assert_awaited_once_with("scr_123")

    async def test_get_score_when_not_scored(self, mock_async_client: AsyncMock) -> None:
        """Test get_score returns None when not scored."""
        run_view = MockScenarioRunView(state="running", scoring_contract_result=None)
        mock_async_client.scenarios.runs.retrieve = AsyncMock(return_value=run_view)

        run = AsyncScenarioRun(mock_async_client, "scr_123", "dbx_123")
        result = await run.get_score()

        assert result is None
        mock_async_client.scenarios.runs.retrieve.assert_awaited_once_with("scr_123")
