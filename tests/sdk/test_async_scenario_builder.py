"""Unit tests for AsyncScenarioBuilder class."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from runloop_api_client.sdk import AsyncSnapshot, AsyncBlueprint, ScenarioPreview, AsyncScenarioBuilder
from runloop_api_client.types.scoring_function_param import ScorerTestBasedScoringFunctionTestFile


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
    def mock_builder(self, mock_async_client: MagicMock) -> AsyncScenarioBuilder:
        """Create an AsyncScenarioBuilder instance with mock client."""
        return AsyncScenarioBuilder("test-scenario", mock_async_client)

    def test_instantiation(self, mock_async_client: MagicMock) -> None:
        """Test builder initialization and repr."""
        builder = AsyncScenarioBuilder("my-scenario", mock_async_client)

        assert builder._client is mock_async_client
        assert builder._name == "my-scenario"
        assert builder.name == "my-scenario"
        assert repr(builder) == "<AsyncScenarioBuilder name='my-scenario'>"

    def test_from_blueprint_and_snapshot(
        self, mock_builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint, mock_snapshot: AsyncSnapshot
    ) -> None:
        """Test blueprint/snapshot setting returns self and are mutually exclusive."""
        # from_blueprint returns self and sets blueprint
        result = mock_builder.from_blueprint(mock_blueprint)
        assert result is mock_builder
        assert mock_builder._blueprint is mock_blueprint
        assert mock_builder._snapshot is None

        # from_snapshot returns self, sets snapshot, and clears blueprint
        result = mock_builder.from_snapshot(mock_snapshot)
        assert result is mock_builder
        assert mock_builder._snapshot is mock_snapshot
        assert mock_builder._blueprint is None

        # from_blueprint clears snapshot
        mock_builder.from_blueprint(mock_blueprint)
        assert mock_builder._blueprint is mock_blueprint
        assert mock_builder._snapshot is None

    def test_scorers(self, mock_builder: AsyncScenarioBuilder) -> None:
        """Test all scorer types, optional params, and multiple scorers."""
        # Test scorer with test files
        test_files: list[ScorerTestBasedScoringFunctionTestFile] = [
            {"file_path": "test_main.py", "file_contents": "def test_foo(): pass"}
        ]
        result = mock_builder.add_test_command_scorer(
            "test-scorer", test_command="pytest", weight=2.0, test_files=test_files
        )
        assert result is mock_builder
        assert mock_builder._scorers[0]["name"] == "test-scorer"
        assert mock_builder._scorers[0]["weight"] == 2.0
        assert mock_builder._scorers[0]["scorer"]["type"] == "test_based_scorer"
        assert mock_builder._scorers[0]["scorer"].get("test_command") == "pytest"
        assert mock_builder._scorers[0]["scorer"].get("test_files") == test_files

        # Command scorer
        mock_builder.add_shell_command_scorer("cmd-scorer", command="./check.sh")
        assert mock_builder._scorers[1]["scorer"]["type"] == "command_scorer"
        assert mock_builder._scorers[1]["scorer"].get("command") == "./check.sh"

        # Bash scorer
        mock_builder.add_bash_script_scorer("bash-scorer", bash_script="echo 'score=1.0'")
        assert mock_builder._scorers[2]["scorer"]["type"] == "bash_script_scorer"
        assert mock_builder._scorers[2]["scorer"].get("bash_script") == "echo 'score=1.0'"

        # Python scorer with optional params
        mock_builder.add_python_script_scorer(
            "python-scorer",
            python_script="print('1.0')",
            python_version_constraint=">=3.10",
            requirements_contents="numpy",
        )
        assert mock_builder._scorers[3]["scorer"]["type"] == "python_script_scorer"
        assert mock_builder._scorers[3]["scorer"].get("python_version_constraint") == ">=3.10"
        assert mock_builder._scorers[3]["scorer"].get("requirements_contents") == "numpy"

        # AST grep scorer with optional lang
        mock_builder.add_ast_grep_scorer("ast-scorer", pattern="$A.foo()", search_directory="/src", lang="python")
        assert mock_builder._scorers[4]["scorer"]["type"] == "ast_grep_scorer"
        assert mock_builder._scorers[4]["scorer"].get("pattern") == "$A.foo()"
        assert mock_builder._scorers[4]["scorer"].get("lang") == "python"

        # Custom scorer with optional params
        mock_builder.add_custom_scorer(
            "custom-scorer", custom_scorer_type="my_scorer", scorer_params={"threshold": 0.5}
        )
        assert mock_builder._scorers[5]["scorer"]["type"] == "custom_scorer"
        assert mock_builder._scorers[5]["scorer"].get("custom_scorer_type") == "my_scorer"
        assert mock_builder._scorers[5]["scorer"].get("scorer_params") == {"threshold": 0.5}

        # Verify multiple scorers accumulated
        assert len(mock_builder._scorers) == 6

    def test_add_scorer_rejects_invalid_weight(self, mock_builder: AsyncScenarioBuilder) -> None:
        """Test that adding a scorer with zero or negative weight raises ValueError."""
        with pytest.raises(ValueError, match="Scorer weight must be positive"):
            mock_builder.add_bash_script_scorer("bad", bash_script="echo 1", weight=0.0)

        with pytest.raises(ValueError, match="Scorer weight must be positive"):
            mock_builder.add_bash_script_scorer("bad", bash_script="echo 1", weight=-1.0)

    def test_build_validation(self, mock_builder: AsyncScenarioBuilder) -> None:
        """Test build raises for missing required fields."""
        # Missing problem statement
        mock_builder.add_test_command_scorer("test", test_command="pytest")
        with pytest.raises(ValueError, match="Problem statement is required"):
            mock_builder.build()

        # Missing scorer (new builder)
        builder2 = AsyncScenarioBuilder("test2", mock_builder._client)
        builder2.with_problem_statement("Fix the bug")
        with pytest.raises(ValueError, match="At least one scorer is required"):
            builder2.build()

    def test_build_with_all_options(self, mock_builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint) -> None:
        """Test build with all optional fields set."""
        mock_builder.with_problem_statement("Fix the bug")
        mock_builder.with_additional_context({"hint": "line 42"})
        mock_builder.add_test_command_scorer("tests", test_command="pytest")
        mock_builder.from_blueprint(mock_blueprint)
        mock_builder.with_working_directory("/app")
        mock_builder.with_metadata({"team": "infra"})
        mock_builder.with_reference_output("diff content")
        mock_builder.with_required_env_vars(["API_KEY"])
        mock_builder.with_required_secrets(["db_pass"])
        mock_builder.with_validation_type("FORWARD")

        params = mock_builder.build()

        assert params["name"] == "test-scenario"
        assert params["input_context"]["problem_statement"] == "Fix the bug"
        assert params["input_context"].get("additional_context") == {"hint": "line 42"}
        env_params = params.get("environment_parameters")
        assert env_params is not None
        assert env_params.get("blueprint_id") == "bp-123"
        assert env_params.get("working_directory") == "/app"
        assert params.get("metadata") == {"team": "infra"}
        assert params.get("reference_output") == "diff content"
        assert params.get("required_environment_variables") == ["API_KEY"]
        assert params.get("required_secret_names") == ["db_pass"]
        assert params.get("validation_type") == "FORWARD"

    def test_build_normalizes_weights(self, mock_builder: AsyncScenarioBuilder) -> None:
        """Test that build normalizes scorer weights to sum to 1.0."""
        mock_builder.with_problem_statement("Fix the bug")
        mock_builder.add_bash_script_scorer("scorer1", bash_script="echo 1", weight=1.0)
        mock_builder.add_bash_script_scorer("scorer2", bash_script="echo 2", weight=2.0)
        mock_builder.add_bash_script_scorer("scorer3", bash_script="echo 3", weight=3.0)

        params = mock_builder.build()
        scorers = list(params["scoring_contract"]["scoring_function_parameters"])

        # Weights 1, 2, 3 should normalize to 1/6, 2/6, 3/6
        assert len(scorers) == 3
        assert abs(scorers[0]["weight"] - 1 / 6) < 0.0001
        assert abs(scorers[1]["weight"] - 2 / 6) < 0.0001
        assert abs(scorers[2]["weight"] - 3 / 6) < 0.0001

        # Total should be 1.0
        total = sum(s["weight"] for s in scorers)
        assert abs(total - 1.0) < 0.0001

    @pytest.mark.asyncio
    async def test_push_calls_api_and_returns_scenario(
        self, mock_builder: AsyncScenarioBuilder, mock_async_client: MagicMock
    ) -> None:
        """Test push() calls API with correct params and returns AsyncScenario."""
        mock_async_client.scenarios.create.return_value.id = "scn-new-123"

        mock_builder.with_problem_statement("Fix the bug")
        mock_builder.add_test_command_scorer("tests", test_command="pytest")

        scenario = await mock_builder.push()

        mock_async_client.scenarios.create.assert_called_once()
        call_kwargs = mock_async_client.scenarios.create.call_args.kwargs
        assert call_kwargs["name"] == "test-scenario"
        assert call_kwargs["input_context"]["problem_statement"] == "Fix the bug"

        assert scenario.id == "scn-new-123"

    def test_fluent_chaining(self, mock_builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint) -> None:
        """Test that all builder methods can be chained fluently."""
        result = (
            mock_builder.from_blueprint(mock_blueprint)
            .with_working_directory("/app")
            .with_problem_statement("Fix the bug")
            .with_additional_context({"hint": "check main.py"})
            .add_test_command_scorer("tests", test_command="pytest")
            .with_metadata({"team": "infra"})
            .with_reference_output("diff content")
            .with_required_env_vars(["API_KEY"])
            .with_required_secrets(["secret"])
            .with_validation_type("FORWARD")
        )

        assert result is mock_builder
        assert mock_builder._blueprint is mock_blueprint
        assert mock_builder._working_directory == "/app"
        assert mock_builder._problem_statement == "Fix the bug"
        assert len(mock_builder._scorers) == 1

    def test_preview_with_no_config(self, mock_builder: AsyncScenarioBuilder) -> None:
        """Test preview() works with no configuration (only name from constructor)."""
        preview = mock_builder.preview()

        assert isinstance(preview, ScenarioPreview)
        assert preview.name == "test-scenario"
        assert preview.input_context is not None
        assert preview.input_context.problem_statement is None
        assert preview.input_context.additional_context is None
        assert preview.scoring_contract is not None
        assert len(preview.scoring_contract.scoring_function_parameters) == 0
        assert preview.environment is None
        assert len(preview.metadata) == 0
        assert preview.reference_output is None
        assert preview.required_environment_variables is None
        assert preview.required_secret_names is None
        assert preview.validation_type is None

    def test_preview_with_full_config(self, mock_builder: AsyncScenarioBuilder, mock_blueprint: AsyncBlueprint) -> None:
        """Test preview() with all fields configured, including weight normalization."""
        mock_builder.with_problem_statement("Fix the bug")
        mock_builder.with_additional_context({"hint": "line 42"})
        mock_builder.from_blueprint(mock_blueprint)
        mock_builder.with_working_directory("/app")
        mock_builder.with_metadata({"team": "infra"})
        mock_builder.with_reference_output("diff content")
        mock_builder.with_required_env_vars(["API_KEY"])
        mock_builder.with_required_secrets(["db_pass"])
        mock_builder.with_validation_type("FORWARD")
        # Add multiple scorers with different weights to test normalization
        mock_builder.add_bash_script_scorer("scorer1", bash_script="echo 1", weight=1.0)
        mock_builder.add_bash_script_scorer("scorer2", bash_script="echo 2", weight=2.0)
        mock_builder.add_bash_script_scorer("scorer3", bash_script="echo 3", weight=3.0)

        preview = mock_builder.preview()

        # Verify it returns ScenarioPreview
        assert isinstance(preview, ScenarioPreview)

        # Verify all fields are populated
        assert preview.name == "test-scenario"
        assert preview.input_context is not None
        assert preview.input_context.problem_statement == "Fix the bug"
        assert preview.input_context.additional_context == {"hint": "line 42"}
        assert preview.environment is not None
        assert preview.environment.blueprint_id == "bp-123"
        assert preview.environment.working_directory == "/app"
        assert preview.metadata == {"team": "infra"}
        assert preview.reference_output == "diff content"
        assert preview.required_environment_variables == ["API_KEY"]
        assert preview.required_secret_names == ["db_pass"]
        assert preview.validation_type == "FORWARD"

        # Verify weights are normalized (1, 2, 3 -> 1/6, 2/6, 3/6)
        assert preview.scoring_contract is not None
        scorers = preview.scoring_contract.scoring_function_parameters
        assert len(scorers) == 3
        assert abs(scorers[0].weight - 1 / 6) < 0.0001
        assert abs(scorers[1].weight - 2 / 6) < 0.0001
        assert abs(scorers[2].weight - 3 / 6) < 0.0001
        assert abs(sum(s.weight for s in scorers) - 1.0) < 0.0001
