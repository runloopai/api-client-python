# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .shared_params.launch_parameters import LaunchParameters

__all__ = ["ScenarioEnvironmentParam"]


class ScenarioEnvironmentParam(TypedDict, total=False):
    """
    ScenarioEnvironmentParameters specify the environment in which a Scenario will be run.
    """

    blueprint_id: Optional[str]
    """Use the blueprint with matching ID."""

    launch_parameters: Optional[LaunchParameters]
    """
    LaunchParameters enable you to customize the resources available to your Devbox
    as well as the environment set up that should be completed before the Devbox is
    marked as 'running'.
    """

    snapshot_id: Optional[str]
    """Use the snapshot with matching ID."""

    working_directory: Optional[str]
    """The working directory where the agent is expected to fulfill the scenario.

    Scoring functions also run from the working directory.
    """
