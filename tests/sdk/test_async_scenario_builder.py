"""Unit tests for AsyncScenarioBuilder class."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from runloop_api_client.sdk.async_snapshot import AsyncSnapshot
from runloop_api_client.sdk.async_blueprint import AsyncBlueprint
from runloop_api_client.sdk.async_scenario_builder import AsyncScenarioBuilder


class TestAsyncScenarioBuilder:
    """Tests for the asynchronous AsyncScenarioBuilder."""

    @pytest.fixture
    def mock_async_client(self) -> MagicMock:
        """Create a mock AsyncRunloop client."""
        client = MagicMock()
        client.scenarios = MagicMock()
        client.scenarios.create = AsyncMock()
        return client

    @pytest.fixture
    def mock_blueprint(self, mock_async_client: MagicMock) -> AsyncBlueprint:
        """Create a mock AsyncBlueprint object."""
        return AsyncBlueprint(mock_async_client, "bp-123")

    @pytest.fixture
    def mock_snapshot(self, mock_async_client: MagicMock) -> AsyncSnapshot:
        """Create a mock AsyncSnapshot object."""
        return AsyncSnapshot(mock_async_client, "snap-123")

    @pytest.fixture
    def builder(self, mock_async_client: MagicMock) -> AsyncScenarioBuilder:
        """Create an AsyncScenarioBuilder instance with mock client."""
        return AsyncScenarioBuilder(mock_async_client, "test-scenario")

    def test_init(self, mock_async_client: MagicMock) -> None:
        """Test builder initialization."""
        builder = AsyncScenarioBuilder(mock_async_client, "my-scenario")

        assert builder._client is mock_async_client
        assert builder._name == "my-scenario"
        assert builder.name == "my-scenario"

    def test_repr(self, builder: AsyncScenarioBuilder) -> None:
        """Test builder __repr__."""
        assert repr(builder) == "<AsyncScenarioBuilder name='test-scenario'>"

    def test_from_blueprint_returns_self(self, builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint) -> None:
        """Test from_blueprint returns self for chaining."""
        result = builder.from_blueprint(mock_blueprint)

        assert result is builder
        assert builder._blueprint is mock_blueprint
        assert builder._snapshot is None

    def test_from_snapshot_returns_self(self, builder: AsyncScenarioBuilder, mock_snapshot: AsyncSnapshot) -> None:
        """Test from_snapshot returns self for chaining."""
        result = builder.from_snapshot(mock_snapshot)

        assert result is builder
        assert builder._snapshot is mock_snapshot
        assert builder._blueprint is None

    def test_with_working_directory_returns_self(self, builder: AsyncScenarioBuilder) -> None:
        """Test with_working_directory returns self for chaining."""
        result = builder.with_working_directory("/app")

        assert result is builder
        assert builder._working_directory == "/app"

    def test_with_problem_statement_returns_self(self, builder: AsyncScenarioBuilder) -> None:
        """Test with_problem_statement returns self for chaining."""
        result = builder.with_problem_statement("Fix the bug")

        assert result is builder
        assert builder._problem_statement == "Fix the bug"

    def test_add_test_scorer(self, builder: AsyncScenarioBuilder) -> None:
        """Test add_test_scorer method."""
        result = builder.add_test_scorer(
            "my-tests",
            test_command="pytest",
            weight=2.0,
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["name"] == "my-tests"
        assert builder._scorers[0]["scorer"]["type"] == "test_based_scorer"

    def test_add_command_scorer(self, builder: AsyncScenarioBuilder) -> None:
        """Test add_command_scorer method."""
        result = builder.add_command_scorer(
            "cmd-scorer",
            command="./check.sh",
        )

        assert result is builder
        assert builder._scorers[0]["scorer"]["type"] == "command_scorer"

    def test_add_bash_scorer(self, builder: AsyncScenarioBuilder) -> None:
        """Test add_bash_scorer method."""
        result = builder.add_bash_scorer(
            "bash-scorer",
            bash_script="echo 'score=1.0'",
        )

        assert result is builder
        assert builder._scorers[0]["scorer"]["type"] == "bash_script_scorer"

    def test_build_params_missing_problem_statement(self, builder: AsyncScenarioBuilder) -> None:
        """Test _build_params raises if problem statement is missing."""
        builder.add_test_scorer("test", test_command="pytest")

        with pytest.raises(ValueError, match="Problem statement is required"):
            builder._build_params()

    def test_build_params_missing_scorer(self, builder: AsyncScenarioBuilder) -> None:
        """Test _build_params raises if no scorers are added."""
        builder.with_problem_statement("Fix the bug")

        with pytest.raises(ValueError, match="At least one scorer is required"):
            builder._build_params()

    def test_build_params_minimal(self, builder: AsyncScenarioBuilder) -> None:
        """Test _build_params with minimal configuration."""
        builder.with_problem_statement("Fix the bug")
        builder.add_test_scorer("tests", test_command="pytest")

        params = builder._build_params()

        assert params["name"] == "test-scenario"
        assert params["input_context"]["problem_statement"] == "Fix the bug"
        assert len(params["scoring_contract"]["scoring_function_parameters"]) == 1

    def test_build_params_with_environment(self, builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint) -> None:
        """Test _build_params includes environment parameters."""
        builder.with_problem_statement("Fix the bug")
        builder.add_test_scorer("tests", test_command="pytest")
        builder.from_blueprint(mock_blueprint)
        builder.with_working_directory("/app")

        params = builder._build_params()

        assert params["environment_parameters"]["blueprint_id"] == "bp-123"
        assert params["environment_parameters"]["working_directory"] == "/app"

    @pytest.mark.asyncio
    async def test_push_calls_api_and_returns_scenario(
        self, builder: AsyncScenarioBuilder, mock_async_client: MagicMock
    ) -> None:
        """Test push() calls API with correct params and returns AsyncScenario."""
        mock_async_client.scenarios.create.return_value.id = "scn-new-123"

        builder.with_problem_statement("Fix the bug")
        builder.add_test_scorer("tests", test_command="pytest")

        scenario = await builder.push()

        mock_async_client.scenarios.create.assert_called_once()
        call_kwargs = mock_async_client.scenarios.create.call_args.kwargs
        assert call_kwargs["name"] == "test-scenario"
        assert call_kwargs["input_context"]["problem_statement"] == "Fix the bug"

        assert scenario.id == "scn-new-123"

    def test_fluent_chaining(self, builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint) -> None:
        """Test that all builder methods can be chained fluently."""
        result = (
            builder.from_blueprint(mock_blueprint)
            .with_working_directory("/app")
            .with_problem_statement("Fix the bug")
            .with_additional_context({"hint": "check main.py"})
            .add_test_scorer("tests", test_command="pytest")
            .with_metadata({"team": "infra"})
            .with_reference_output("diff content")
            .with_required_env_vars(["API_KEY"])
            .with_required_secrets(["secret"])
            .with_validation_type("FORWARD")
        )

        assert result is builder
        assert builder._blueprint is mock_blueprint
        assert builder._working_directory == "/app"
        assert builder._problem_statement == "Fix the bug"
        assert len(builder._scorers) == 1
