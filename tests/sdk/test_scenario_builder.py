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

    def test_instantiation(self, mock_client: MagicMock) -> None:
        """Test builder initialization and repr."""
        builder = ScenarioBuilder(mock_client, "my-scenario")

        assert builder._client is mock_client
        assert builder._name == "my-scenario"
        assert builder.name == "my-scenario"
        assert repr(builder) == "<ScenarioBuilder name='my-scenario'>"

    def test_from_blueprint_and_snapshot(
        self, builder: ScenarioBuilder, mock_blueprint: Blueprint, mock_snapshot: Snapshot
    ) -> None:
        """Test blueprint/snapshot setting returns self and are mutually exclusive."""
        # from_blueprint returns self and sets blueprint
        result = builder.from_blueprint(mock_blueprint)
        assert result is builder
        assert builder._blueprint is mock_blueprint
        assert builder._snapshot is None

        # from_snapshot returns self, sets snapshot, and clears blueprint
        result = builder.from_snapshot(mock_snapshot)
        assert result is builder
        assert builder._snapshot is mock_snapshot
        assert builder._blueprint is None

        # from_blueprint clears snapshot
        builder.from_blueprint(mock_blueprint)
        assert builder._blueprint is mock_blueprint
        assert builder._snapshot is None

    def test_scorers(self, builder: ScenarioBuilder) -> None:
        """Test all scorer types, optional params, and multiple scorers."""
        # Test scorer with test files
        test_files: list[ScorerTestBasedScoringFunctionTestFile] = [
            {"file_path": "test_main.py", "file_contents": "def test_foo(): pass"}
        ]
        result = builder.add_test_command_scorer(
            "test-scorer", test_command="pytest", weight=2.0, test_files=test_files
        )
        assert result is builder
        assert builder._scorers[0]["name"] == "test-scorer"
        assert builder._scorers[0]["weight"] == 2.0
        assert builder._scorers[0]["scorer"]["type"] == "test_based_scorer"
        assert builder._scorers[0]["scorer"].get("test_command") == "pytest"
        assert builder._scorers[0]["scorer"].get("test_files") == test_files

        # Command scorer
        builder.add_shell_command_scorer("cmd-scorer", command="./check.sh")
        assert builder._scorers[1]["scorer"]["type"] == "command_scorer"
        assert builder._scorers[1]["scorer"].get("command") == "./check.sh"

        # Bash scorer
        builder.add_bash_script_scorer("bash-scorer", bash_script="echo 'score=1.0'")
        assert builder._scorers[2]["scorer"]["type"] == "bash_script_scorer"
        assert builder._scorers[2]["scorer"].get("bash_script") == "echo 'score=1.0'"

        # Python scorer with optional params
        builder.add_python_script_scorer(
            "python-scorer",
            python_script="print('1.0')",
            python_version_constraint=">=3.10",
            requirements_contents="numpy",
        )
        assert builder._scorers[3]["scorer"]["type"] == "python_script_scorer"
        assert builder._scorers[3]["scorer"].get("python_version_constraint") == ">=3.10"
        assert builder._scorers[3]["scorer"].get("requirements_contents") == "numpy"

        # AST grep scorer with optional lang
        builder.add_ast_grep_scorer("ast-scorer", pattern="$A.foo()", search_directory="/src", lang="python")
        assert builder._scorers[4]["scorer"]["type"] == "ast_grep_scorer"
        assert builder._scorers[4]["scorer"].get("pattern") == "$A.foo()"
        assert builder._scorers[4]["scorer"].get("lang") == "python"

        # Custom scorer with optional params
        builder.add_custom_scorer("custom-scorer", custom_scorer_type="my_scorer", scorer_params={"threshold": 0.5})
        assert builder._scorers[5]["scorer"]["type"] == "custom_scorer"
        assert builder._scorers[5]["scorer"].get("custom_scorer_type") == "my_scorer"
        assert builder._scorers[5]["scorer"].get("scorer_params") == {"threshold": 0.5}

        # Verify multiple scorers accumulated
        assert len(builder._scorers) == 6

    def test_add_scorer_rejects_invalid_weight(self, builder: ScenarioBuilder) -> None:
        """Test that adding a scorer with zero or negative weight raises ValueError."""
        with pytest.raises(ValueError, match="Scorer weight must be positive"):
            builder.add_bash_script_scorer("bad", bash_script="echo 1", weight=0.0)

        with pytest.raises(ValueError, match="Scorer weight must be positive"):
            builder.add_bash_script_scorer("bad", bash_script="echo 1", weight=-1.0)

    def test_build_params_validation(self, builder: ScenarioBuilder) -> None:
        """Test _build_params raises for missing required fields."""
        # Missing problem statement
        builder.add_test_command_scorer("test", test_command="pytest")
        with pytest.raises(ValueError, match="Problem statement is required"):
            builder._build_params()

        # Missing scorer (new builder)
        builder2 = ScenarioBuilder(builder._client, "test2")
        builder2.with_problem_statement("Fix the bug")
        with pytest.raises(ValueError, match="At least one scorer is required"):
            builder2._build_params()

    def test_build_params_with_all_options(self, builder: ScenarioBuilder, mock_blueprint: Blueprint) -> None:
        """Test _build_params with all optional fields set."""
        builder.with_problem_statement("Fix the bug")
        builder.with_additional_context({"hint": "line 42"})
        builder.add_test_command_scorer("tests", test_command="pytest")
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
        builder.add_bash_script_scorer("scorer1", bash_script="echo 1", weight=1.0)
        builder.add_bash_script_scorer("scorer2", bash_script="echo 2", weight=2.0)
        builder.add_bash_script_scorer("scorer3", bash_script="echo 3", weight=3.0)

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
        builder.add_test_command_scorer("tests", test_command="pytest")

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
            .add_test_command_scorer("tests", test_command="pytest")
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
