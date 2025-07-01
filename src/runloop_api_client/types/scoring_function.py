# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "ScoringFunction",
    "Scorer",
    "ScorerAstGrepScoringFunction",
    "ScorerBashScriptScoringFunction",
    "ScorerCommandScoringFunction",
    "ScorerCustomScoringFunction",
    "ScorerPythonScriptScoringFunction",
    "ScorerTestBasedScoringFunction",
    "ScorerTestBasedScoringFunctionTestFile",
]


class ScorerAstGrepScoringFunction(BaseModel):
    pattern: str
    """AST pattern to match.

    Pattern will be passed to ast-grep using the commandline surround by double
    quotes ("), so make sure to use proper escaping (for example, \\$$\\$$\\$$).
    """

    search_directory: str
    """The path to search."""

    type: Literal["ast_grep_scorer"]

    lang: Optional[str] = None
    """The language of the pattern."""


class ScorerBashScriptScoringFunction(BaseModel):
    type: Literal["bash_script_scorer"]

    bash_script: Optional[str] = None
    """
    A single bash script that sets up the environment, scores, and prints the final
    score to standard out. Score should be a float between 0.0 and 1.0, and look
    like "score=[0.0..1.0].
    """


class ScorerCommandScoringFunction(BaseModel):
    type: Literal["command_scorer"]

    command: Optional[str] = None
    """The command to execute."""


class ScorerCustomScoringFunction(BaseModel):
    custom_scorer_type: str
    """Type of the scoring function, previously registered with Runloop."""

    type: Literal["custom_scorer"]

    scorer_params: Optional[object] = None
    """Additional JSON structured context to pass to the scoring function."""


class ScorerPythonScriptScoringFunction(BaseModel):
    python_script: str
    """Python script to be run.

    The script should output the score to standard out as a float between 0.0 and
    1.0.
    """

    type: Literal["python_script_scorer"]

    python_version_constraint: Optional[str] = None
    """Python version to run scoring. Default is "==3.12.10" """

    requirements_contents: Optional[str] = None
    """Package dependencies to be installed.

    The requirements should be a valid requirements.txt file.
    """


class ScorerTestBasedScoringFunctionTestFile(BaseModel):
    file_contents: Optional[str] = None
    """Content of the test file"""

    file_path: Optional[str] = None
    """
    Path to write content of the test file, relative to your environment's working
    directory
    """


class ScorerTestBasedScoringFunction(BaseModel):
    type: Literal["test_based_scorer"]

    test_command: Optional[str] = None
    """The command to execute for running the tests"""

    test_files: Optional[List[ScorerTestBasedScoringFunctionTestFile]] = None
    """List of test files to create"""


Scorer: TypeAlias = Annotated[
    Union[
        ScorerAstGrepScoringFunction,
        ScorerBashScriptScoringFunction,
        ScorerCommandScoringFunction,
        ScorerCustomScoringFunction,
        ScorerPythonScriptScoringFunction,
        ScorerTestBasedScoringFunction,
    ],
    PropertyInfo(discriminator="type"),
]


class ScoringFunction(BaseModel):
    name: str
    """Name of scoring function. Names must only contain [a-zA-Z0-9_-]."""

    scorer: Scorer
    """The scoring function to use for evaluating this scenario.

    The type field determines which built-in function to use.
    """

    weight: float
    """Weight to apply to scoring function score.

    Weights of all scoring functions should sum to 1.0.
    """
