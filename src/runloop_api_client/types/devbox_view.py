# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DevboxView"]


class DevboxView(BaseModel):
    id: Optional[str] = None
    """The id of the Devbox."""

    blueprint_id: Optional[str] = None
    """The Blueprint ID used in creation of the Devbox, if any."""

    create_time_ms: Optional[int] = None
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    end_time_ms: Optional[int] = None
    """The time the Devbox finished execution (Unix timestamp milliseconds)."""

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "execution_failed"]] = None
    """The failure reason if the Devbox failed, if any."""

    initiator_id: Optional[str] = None
    """The initiator ID of the devbox."""

    initiator_type: Optional[Literal["unknown", "api", "invocation"]] = None
    """The initiator of the devbox."""

    metadata: Optional[Dict[str, str]] = None
    """The user defined Devbox metadata."""

    name: Optional[str] = None
    """The name of the Devbox."""

    status: Optional[Literal["provisioning", "initializing", "running", "failure", "shutdown"]] = None
    """The current status of the Devbox."""
