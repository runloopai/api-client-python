"""Comprehensive tests for async AsyncScenario class."""

from __future__ import annotations

from unittest.mock import AsyncMock

from tests.sdk.conftest import MockScenarioView, MockScenarioRunView
from runloop_api_client.sdk import AsyncScenario


class TestAsyncScenario:
    """Tests for AsyncScenario class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncScenario initialization."""
        scenario = AsyncScenario(mock_async_client, "scn_123")
        assert scenario.id == "scn_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncScenario string representation."""
        scenario = AsyncScenario(mock_async_client, "scn_123")
        assert repr(scenario) == "<AsyncScenario id='scn_123'>"

    async def test_get_info(self, mock_async_client: AsyncMock, scenario_view: MockScenarioView) -> None:
        """Test get_info method."""
        mock_async_client.scenarios.retrieve = AsyncMock(return_value=scenario_view)

        scenario = AsyncScenario(mock_async_client, "scn_123")
        result = await scenario.get_info()

        assert result == scenario_view
        mock_async_client.scenarios.retrieve.assert_awaited_once_with("scn_123")

    async def test_update(self, mock_async_client: AsyncMock, scenario_view: MockScenarioView) -> None:
        """Test update method."""
        mock_async_client.scenarios.update = AsyncMock(return_value=scenario_view)

        scenario = AsyncScenario(mock_async_client, "scn_123")
        result = await scenario.update(name="new-name", metadata={"key": "value"})

        assert result == scenario_view
        mock_async_client.scenarios.update.assert_awaited_once_with(
            "scn_123",
            name="new-name",
            metadata={"key": "value"},
        )

    async def test_run(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run method returns AsyncScenarioRun wrapper."""
        mock_async_client.scenarios.start_run = AsyncMock(return_value=scenario_run_view)

        scenario = AsyncScenario(mock_async_client, "scn_123")
        run = await scenario.run(run_name="test-run")

        assert run.id == "run_123"
        assert run.devbox_id == "dev_123"
        mock_async_client.scenarios.start_run.assert_awaited_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )

    async def test_run_and_await_env_ready(
        self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView
    ) -> None:
        """Test run_and_await_env_ready method."""
        mock_async_client.scenarios.start_run_and_await_env_ready = AsyncMock(return_value=scenario_run_view)

        scenario = AsyncScenario(mock_async_client, "scn_123")
        run = await scenario.run_and_await_env_ready(run_name="test-run")

        assert run.id == "run_123"
        assert run.devbox_id == "dev_123"
        mock_async_client.scenarios.start_run_and_await_env_ready.assert_awaited_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )
