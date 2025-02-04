# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..scenario_environment_param import ScenarioEnvironmentParam

__all__ = ["ScorerValidateParams"]


class ScorerValidateParams(TypedDict, total=False):
    scoring_context: Required[object]
    """Json context that gets passed to the custom scorer"""

    environment_parameters: ScenarioEnvironmentParam
    """The Environment in which the Scenario will run."""
