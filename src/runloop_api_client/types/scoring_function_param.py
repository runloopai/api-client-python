# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "ScoringFunctionParam",
    "Scorer",
    "ScorerAstGrepScoringFunction",
    "ScorerBashScriptScoringFunction",
    "ScorerCommandScoringFunction",
    "ScorerCustomScoringFunction",
    "ScorerPythonScriptScoringFunction",
    "ScorerTestBasedScoringFunction",
    "ScorerTestBasedScoringFunctionTestFile",
]


class ScorerAstGrepScoringFunction(TypedDict, total=False):
    """AstGrepScoringFunction utilizes structured coach search for scoring."""

    pattern: Required[str]
    """AST pattern to match.

    Pattern will be passed to ast-grep using the commandline surround by double
    quotes ("), so make sure to use proper escaping (for example, \\$$\\$$\\$$).
    """

    search_directory: Required[str]
    """The path to search."""

    type: Required[Literal["ast_grep_scorer"]]

    lang: str
    """The language of the pattern."""


class ScorerBashScriptScoringFunction(TypedDict, total=False):
    """
    BashScriptScoringFunction is a scoring function specified by a bash script that will be run in the context of your environment.
    """

    type: Required[Literal["bash_script_scorer"]]

    bash_script: str
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be a float between 0.0 and 1.0, and look
    like "score=[0.0..1.0].
    """


class ScorerCommandScoringFunction(TypedDict, total=False):
    """
    CommandScoringFunction executes a single command and checks the result.The output of the command will be printed. Scoring will passed if the command returns status code 0, otherwise it will be failed.
    """

    type: Required[Literal["command_scorer"]]

    command: str
    """The command to execute."""


class ScorerCustomScoringFunction(TypedDict, total=False):
    """CustomScoringFunction is a custom, user defined scoring function."""

    custom_scorer_type: Required[str]
    """Type of the scoring function, previously registered with Runloop."""

    type: Required[Literal["custom_scorer"]]

    scorer_params: Optional[object]
    """Additional JSON structured context to pass to the scoring function."""


class ScorerPythonScriptScoringFunction(TypedDict, total=False):
    """
    PythonScriptScoringFunction will run a python script in the context of your environment as a ScoringFunction.
    """

    python_script: Required[str]
    """Python script to be run.

    The script should output the score to standard out as a float between 0.0 and
    1.0.
    """

    type: Required[Literal["python_script_scorer"]]

    python_version_constraint: Optional[str]
    """Python version to run scoring. Default is "==3.12.10" """

    requirements_contents: Optional[str]
    """Package dependencies to be installed.

    The requirements should be a valid requirements.txt file.
    """


class ScorerTestBasedScoringFunctionTestFile(TypedDict, total=False):
    file_contents: str
    """Content of the test file"""

    file_path: str
    """
    Path to write content of the test file, relative to your environment's working
    directory
    """


class ScorerTestBasedScoringFunction(TypedDict, total=False):
    """
    TestBasedScoringFunction writes test files to disk and executes a test command to verify the solution.
    """

    type: Required[Literal["test_based_scorer"]]

    test_command: str
    """The command to execute for running the tests"""

    test_files: Iterable[ScorerTestBasedScoringFunctionTestFile]
    """List of test files to create"""


Scorer: TypeAlias = Union[
    ScorerAstGrepScoringFunction,
    ScorerBashScriptScoringFunction,
    ScorerCommandScoringFunction,
    ScorerCustomScoringFunction,
    ScorerPythonScriptScoringFunction,
    ScorerTestBasedScoringFunction,
]


class ScoringFunctionParam(TypedDict, total=False):
    """ScoringFunction specifies a method of scoring a Scenario."""

    name: Required[str]
    """Name of scoring function. Names must only contain ``[a-zA-Z0-9_-]``."""

    scorer: Required[Scorer]
    """The scoring function to use for evaluating this scenario.

    The type field determines which built-in function to use.
    """

    weight: Required[float]
    """Weight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """
