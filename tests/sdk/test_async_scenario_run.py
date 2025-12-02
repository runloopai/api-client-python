"""Comprehensive tests for async AsyncScenarioRun class."""

from __future__ import annotations

from types import SimpleNamespace
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock

import pytest

from runloop_api_client.sdk import AsyncScenarioRun


@dataclass
class MockScenarioRunView:
    """Mock ScenarioRunView for testing."""

    id: str = "run_123"
    devbox_id: str = "dev_123"
    scenario_id: str = "scn_123"
    state: str = "running"
    metadata: dict = None
    scoring_contract_result: object = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MockDevboxView:
    """Mock DevboxView for testing."""

    id: str = "dev_123"
    status: str = "running"


@pytest.fixture
def mock_async_client() -> MagicMock:
    """Create a mock AsyncRunloop client with proper async returns."""
    client = MagicMock()
    # Set up scenarios.runs resource
    client.scenarios = MagicMock()
    client.scenarios.runs = MagicMock()
    client.scenarios.runs.retrieve = AsyncMock()
    client.scenarios.runs.score = AsyncMock()
    client.scenarios.runs.await_scored = AsyncMock()
    client.scenarios.runs.score_and_await = AsyncMock()
    client.scenarios.runs.complete = AsyncMock()
    client.scenarios.runs.cancel = AsyncMock()
    # Set up devboxes resource
    client.devboxes = MagicMock()
    client.devboxes.await_running = AsyncMock()
    return client


@pytest.fixture
def scenario_run_view() -> MockScenarioRunView:
    """Create a mock ScenarioRunView."""
    return MockScenarioRunView()


@pytest.fixture
def devbox_view() -> MockDevboxView:
    """Create a mock DevboxView."""
    return MockDevboxView()


class TestAsyncScenarioRun:
    """Tests for AsyncScenarioRun class."""

    def test_init(self, mock_async_client: MagicMock) -> None:
        """Test AsyncScenarioRun initialization."""
        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        assert run.id == "run_123"
        assert run.devbox_id == "dev_123"

    def test_repr(self, mock_async_client: MagicMock) -> None:
        """Test AsyncScenarioRun string representation."""
        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        assert repr(run) == "<AsyncScenarioRun id='run_123'>"

    def test_devbox_property(self, mock_async_client: MagicMock) -> None:
        """Test devbox property returns AsyncDevbox wrapper."""
        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        devbox = run.devbox

        assert devbox.id == "dev_123"

    async def test_get_info(self, mock_async_client: MagicMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test get_info method."""
        mock_async_client.scenarios.runs.retrieve.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.get_info()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.retrieve.assert_called_once_with("run_123")

    async def test_await_env_ready(
        self,
        mock_async_client: MagicMock,
        scenario_run_view: MockScenarioRunView,
        devbox_view: MockDevboxView,
    ) -> None:
        """Test await_env_ready method."""
        mock_async_client.devboxes.await_running.return_value = devbox_view
        mock_async_client.scenarios.runs.retrieve.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.await_env_ready()

        mock_async_client.devboxes.await_running.assert_called_once_with("dev_123", polling_config=None)
        assert result == scenario_run_view

    async def test_score(self, mock_async_client: MagicMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score method."""
        scenario_run_view.state = "scoring"
        mock_async_client.scenarios.runs.score.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.score()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.score.assert_called_once_with("run_123")

    async def test_await_scored(self, mock_async_client: MagicMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test await_scored method."""
        scenario_run_view.state = "scored"
        mock_async_client.scenarios.runs.await_scored.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.await_scored()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.await_scored.assert_called_once_with("run_123", polling_config=None)

    async def test_score_and_await(self, mock_async_client: MagicMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test score_and_await method."""
        scenario_run_view.state = "scored"
        mock_async_client.scenarios.runs.score_and_await.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.score_and_await()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.score_and_await.assert_called_once_with("run_123", polling_config=None)

    async def test_complete(self, mock_async_client: MagicMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test complete method."""
        scenario_run_view.state = "completed"
        mock_async_client.scenarios.runs.complete.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.complete()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.complete.assert_called_once_with("run_123")

    async def test_cancel(self, mock_async_client: MagicMock, scenario_run_view: MockScenarioRunView) -> None:
        """Test cancel method."""
        scenario_run_view.state = "canceled"
        mock_async_client.scenarios.runs.cancel.return_value = scenario_run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.cancel()

        assert result == scenario_run_view
        mock_async_client.scenarios.runs.cancel.assert_called_once_with("run_123")

    async def test_get_score_when_scored(self, mock_async_client: MagicMock) -> None:
        """Test get_score returns scoring result when scored."""
        scoring_result = SimpleNamespace(score=0.95, scoring_function_results=[])
        run_view = MockScenarioRunView(state="scored", scoring_contract_result=scoring_result)
        mock_async_client.scenarios.runs.retrieve.return_value = run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.get_score()

        assert result == scoring_result
        assert result.score == 0.95

    async def test_get_score_when_not_scored(self, mock_async_client: MagicMock) -> None:
        """Test get_score returns None when not scored."""
        run_view = MockScenarioRunView(state="running", scoring_contract_result=None)
        mock_async_client.scenarios.runs.retrieve.return_value = run_view

        run = AsyncScenarioRun(mock_async_client, "run_123", "dev_123")
        result = await run.get_score()

        assert result is None
