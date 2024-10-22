# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.launch_parameters import LaunchParameters

__all__ = ["DevboxView"]


class DevboxView(BaseModel):
    id: str
    """The id of the Devbox."""

    create_time_ms: int
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    initiator_id: str
    """The initiator ID of the devbox."""

    initiator_type: Literal["unknown", "api", "invocation"]
    """The initiator of the devbox."""

    launch_parameters: LaunchParameters
    """The launch parameters used to create the Devbox."""

    metadata: Dict[str, str]
    """The user defined Devbox metadata."""

    status: Literal["provisioning", "initializing", "running", "failure", "shutdown"]
    """The current status of the Devbox."""

    blueprint_id: Optional[str] = None
    """The Blueprint ID used in creation of the Devbox, if any."""

    end_time_ms: Optional[int] = None
    """The time the Devbox finished execution (Unix timestamp milliseconds)."""

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "execution_failed"]] = None
    """The failure reason if the Devbox failed, if any."""

    name: Optional[str] = None
    """The name of the Devbox."""

    shutdown_reason: Optional[Literal["api_shutdown", "keep_alive_timeout", "entrypoint_exit"]] = None
    """The shutdown reason if the Devbox shutdown, if any."""
