"""Unit tests for ScenarioBuilder class."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from runloop_api_client.sdk.snapshot import Snapshot
from runloop_api_client.sdk.blueprint import Blueprint
from runloop_api_client.sdk.scenario_builder import ScenarioBuilder
from runloop_api_client.types.scoring_function_param import ScorerTestBasedScoringFunctionTestFile


class TestScenarioBuilder:
    """Tests for the synchronous ScenarioBuilder."""

    @pytest.fixture
    def mock_client(self) -> MagicMock:
        """Create a mock Runloop client."""
        client = MagicMock()
        return client

    @pytest.fixture
    def mock_blueprint(self, mock_client: MagicMock) -> Blueprint:
        """Create a mock Blueprint object."""
        return Blueprint(mock_client, "bp-123")

    @pytest.fixture
    def mock_snapshot(self, mock_client: MagicMock) -> Snapshot:
        """Create a mock Snapshot object."""
        return Snapshot(mock_client, "snap-123")

    @pytest.fixture
    def builder(self, mock_client: MagicMock) -> ScenarioBuilder:
        """Create a ScenarioBuilder instance with mock client."""
        return ScenarioBuilder(mock_client, "test-scenario")

    def test_init(self, mock_client: MagicMock) -> None:
        """Test builder initialization."""
        builder = ScenarioBuilder(mock_client, "my-scenario")

        assert builder._client is mock_client
        assert builder._name == "my-scenario"
        assert builder.name == "my-scenario"

    def test_repr(self, builder: ScenarioBuilder) -> None:
        """Test builder __repr__."""
        assert repr(builder) == "<ScenarioBuilder name='test-scenario'>"

    def test_from_blueprint_returns_self(self, builder: ScenarioBuilder, mock_blueprint: Blueprint) -> None:
        """Test from_blueprint returns self for chaining."""
        result = builder.from_blueprint(mock_blueprint)

        assert result is builder
        assert builder._blueprint is mock_blueprint
        assert builder._snapshot is None

    def test_from_snapshot_returns_self(self, builder: ScenarioBuilder, mock_snapshot: Snapshot) -> None:
        """Test from_snapshot returns self for chaining."""
        result = builder.from_snapshot(mock_snapshot)

        assert result is builder
        assert builder._snapshot is mock_snapshot
        assert builder._blueprint is None

    def test_from_blueprint_clears_snapshot(
        self, builder: ScenarioBuilder, mock_blueprint: Blueprint, mock_snapshot: Snapshot
    ) -> None:
        """Test that setting blueprint clears snapshot."""
        builder.from_snapshot(mock_snapshot)
        builder.from_blueprint(mock_blueprint)

        assert builder._blueprint is mock_blueprint
        assert builder._snapshot is None

    def test_from_snapshot_clears_blueprint(
        self, builder: ScenarioBuilder, mock_blueprint: Blueprint, mock_snapshot: Snapshot
    ) -> None:
        """Test that setting snapshot clears blueprint."""
        builder.from_blueprint(mock_blueprint)
        builder.from_snapshot(mock_snapshot)

        assert builder._snapshot is mock_snapshot
        assert builder._blueprint is None

    def test_with_working_directory_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_working_directory returns self for chaining."""
        result = builder.with_working_directory("/app")

        assert result is builder
        assert builder._working_directory == "/app"

    def test_with_problem_statement_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_problem_statement returns self for chaining."""
        result = builder.with_problem_statement("Fix the bug")

        assert result is builder
        assert builder._problem_statement == "Fix the bug"

    def test_with_additional_context_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_additional_context returns self for chaining."""
        context = {"hint": "Look at line 42"}
        result = builder.with_additional_context(context)

        assert result is builder
        assert builder._additional_context == context

    def test_add_test_scorer(self, builder: ScenarioBuilder) -> None:
        """Test add_test_scorer method."""
        result = builder.add_test_scorer(
            "my-tests",
            test_command="pytest",
            weight=2.0,
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["name"] == "my-tests"
        assert builder._scorers[0]["weight"] == 2.0
        assert builder._scorers[0]["scorer"]["type"] == "test_based_scorer"
        assert "test_command" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["test_command"] == "pytest"

    def test_add_test_scorer_with_files(self, builder: ScenarioBuilder) -> None:
        """Test add_test_scorer with test files."""
        test_files: list[ScorerTestBasedScoringFunctionTestFile] = [
            {"file_path": "test_main.py", "file_contents": "def test_foo(): pass"}
        ]
        result = builder.add_test_scorer("tests", test_command="pytest", test_files=test_files)

        assert result is builder
        assert "test_files" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["test_files"] == test_files

    def test_add_command_scorer(self, builder: ScenarioBuilder) -> None:
        """Test add_command_scorer method."""
        result = builder.add_command_scorer(
            "cmd-scorer",
            command="./check.sh",
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["scorer"]["type"] == "command_scorer"
        assert "command" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["command"] == "./check.sh"

    def test_add_bash_scorer(self, builder: ScenarioBuilder) -> None:
        """Test add_bash_scorer method."""
        result = builder.add_bash_scorer(
            "bash-scorer",
            bash_script="echo 'score=1.0'",
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["scorer"]["type"] == "bash_script_scorer"
        assert "bash_script" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["bash_script"] == "echo 'score=1.0'"

    def test_add_python_scorer(self, builder: ScenarioBuilder) -> None:
        """Test add_python_scorer method."""
        result = builder.add_python_scorer(
            "python-scorer",
            python_script="print('score=1.0')",
            python_version_constraint=">=3.10",
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["scorer"]["type"] == "python_script_scorer"
        assert builder._scorers[0]["scorer"]["python_script"] == "print('score=1.0')"
        assert "python_version_constraint" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["python_version_constraint"] == ">=3.10"

    def test_add_ast_grep_scorer(self, builder: ScenarioBuilder) -> None:
        """Test add_ast_grep_scorer method."""
        result = builder.add_ast_grep_scorer(
            "ast-scorer",
            pattern="$A.foo()",
            search_directory="/src",
            lang="python",
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["scorer"]["type"] == "ast_grep_scorer"
        assert builder._scorers[0]["scorer"]["pattern"] == "$A.foo()"
        assert builder._scorers[0]["scorer"]["search_directory"] == "/src"
        assert "lang" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["lang"] == "python"

    def test_add_custom_scorer(self, builder: ScenarioBuilder) -> None:
        """Test add_custom_scorer method."""
        result = builder.add_custom_scorer(
            "custom-scorer",
            custom_scorer_type="my_custom_scorer",
            scorer_params={"threshold": 0.5},
        )

        assert result is builder
        assert len(builder._scorers) == 1
        assert builder._scorers[0]["scorer"]["type"] == "custom_scorer"
        assert builder._scorers[0]["scorer"]["custom_scorer_type"] == "my_custom_scorer"
        assert "scorer_params" in builder._scorers[0]["scorer"]
        assert builder._scorers[0]["scorer"]["scorer_params"] == {"threshold": 0.5}

    def test_add_multiple_scorers(self, builder: ScenarioBuilder) -> None:
        """Test adding multiple scorers."""
        builder.add_test_scorer("test1", test_command="pytest", weight=1.0)
        builder.add_command_scorer("test2", command="./check.sh", weight=2.0)

        assert len(builder._scorers) == 2
        assert builder._scorers[0]["name"] == "test1"
        assert builder._scorers[1]["name"] == "test2"

    def test_add_scorer_rejects_zero_weight(self, builder: ScenarioBuilder) -> None:
        """Test that adding a scorer with zero weight raises ValueError."""
        with pytest.raises(ValueError, match="Scorer weight must be positive"):
            builder.add_bash_scorer("bad", bash_script="echo 1", weight=0.0)

    def test_add_scorer_rejects_negative_weight(self, builder: ScenarioBuilder) -> None:
        """Test that adding a scorer with negative weight raises ValueError."""
        with pytest.raises(ValueError, match="Scorer weight must be positive"):
            builder.add_bash_scorer("bad", bash_script="echo 1", weight=-1.0)

    def test_with_metadata_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_metadata returns self for chaining."""
        result = builder.with_metadata({"team": "infra"})

        assert result is builder
        assert builder._metadata == {"team": "infra"}

    def test_with_reference_output_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_reference_output returns self for chaining."""
        result = builder.with_reference_output("--- a/file.py\n+++ b/file.py")

        assert result is builder
        assert builder._reference_output == "--- a/file.py\n+++ b/file.py"

    def test_with_required_env_vars_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_required_env_vars returns self for chaining."""
        result = builder.with_required_env_vars(["API_KEY", "SECRET"])

        assert result is builder
        assert builder._required_env_vars == ["API_KEY", "SECRET"]

    def test_with_required_secrets_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_required_secrets returns self for chaining."""
        result = builder.with_required_secrets(["db_password"])

        assert result is builder
        assert builder._required_secrets == ["db_password"]

    def test_with_validation_type_returns_self(self, builder: ScenarioBuilder) -> None:
        """Test with_validation_type returns self for chaining."""
        result = builder.with_validation_type("FORWARD")

        assert result is builder
        assert builder._validation_type == "FORWARD"

    def test_build_params_missing_problem_statement(self, builder: ScenarioBuilder) -> None:
        """Test _build_params raises if problem statement is missing."""
        builder.add_test_scorer("test", test_command="pytest")

        with pytest.raises(ValueError, match="Problem statement is required"):
            builder._build_params()

    def test_build_params_missing_scorer(self, builder: ScenarioBuilder) -> None:
        """Test _build_params raises if no scorers are added."""
        builder.with_problem_statement("Fix the bug")

        with pytest.raises(ValueError, match="At least one scorer is required.*add_test_scorer"):
            builder._build_params()

    def test_build_params_minimal(self, builder: ScenarioBuilder) -> None:
        """Test _build_params with minimal configuration."""
        builder.with_problem_statement("Fix the bug")
        builder.add_test_scorer("tests", test_command="pytest")

        params = builder._build_params()

        assert params["name"] == "test-scenario"
        assert params["input_context"]["problem_statement"] == "Fix the bug"
        assert len(params["scoring_contract"]["scoring_function_parameters"]) == 1

    def test_build_params_with_environment(self, builder: ScenarioBuilder, mock_blueprint: Blueprint) -> None:
        """Test _build_params includes environment parameters."""
        builder.with_problem_statement("Fix the bug")
        builder.add_test_scorer("tests", test_command="pytest")
        builder.from_blueprint(mock_blueprint)
        builder.with_working_directory("/app")

        params = builder._build_params()

        assert params["environment_parameters"]["blueprint_id"] == "bp-123"
        assert params["environment_parameters"]["working_directory"] == "/app"

    def test_build_params_with_all_options(self, builder: ScenarioBuilder, mock_blueprint: Blueprint) -> None:
        """Test _build_params with all optional fields set."""
        builder.with_problem_statement("Fix the bug")
        builder.with_additional_context({"hint": "line 42"})
        builder.add_test_scorer("tests", test_command="pytest")
        builder.from_blueprint(mock_blueprint)
        builder.with_working_directory("/app")
        builder.with_metadata({"team": "infra"})
        builder.with_reference_output("diff content")
        builder.with_required_env_vars(["API_KEY"])
        builder.with_required_secrets(["db_pass"])
        builder.with_validation_type("FORWARD")

        params = builder._build_params()

        assert params["name"] == "test-scenario"
        assert params["input_context"]["problem_statement"] == "Fix the bug"
        assert params["input_context"]["additional_context"] == {"hint": "line 42"}
        assert params["environment_parameters"]["blueprint_id"] == "bp-123"
        assert params["environment_parameters"]["working_directory"] == "/app"
        assert params["metadata"] == {"team": "infra"}
        assert params["reference_output"] == "diff content"
        assert params["required_environment_variables"] == ["API_KEY"]
        assert params["required_secret_names"] == ["db_pass"]
        assert params["validation_type"] == "FORWARD"

    def test_build_params_normalizes_weights(self, builder: ScenarioBuilder) -> None:
        """Test that _build_params normalizes scorer weights to sum to 1.0."""
        builder.with_problem_statement("Fix the bug")
        builder.add_bash_scorer("scorer1", bash_script="echo 1", weight=1.0)
        builder.add_bash_scorer("scorer2", bash_script="echo 2", weight=2.0)
        builder.add_bash_scorer("scorer3", bash_script="echo 3", weight=3.0)

        params = builder._build_params()
        scorers = params["scoring_contract"]["scoring_function_parameters"]

        # Weights 1, 2, 3 should normalize to 1/6, 2/6, 3/6
        assert len(scorers) == 3
        assert abs(scorers[0]["weight"] - 1 / 6) < 0.0001
        assert abs(scorers[1]["weight"] - 2 / 6) < 0.0001
        assert abs(scorers[2]["weight"] - 3 / 6) < 0.0001

        # Total should be 1.0
        total = sum(s["weight"] for s in scorers)
        assert abs(total - 1.0) < 0.0001

    def test_push_calls_api_and_returns_scenario(self, builder: ScenarioBuilder, mock_client: MagicMock) -> None:
        """Test push() calls API with correct params and returns Scenario."""
        mock_client.scenarios.create.return_value.id = "scn-new-123"

        builder.with_problem_statement("Fix the bug")
        builder.add_test_scorer("tests", test_command="pytest")

        scenario = builder.push()

        mock_client.scenarios.create.assert_called_once()
        call_kwargs = mock_client.scenarios.create.call_args.kwargs
        assert call_kwargs["name"] == "test-scenario"
        assert call_kwargs["input_context"]["problem_statement"] == "Fix the bug"

        assert scenario.id == "scn-new-123"

    def test_fluent_chaining(self, builder: ScenarioBuilder, mock_blueprint: Blueprint) -> None:
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
