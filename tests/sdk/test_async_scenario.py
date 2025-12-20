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
        result = await scenario.update(
            name="updated-scenario",
            metadata={"env": "test"},
            environment_parameters={
                "blueprint_id": "bp_456",
            },
            input_context={
                "problem_statement": "Updated problem statement",
            },
            reference_output="--- a/main.py\n+++ b/main.py\n@@ -1 +1 @@\n-old\n+new",
            required_environment_variables=["API_KEY", "DEBUG"],
            required_secret_names=["DB_PASSWORD", "JWT_SECRET"],
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "test-scorer",
                        "scorer": {
                            "type": "command_scorer",
                            "command": "echo 'score=1.0'",
                        },
                        "weight": 1.0,
                    }
                ],
            },
            validation_type="FORWARD",
        )

        assert result == scenario_view
        mock_async_client.scenarios.update.assert_awaited_once_with(
            "scn_123",
            name="updated-scenario",
            metadata={"env": "test"},
            environment_parameters={
                "blueprint_id": "bp_456",
            },
            input_context={
                "problem_statement": "Updated problem statement",
            },
            reference_output="--- a/main.py\n+++ b/main.py\n@@ -1 +1 @@\n-old\n+new",
            required_environment_variables=["API_KEY", "DEBUG"],
            required_secret_names=["DB_PASSWORD", "JWT_SECRET"],
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "test-scorer",
                        "scorer": {
                            "type": "command_scorer",
                            "command": "echo 'score=1.0'",
                        },
                        "weight": 1.0,
                    }
                ],
            },
            validation_type="FORWARD",
        )

    async def test_run_async(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run_async method returns AsyncScenarioRun wrapper."""
        mock_async_client.scenarios.start_run = AsyncMock(return_value=scenario_run_view)

        scenario = AsyncScenario(mock_async_client, "scn_123")
        run = await scenario.run_async(run_name="test-run")

        assert run.id == "scr_123"
        assert run.devbox_id == "dbx_123"
        mock_async_client.scenarios.start_run.assert_awaited_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )

    async def test_run(self, mock_async_client: AsyncMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test run method."""
        mock_async_client.scenarios.start_run_and_await_env_ready = AsyncMock(return_value=scenario_run_view)

        scenario = AsyncScenario(mock_async_client, "scn_123")
        run = await scenario.run(run_name="test-run")

        assert run.id == "scr_123"
        assert run.devbox_id == "dbx_123"
        mock_async_client.scenarios.start_run_and_await_env_ready.assert_awaited_once_with(
            scenario_id="scn_123",
            run_name="test-run",
        )
