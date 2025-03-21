# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Literal, TypedDict

from .after_idle import AfterIdle

__all__ = ["LaunchParameters"]


class LaunchParameters(TypedDict, total=False):
    after_idle: Optional[AfterIdle]
    """Configure Devbox lifecycle based on idle activity.

    If after_idle is set, Devbox will ignore keep_alive_time_seconds.
    """

    available_ports: Optional[Iterable[int]]
    """A list of ports to make available on the Devbox.

    Only ports made available will be surfaced to create tunnels via the
    'createTunnel' API.
    """

    custom_cpu_cores: Optional[int]
    """custom resource size, number of cpu cores, must be multiple of 2."""

    custom_gb_memory: Optional[int]
    """custom memory size, number in Gi, must be a multiple of 2."""

    keep_alive_time_seconds: Optional[int]
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: Optional[List[str]]
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: Optional[Literal["SMALL", "MEDIUM", "LARGE", "X_LARGE", "XX_LARGE", "CUSTOM_SIZE"]]
    """Manual resource configuration for Devbox. If not set, defaults will be used."""
