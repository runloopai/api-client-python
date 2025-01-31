# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.launch_parameters import LaunchParameters

__all__ = ["DevboxView"]


class DevboxView(BaseModel):
    id: str
    """The ID of the Devbox."""

    capabilities: List[Literal["unknown", "computer_usage", "browser_usage"]]
    """A list of capability groups this devbox has access to.

    This allows devboxes to be compatible with certain tools sets like computer
    usage APIs.
    """

    create_time_ms: int
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    launch_parameters: LaunchParameters
    """The launch parameters used to create the Devbox."""

    metadata: Dict[str, str]
    """The user defined Devbox metadata."""

    status: Literal[
        "provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"
    ]
    """The current status of the Devbox."""

    blueprint_id: Optional[str] = None
    """
    The Blueprint ID used in creation of the Devbox, if the devbox was created from
    a Blueprint.
    """

    end_time_ms: Optional[int] = None
    """The time the Devbox finished execution (Unix timestamp milliseconds).

    Present if the Devbox is in a terminal state.
    """

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "execution_failed"]] = None
    """The failure reason if the Devbox failed, if the Devbox has a 'failure' status."""

    name: Optional[str] = None
    """The name of the Devbox."""

    shutdown_reason: Optional[
        Literal["api_shutdown", "keep_alive_timeout", "entrypoint_exit", "idle", "lambda_lifecycle"]
    ] = None
    """
    The shutdown reason if the Devbox shutdown, if the Devbox has a 'shutdown'
    status.
    """

    snapshot_id: Optional[str] = None
    """
    The Snapshot ID used in creation of the Devbox, if the devbox was created from a
    Snapshot.
    """
