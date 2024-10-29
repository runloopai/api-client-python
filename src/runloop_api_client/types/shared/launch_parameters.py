# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LaunchParameters"]


class LaunchParameters(BaseModel):
    available_ports: Optional[List[int]] = None
    """A list of ports to make available on the Devbox.

    Call createTunnel to open a tunnel to the port.
    """

    keep_alive_time_seconds: Optional[int] = None
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: Optional[List[str]] = None
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: Optional[Literal["SMALL", "MEDIUM", "LARGE", "X_LARGE", "CUSTOM_SIZE"]] = None
    """Manual resource configuration for Devbox. If not set, defaults will be used."""