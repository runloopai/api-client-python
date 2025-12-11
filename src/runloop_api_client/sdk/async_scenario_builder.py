"""AsyncScenarioBuilder for constructing scenarios with a fluent API."""

from __future__ import annotations

from typing import Dict, List, Iterable, Optional
from typing_extensions import Self, Unpack, Literal, override

from ..types import ScenarioCreateParams, ScenarioEnvironmentParam
from ._types import ScenarioPreview, LongRequestOptions
from .._client import AsyncRunloop
from .async_scenario import AsyncScenario
from .async_snapshot import AsyncSnapshot
from .async_blueprint import AsyncBlueprint
from ..types.scoring_function_param import (
    Scorer,
    ScoringFunctionParam,
    ScorerCustomScoringFunction,
    ScorerAstGrepScoringFunction,
    ScorerCommandScoringFunction,
    ScorerTestBasedScoringFunction,
    ScorerBashScriptScoringFunction,
    ScorerPythonScriptScoringFunction,
    ScorerTestBasedScoringFunctionTestFile,
)


class AsyncScenarioBuilder:
    """Async builder for constructing scenarios with a fluent API.

    Provides a step-by-step interface for configuring all aspects of a scenario
    before pushing it to the platform.

    Example:
        >>> builder = (
        ...     runloop.scenario.builder("my-scenario")
        ...     .from_blueprint(blueprint)
        ...     .with_working_directory("/app")
        ...     .with_problem_statement("Fix the bug in main.py")
        ...     .add_test_command_scorer("tests", test_command="pytest")
        ... )
        >>> params = builder.build()
        >>> scenario = await runloop.scenario.create(**params)  # equivalent to builder.push()
    """

    def __init__(self, name: str, client: AsyncRunloop) -> None:
        """Initialize the builder.

        :param name: Name for the scenario
        :type name: str
        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        """
        self._client = client
        self._name = name

        # Environment configuration
        self._blueprint: Optional[AsyncBlueprint] = None
        self._snapshot: Optional[AsyncSnapshot] = None
        self._working_directory: Optional[str] = None

        # Input context
        self._problem_statement: Optional[str] = None
        self._additional_context: Optional[object] = None

        # Scoring
        self._scorers: List[ScoringFunctionParam] = []

        # Metadata and other options
        self._metadata: Dict[str, str] = {}
        self._reference_output: Optional[str] = None
        self._required_env_vars: Optional[List[str]] = None
        self._required_secrets: Optional[List[str]] = None
        self._validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]] = None

    @override
    def __repr__(self) -> str:
        return f"<AsyncScenarioBuilder name={self._name!r}>"

    @property
    def name(self) -> str:
        """Return the scenario name.

        :return: Scenario name
        :rtype: str
        """
        return self._name

    def from_blueprint(self, blueprint: AsyncBlueprint) -> Self:
        """Set a blueprint to define the baseline environment for the scenario.

        :param blueprint: Blueprint to use
        :type blueprint: AsyncBlueprint
        :return: Self for method chaining
        :rtype: Self
        """
        self._blueprint = blueprint
        self._snapshot = None  # Clear snapshot if blueprint is set
        return self

    def from_snapshot(self, snapshot: AsyncSnapshot) -> Self:
        """Set a snapshot to define the baseline environment for the scenario.

        :param snapshot: Snapshot to use
        :type snapshot: AsyncSnapshot
        :return: Self for method chaining
        :rtype: Self
        """
        self._snapshot = snapshot
        self._blueprint = None  # Clear blueprint if snapshot is set
        return self

    def with_working_directory(self, directory: str) -> Self:
        """Set the working directory for the scenario.

        :param directory: Working directory path
        :type directory: str
        :return: Self for method chaining
        :rtype: Self
        """
        self._working_directory = directory
        return self

    def with_problem_statement(self, statement: str) -> Self:
        """Set the problem statement for the scenario; this will be provided as input context to the agent.

        :param statement: Problem statement text
        :type statement: str
        :return: Self for method chaining
        :rtype: Self
        """
        self._problem_statement = statement
        return self

    def with_additional_context(self, context: object) -> Self:
        """Set additional structured context for the scenario.
        This can be used to provide additional information to the agent, such as hints, examples, or other relevant information.

        :param context: Additional context (JSON-serializable)
        :type context: object
        :return: Self for method chaining
        :rtype: Self
        """
        self._additional_context = context
        return self

    def _add_scorer(self, name: str, weight: float, scorer: Scorer) -> Self:
        """Internal helper to add a scorer to the list.

        :raises ValueError: If weight is not positive
        """
        if weight <= 0:
            raise ValueError(f"Scorer weight must be positive, got {weight}")
        self._scorers.append({"name": name, "weight": weight, "scorer": scorer})
        return self

    def add_test_command_scorer(
        self,
        name: str,
        *,
        test_command: str,
        weight: float = 1.0,
        test_files: Optional[Iterable[ScorerTestBasedScoringFunctionTestFile]] = None,
    ) -> Self:
        """Add a test-based scorer that runs a test command.

        :param name: Name of the scoring function
        :type name: str
        :param test_command: Command to run tests (e.g., "pytest")
        :type test_command: str
        :param weight: Weight for this scorer (normalized automatically)
        :type weight: float
        :param test_files: Optional test files to create before running
        :type test_files: Optional[Iterable[ScorerTestBasedScoringFunctionTestFile]]
        :return: Self for method chaining
        :rtype: Self
        """
        scorer: ScorerTestBasedScoringFunction = {
            "type": "test_based_scorer",
            "test_command": test_command,
        }
        if test_files:
            scorer["test_files"] = test_files
        return self._add_scorer(name, weight, scorer)

    def add_shell_command_scorer(
        self,
        name: str,
        *,
        command: str,
        weight: float = 1.0,
    ) -> Self:
        """Add a command scorer that runs a shell command.

        :param name: Name of the scoring function
        :type name: str
        :param command: Shell command to execute
        :type command: str
        :param weight: Weight for this scorer (normalized automatically)
        :type weight: float
        :return: Self for method chaining
        :rtype: Self
        """
        scorer: ScorerCommandScoringFunction = {
            "type": "command_scorer",
            "command": command,
        }
        return self._add_scorer(name, weight, scorer)

    def add_bash_script_scorer(
        self,
        name: str,
        *,
        bash_script: str,
        weight: float = 1.0,
    ) -> Self:
        """Add a standalone bash script scorer.

        The script should output "score=X.X" where X.X is a float between 0.0 and 1.0, inclusive.

        :param name: Name of the scoring function
        :type name: str
        :param bash_script: Bash script content
        :type bash_script: str
        :param weight: Weight for this scorer (normalized automatically)
        :type weight: float
        :return: Self for method chaining
        :rtype: Self
        """
        scorer: ScorerBashScriptScoringFunction = {
            "type": "bash_script_scorer",
            "bash_script": bash_script,
        }
        return self._add_scorer(name, weight, scorer)

    def add_python_script_scorer(
        self,
        name: str,
        *,
        python_script: str,
        weight: float = 1.0,
        python_version_constraint: Optional[str] = None,
        requirements_contents: Optional[str] = None,
    ) -> Self:
        """Add a standalone Python script scorer.

        The script is run in an isolated uv environment, and the dependencies are declared in the
        `uv script header <https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies>`__.

        The script should print the score in the range [0.0, 1.0] to stdout.

        :param name: Name of the scoring function
        :type name: str
        :param python_script: Python script content
        :type python_script: str
        :param weight: Weight for this scorer (normalized automatically)
        :type weight: float
        :param python_version_constraint: Python version (default "==3.12.10")
        :type python_version_constraint: Optional[str]
        :param requirements_contents: pip requirements.txt content
        :type requirements_contents: Optional[str]
        :return: Self for method chaining
        :rtype: Self
        """
        scorer: ScorerPythonScriptScoringFunction = {
            "type": "python_script_scorer",
            "python_script": python_script,
        }
        if python_version_constraint:
            scorer["python_version_constraint"] = python_version_constraint
        if requirements_contents:
            scorer["requirements_contents"] = requirements_contents
        return self._add_scorer(name, weight, scorer)

    def add_ast_grep_scorer(
        self,
        name: str,
        *,
        pattern: str,
        weight: float = 1.0,
        search_directory: str = ".",
        lang: Optional[str] = None,
    ) -> Self:
        """Add an AST grep scorer that matches code patterns.

        :param name: Name of the scoring function
        :type name: str
        :param pattern: AST pattern to match
        :type pattern: str
        :param weight: Weight for this scorer (normalized automatically)
        :type weight: float
        :param search_directory: Directory to search (default ".")
        :type search_directory: str
        :param lang: Language of the pattern (optional)
        :type lang: Optional[str]
        :return: Self for method chaining
        :rtype: Self
        """
        scorer: ScorerAstGrepScoringFunction = {
            "type": "ast_grep_scorer",
            "pattern": pattern,
            "search_directory": search_directory,
        }
        if lang:
            scorer["lang"] = lang
        return self._add_scorer(name, weight, scorer)

    def add_custom_scorer(
        self,
        name: str,
        *,
        custom_scorer_type: str,
        weight: float = 1.0,
        scorer_params: Optional[object] = None,
    ) -> Self:
        """Add a custom scorer registered with Runloop.

        :param name: Name of the scoring function
        :type name: str
        :param custom_scorer_type: Type identifier registered with Runloop
        :type custom_scorer_type: str
        :param weight: Weight for this scorer (normalized automatically)
        :type weight: float
        :param scorer_params: Additional JSON parameters for the scorer
        :type scorer_params: Optional[object]
        :return: Self for method chaining
        :rtype: Self
        """
        scorer: ScorerCustomScoringFunction = {
            "type": "custom_scorer",
            "custom_scorer_type": custom_scorer_type,
        }
        if scorer_params:
            scorer["scorer_params"] = scorer_params
        return self._add_scorer(name, weight, scorer)

    def with_metadata(self, metadata: Dict[str, str]) -> Self:
        """Set metadata for the scenario.

        :param metadata: Key-value metadata
        :type metadata: Dict[str, str]
        :return: Self for method chaining
        :rtype: Self
        """
        self._metadata = metadata
        return self

    def with_reference_output(self, output: str) -> Self:
        """Set the reference solution or gold patch for validation.
        After application, the scorer is expected to return a score of 1.0.

        :param output: Reference solution or gold patch (e.g., git diff)
        :type output: str
        :return: Self for method chaining
        :rtype: Self
        """
        self._reference_output = output
        return self

    def with_required_env_vars(self, env_vars: List[str]) -> Self:
        """Set required environment variables.

        :param env_vars: List of required environment variable names
        :type env_vars: List[str]
        :return: Self for method chaining
        :rtype: Self
        """
        self._required_env_vars = env_vars
        return self

    def with_required_secrets(self, secrets: List[str]) -> Self:
        """Set required secrets.

        :param secrets: List of required secret names
        :type secrets: List[str]
        :return: Self for method chaining
        :rtype: Self
        """
        self._required_secrets = secrets
        return self

    def with_validation_type(self, validation_type: Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]) -> Self:
        """Set the validation strategy to specify how the reference solution or gold patch is applied to the scenario.

        :param validation_type: Validation type
        :type validation_type: Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]
        :return: Self for method chaining
        :rtype: Self
        """
        self._validation_type = validation_type
        return self

    def _build_normalized_scorers(self) -> List[ScoringFunctionParam]:
        """Build normalized scorers list."""
        total_weight = sum(s["weight"] for s in self._scorers)
        return [{**s, "weight": s["weight"] / total_weight} for s in self._scorers]

    def _build_environment_params(self) -> Optional[ScenarioEnvironmentParam]:
        """Build environment parameters."""
        if not self._blueprint and not self._snapshot and not self._working_directory:
            return None
        return {
            "blueprint_id": self._blueprint.id if self._blueprint else None,
            "snapshot_id": self._snapshot.id if self._snapshot else None,
            "working_directory": self._working_directory if self._working_directory else None,
        }

    def build(self) -> ScenarioCreateParams:
        """Build the scenario creation parameters.

        Weights are automatically normalized to sum to 1.0.

        :raises ValueError: If required fields are missing
        :return: Parameters for scenario creation
        :rtype: ScenarioCreateParams
        """
        if not self._problem_statement:
            raise ValueError("Problem statement is required. Call with_problem_statement() first.")

        if not self._scorers:
            raise ValueError(
                "At least one scorer is required. "
                "Call add_test_command_scorer(), add_bash_script_scorer(), or another scorer method first."
            )

        return {
            "name": self._name,
            "input_context": {
                "problem_statement": self._problem_statement,
                "additional_context": self._additional_context,
            },
            "scoring_contract": {
                "scoring_function_parameters": self._build_normalized_scorers(),
            },
            "environment_parameters": self._build_environment_params(),
            "metadata": self._metadata,
            "reference_output": self._reference_output,
            "required_environment_variables": self._required_env_vars,
            "required_secret_names": self._required_secrets,
            "validation_type": self._validation_type,
        }

    def preview(self) -> ScenarioPreview:
        """Preview the scenario configuration without pushing to the platform.

        Returns the current configuration state as a ScenarioPreview object.
        Does not validate or raise errors for missing required fields.

        :return: Preview of the scenario configuration
        :rtype: ScenarioPreview
        """
        return ScenarioPreview.model_validate(
            {
                "name": self._name,
                "input_context": {
                    "problem_statement": self._problem_statement,
                    "additional_context": self._additional_context,
                },
                "scoring_contract": {
                    "scoring_function_parameters": self._build_normalized_scorers(),
                },
                "environment": self._build_environment_params(),
                "metadata": self._metadata,
                "reference_output": self._reference_output,
                "required_environment_variables": self._required_env_vars,
                "required_secret_names": self._required_secrets,
                "validation_type": self._validation_type,
            }
        )

    async def push(self, **options: Unpack[LongRequestOptions]) -> AsyncScenario:
        """Create the scenario on the platform.

        :param options: Optional long-running request configuration
        :raises ValueError: If required fields are missing
        :return: Created scenario wrapper
        :rtype: AsyncScenario
        """
        params = self.build()
        scenario_view = await self._client.scenarios.create(**params, **options)
        return AsyncScenario(self._client, scenario_view.id)
