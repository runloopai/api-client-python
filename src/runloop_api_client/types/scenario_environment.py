# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .shared.launch_parameters import LaunchParameters

__all__ = ["ScenarioEnvironment"]


class ScenarioEnvironment(BaseModel):
    blueprint_id: Optional[str] = None
    """Use the blueprint with matching ID."""

    launch_parameters: Optional[LaunchParameters] = None
    """Optional launch parameters to apply to the devbox environment at launch."""

    snapshot_id: Optional[str] = None
    """Use the snapshot with matching ID."""

    working_directory: Optional[str] = None
    """The working directory where the agent is expected to fulfill the scenario.

    Scoring functions also run from the working directory.
    """
