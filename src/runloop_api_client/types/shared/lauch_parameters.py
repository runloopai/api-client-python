# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from ..resource_size import ResourceSize

__all__ = ["LauchParameters"]


class LauchParameters(BaseModel):
    keep_alive_time_seconds: Optional[int] = None
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: Optional[List[str]] = None
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: Optional[ResourceSize] = None
    """Manual resource configuration for Devbox. If not set, defaults will be used."""
