# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RepositoryVersionDetails", "ExtractedTools", "RepositorySetupDetails"]


class ExtractedTools(BaseModel):
    commands: Dict[str, str]
    """The set of available commands on this repository such as building etc."""

    package_manager: str
    """What package manager this repository uses."""


class RepositorySetupDetails(BaseModel):
    blueprint_id: str
    """The blueprint built that supports setting up this repository."""

    env_initialization_command: str
    """Command to initialize the env we need to run the commands for this repository."""

    workspace_setup: List[str]
    """Setup commands necessary to support repository i.e. apt install XXX."""


class RepositoryVersionDetails(BaseModel):
    analyzed_at: int
    """Analyzed time of the Repository Version (Unix timestamp milliseconds)."""

    commit_sha: str
    """The sha of the analyzed version of the Repository."""

    extracted_tools: ExtractedTools
    """Tools discovered during inspection."""

    repository_setup_details: RepositorySetupDetails
    """Commands required to set up repository environment."""

    status: Literal["inspecting", "inspection_failed", "success"]
    """The account owner of the Repository."""
