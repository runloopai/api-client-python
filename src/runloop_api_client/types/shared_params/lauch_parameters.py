# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .resource_size import ResourceSize
from ..resource_size import ResourceSize

__all__ = ["LauchParameters"]


class LauchParameters(TypedDict, total=False):
    keep_alive_time_seconds: int
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: List[str]
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: ResourceSize
    """Manual resource configuration for Devbox. If not set, defaults will be used."""
