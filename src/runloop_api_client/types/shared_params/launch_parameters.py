# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, TypedDict

__all__ = ["LaunchParameters"]


class LaunchParameters(TypedDict, total=False):
    available_ports: Iterable[int]
    """A list of ports to make available on the Devbox.

    Call createTunnel to open a tunnel to the port.
    """

    keep_alive_time_seconds: int
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour.
    """

    launch_commands: List[str]
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    resource_size_request: Literal["SMALL", "MEDIUM", "LARGE", "X_LARGE", "CUSTOM_SIZE"]
    """Manual resource configuration for Devbox. If not set, defaults will be used."""
