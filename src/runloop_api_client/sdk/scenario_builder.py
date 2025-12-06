"""ScenarioBuilder for constructing scenarios with a fluent API."""

from __future__ import annotations

from typing import Any, Dict, List, Iterable, Optional
from typing_extensions import Self, Literal, override

from .._client import Runloop
from .scenario import Scenario
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


class ScenarioBuilder:
    """Builder for constructing scenarios with a fluent API.

    Provides a step-by-step interface for configuring all aspects of a scenario
    before pushing it to the platform.

    Example:
        >>> builder = sdk.scenario.builder("my-scenario")
        >>> builder.from_blueprint_id("bp-xxx")
        >>> builder.with_working_directory("/app")
        >>> builder.with_problem_statement("Fix the bug in main.py")
        >>> builder.add_test_scorer("tests", test_command="pytest")
        >>> scenario = builder.push()
    """

    def __init__(self, client: Runloop, name: str) -> None:
        """Initialize the builder.

        :param client: Runloop client instance
        :type client: Runloop
        :param name: Name for the scenario
        :type name: str
        """
        self._client = client
        self._name = name

        # Environment configuration
        self._blueprint_id: Optional[str] = None
        self._snapshot_id: Optional[str] = None
        self._working_directory: Optional[str] = None

        # Input context
        self._problem_statement: Optional[str] = None
        self._additional_context: Optional[object] = None

        # Scoring
        self._scorers: List[ScoringFunctionParam] = []

        # Metadata and other options
        self._metadata: Optional[Dict[str, str]] = None
        self._reference_output: Optional[str] = None
        self._required_env_vars: Optional[List[str]] = None
        self._required_secrets: Optional[List[str]] = None
        self._validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]] = None

    @override
    def __repr__(self) -> str:
        return f"<ScenarioBuilder name={self._name!r}>"

    @property
    def name(self) -> str:
        """Return the scenario name.

        :return: Scenario name
        :rtype: str
        """
        return self._name

    def from_blueprint_id(self, blueprint_id: str) -> Self:
        """Set the blueprint ID for the scenario environment.

        :param blueprint_id: Blueprint ID to use
        :type blueprint_id: str
        :return: Self for method chaining
        :rtype: Self
        """
        self._blueprint_id = blueprint_id
        self._snapshot_id = None  # Clear snapshot if blueprint is set
        return self

    def from_snapshot_id(self, snapshot_id: str) -> Self:
        """Set the snapshot ID for the scenario environment.

        :param snapshot_id: Snapshot ID to use
        :type snapshot_id: str
        :return: Self for method chaining
        :rtype: Self
        """
        self._snapshot_id = snapshot_id
        self._blueprint_id = None  # Clear blueprint if snapshot is set
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
        """Set the problem statement for the scenario.

        :param statement: Problem statement text
        :type statement: str
        :return: Self for method chaining
        :rtype: Self
        """
        self._problem_statement = statement
        return self

    def with_additional_context(self, context: object) -> Self:
        """Set additional structured context for the scenario.

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

    def add_test_scorer(
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

    def add_command_scorer(
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

    def add_bash_scorer(
        self,
        name: str,
        *,
        bash_script: str,
        weight: float = 1.0,
    ) -> Self:
        """Add a bash script scorer.

        The script should output "score=X.X" where X.X is a float between 0.0 and 1.0.

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

    def add_python_scorer(
        self,
        name: str,
        *,
        python_script: str,
        weight: float = 1.0,
        python_version_constraint: Optional[str] = None,
        requirements_contents: Optional[str] = None,
    ) -> Self:
        """Add a Python script scorer.

        The script should print the score (0.0-1.0) to stdout.

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
        """Set the reference output/solution for validation.

        :param output: Reference output (e.g., git diff)
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
        """Set the validation strategy.

        :param validation_type: Validation type
        :type validation_type: Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]
        :return: Self for method chaining
        :rtype: Self
        """
        self._validation_type = validation_type
        return self

    def _build_params(self) -> Dict[str, Any]:
        """Build the scenario creation parameters.

        Weights are automatically normalized to sum to 1.0.

        :raises ValueError: If required fields are missing
        :return: Parameters for scenario creation
        :rtype: Dict[str, Any]
        """
        if not self._problem_statement:
            raise ValueError("Problem statement is required. Call with_problem_statement() first.")

        if not self._scorers:
            raise ValueError(
                "At least one scorer is required. "
                "Call add_test_scorer(), add_bash_scorer(), or another scorer method first."
            )

        # Normalize weights to sum to 1.0
        total_weight = sum(s["weight"] for s in self._scorers)
        normalized_scorers = [{**s, "weight": s["weight"] / total_weight} for s in self._scorers]

        params: Dict[str, Any] = {
            "name": self._name,
            "input_context": {
                "problem_statement": self._problem_statement,
            },
            "scoring_contract": {
                "scoring_function_parameters": normalized_scorers,
            },
        }

        # Add additional context if set
        if self._additional_context is not None:
            params["input_context"]["additional_context"] = self._additional_context

        # Build environment parameters if any are set
        env_params: Dict[str, Any] = {}
        if self._blueprint_id:
            env_params["blueprint_id"] = self._blueprint_id
        if self._snapshot_id:
            env_params["snapshot_id"] = self._snapshot_id
        if self._working_directory:
            env_params["working_directory"] = self._working_directory

        if env_params:
            params["environment_parameters"] = env_params

        # Add optional fields
        if self._metadata:
            params["metadata"] = self._metadata
        if self._reference_output:
            params["reference_output"] = self._reference_output
        if self._required_env_vars:
            params["required_environment_variables"] = self._required_env_vars
        if self._required_secrets:
            params["required_secret_names"] = self._required_secrets
        if self._validation_type:
            params["validation_type"] = self._validation_type

        return params

    def push(self) -> Scenario:
        """Create the scenario on the platform.

        :raises ValueError: If required fields are missing
        :return: Created scenario wrapper
        :rtype: Scenario
        """
        params = self._build_params()
        scenario_view = self._client.scenarios.create(**params)
        return Scenario(self._client, scenario_view.id)
