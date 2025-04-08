# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ScorerCreateParams"]


class ScorerCreateParams(TypedDict, total=False):
    bash_script: Required[str]
    """
    Bash script for the custom scorer taking context as a json object
    $RL_SCORER_CONTEXT.
    """

    type: Required[str]
    """Name of the type of custom scorer."""
