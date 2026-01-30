# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from .after_idle import AfterIdle

__all__ = ["LaunchParameters", "UserParameters"]


class UserParameters(TypedDict, total=False):
    """Specify the user for execution on Devbox.

    If not set, default `user` will be used.
    """

    uid: Required[int]
    """User ID (UID) for the Linux user. Must be a non-negative integer."""

    username: Required[str]
    """Username for the Linux user."""


class LaunchParameters(TypedDict, total=False):
    """
    LaunchParameters enable you to customize the resources available to your Devbox as well as the environment set up that should be completed before the Devbox is marked as 'running'.
    """

    after_idle: Optional[AfterIdle]
    """Configure Devbox lifecycle based on idle activity.

    If after_idle is set, Devbox will ignore keep_alive_time_seconds.
    """

    architecture: Optional[Literal["x86_64", "arm64"]]
    """The target architecture for the Devbox. If unset, defaults to x86_64."""

    available_ports: Optional[Iterable[int]]
    """A list of ports to make available on the Devbox.

    Only ports made available will be surfaced to create tunnels via the
    'createTunnel' API.
    """

    custom_cpu_cores: Optional[int]
    """Custom CPU cores. Must be 0.5, 1, or a multiple of 2. Max is 16."""

    custom_disk_size: Optional[int]
    """Custom disk size in GiB. Must be a multiple of 2. Min is 2GiB, max is 64GiB."""

    custom_gb_memory: Optional[int]
    """Custom memory size in GiB. Must be 1 or a multiple of 2. Max is 64GiB."""

    keep_alive_time_seconds: Optional[int]
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour. Maximum is 48 hours (172800 seconds).
    """

    launch_commands: Optional[SequenceNotStr[str]]
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    network_policy_id: Optional[str]
    """
    (Optional) ID of the network policy to apply to Devboxes launched with these
    parameters. When set on a Blueprint launch parameters, Devboxes created from it
    will inherit this policy unless explicitly overridden.
    """

    required_services: Optional[SequenceNotStr[str]]
    """A list of ContainerizedService names to be started when a Devbox is created.

    A valid ContainerizedService must be specified in Blueprint to be started.
    """

    resource_size_request: Optional[
        Literal["X_SMALL", "SMALL", "MEDIUM", "LARGE", "X_LARGE", "XX_LARGE", "CUSTOM_SIZE"]
    ]
    """Manual resource configuration for Devbox. If not set, defaults will be used."""

    user_parameters: Optional[UserParameters]
    """Specify the user for execution on Devbox.

    If not set, default `user` will be used.
    """
