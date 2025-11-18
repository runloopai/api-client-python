# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.launch_parameters import LaunchParameters

__all__ = ["DevboxView", "StateTransition"]


class StateTransition(BaseModel):
    status: Optional[
        Literal["provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"]
    ] = None
    """The status of the Devbox.

    provisioning: Runloop is allocating and booting the necessary infrastructure
    resources. initializing: Runloop defined boot scripts are running to enable the
    environment for interaction. running: The Devbox is ready for interaction.
    suspending: The Devbox disk is being snapshotted as part of suspension.
    suspended: The Devbox disk is saved and no more active compute is being used for
    the Devbox. resuming: The Devbox disk is being loaded as part of booting a
    suspended Devbox. failure: The Devbox failed as part of booting or running user
    requested actions. shutdown: The Devbox was successfully shutdown and no more
    active compute is being used.
    """

    transition_time_ms: Optional[object] = None
    """The time the status change occurred"""


class DevboxView(BaseModel):
    id: str
    """The ID of the Devbox."""

    capabilities: List[Literal["unknown", "computer_usage", "browser_usage", "docker_in_docker"]]
    """A list of capability groups this devbox has access to.

    This allows devboxes to be compatible with certain tools sets like computer
    usage APIs.
    """

    create_time_ms: int
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    end_time_ms: Optional[int] = None
    """The time the Devbox finished execution (Unix timestamp milliseconds).

    Present if the Devbox is in a terminal state.
    """

    launch_parameters: LaunchParameters
    """The launch parameters used to create the Devbox."""

    metadata: Dict[str, str]
    """The user defined Devbox metadata."""

    state_transitions: List[StateTransition]
    """A list of state transitions in order with durations"""

    status: Literal[
        "provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"
    ]
    """The current status of the Devbox."""

    blueprint_id: Optional[str] = None
    """
    The Blueprint ID used in creation of the Devbox, if the devbox was created from
    a Blueprint.
    """

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "execution_failed"]] = None
    """The failure reason if the Devbox failed, if the Devbox has a 'failure' status."""

    initiator_id: Optional[str] = None
    """The ID of the initiator that created the Devbox."""

    initiator_type: Optional[Literal["unknown", "api", "scenario"]] = None
    """The type of initiator that created the Devbox."""

    name: Optional[str] = None
    """The name of the Devbox."""

    shutdown_reason: Optional[Literal["api_shutdown", "keep_alive_timeout", "entrypoint_exit", "idle"]] = None
    """
    The shutdown reason if the Devbox shutdown, if the Devbox has a 'shutdown'
    status.
    """

    snapshot_id: Optional[str] = None
    """
    The Snapshot ID used in creation of the Devbox, if the devbox was created from a
    Snapshot.
    """
