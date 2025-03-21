# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "ScoringFunctionParam",
    "ScoringFunction",
    "ScoringFunctionAstGrepScoringFunction",
    "ScoringFunctionBashScriptScoringFunction",
    "ScoringFunctionCommandScoringFunction",
    "ScoringFunctionCustomScoringFunction",
    "ScoringFunctionPythonScriptScoringFunction",
    "ScoringFunctionTestBasedScoringFunction",
    "ScoringFunctionTestBasedScoringFunctionTestFile",
]


class ScoringFunctionAstGrepScoringFunction(TypedDict, total=False):
    pattern: Required[str]
    """AST pattern to match."""

    search_directory: Required[str]
    """The path to search."""

    type: Required[Literal["ast_grep_scorer"]]

    lang: str
    """The language of the pattern."""


class ScoringFunctionBashScriptScoringFunction(TypedDict, total=False):
    type: Required[Literal["bash_script_scorer"]]

    bash_script: str
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be a float between 0.0 and 1.0, and look
    like "score=[0.0..1.0].
    """


class ScoringFunctionCommandScoringFunction(TypedDict, total=False):
    type: Required[Literal["command_scorer"]]

    command: str
    """The command to execute."""


class ScoringFunctionCustomScoringFunction(TypedDict, total=False):
    type: Required[Literal["custom_scorer"]]

    scorer_params: Optional[object]
    """Additional JSON structured context to pass to the scoring function."""


class ScoringFunctionPythonScriptScoringFunction(TypedDict, total=False):
    python_script: Required[str]
    """Python script to be run.

    The script should output the score to standard out as a float between 0.0 and
    1.0.
    """

    type: Required[Literal["python_script_scorer"]]

    requirements_contents: str
    """Package dependencies to be installed.

    The requirements should be a valid requirements.txt file.
    """


class ScoringFunctionTestBasedScoringFunctionTestFile(TypedDict, total=False):
    file_contents: str
    """Content of the test file"""

    file_path: str
    """
    Path to write content of the test file, relative to your environment's working
    directory
    """


class ScoringFunctionTestBasedScoringFunction(TypedDict, total=False):
    type: Required[Literal["test_based_scorer"]]

    test_command: str
    """The command to execute for running the tests"""

    test_files: Iterable[ScoringFunctionTestBasedScoringFunctionTestFile]
    """List of test files to create"""


ScoringFunction: TypeAlias = Union[
    ScoringFunctionAstGrepScoringFunction,
    ScoringFunctionBashScriptScoringFunction,
    ScoringFunctionCommandScoringFunction,
    ScoringFunctionCustomScoringFunction,
    ScoringFunctionPythonScriptScoringFunction,
    ScoringFunctionTestBasedScoringFunction,
]


class ScoringFunctionParam(TypedDict, total=False):
    name: Required[str]
    """Name of scoring function. Names must only contain [a-zA-Z0-9_-]."""

    scoring_function: Required[ScoringFunction]
    """The scoring function to use for evaluating this scenario.

    The type field determines which built-in function to use.
    """

    weight: Required[float]
    """Weight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """
