# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .after_idle import AfterIdle

__all__ = ["LaunchParameters", "UserParameters"]


class UserParameters(BaseModel):
    uid: int
    """User ID (UID) for the Linux user. Must be a positive integer."""

    username: str
    """Username for the Linux user."""


class LaunchParameters(BaseModel):
    after_idle: Optional[AfterIdle] = None
    """Configure Devbox lifecycle based on idle activity.

    If after_idle is set, Devbox will ignore keep_alive_time_seconds.
    """

    architecture: Optional[Literal["x86_64", "arm64"]] = None
    """The target architecture for the Devbox. If unset, defaults to arm64."""

    available_ports: Optional[List[int]] = None
    """A list of ports to make available on the Devbox.

    Only ports made available will be surfaced to create tunnels via the
    'createTunnel' API.
    """

    custom_cpu_cores: Optional[int] = None
    """custom resource size, number of cpu cores, must be multiple of 2.

    Min is 1, max is 16.
    """

    custom_disk_size: Optional[int] = None
    """custom disk size, number in GiB, must be a multiple of 2.

    Min is 2GiB, max is 64GiB.
    """

    custom_gb_memory: Optional[int] = None
    """custom memory size, number in GiB, must be a multiple of 2.

    Min is 2GiB, max is 64GiB.
    """

    keep_alive_time_seconds: Optional[int] = None
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour. Maximum is 48 hours (172800 seconds).
    """

    launch_commands: Optional[List[str]] = None
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    required_services: Optional[List[str]] = None
    """A list of ContainerizedService names to be started when a Devbox is created.

    A valid ContainerizedService must be specified in Blueprint to be started.
    """

    resource_size_request: Optional[
        Literal["X_SMALL", "SMALL", "MEDIUM", "LARGE", "X_LARGE", "XX_LARGE", "CUSTOM_SIZE"]
    ] = None
    """Manual resource configuration for Devbox. If not set, defaults will be used."""

    user_parameters: Optional[UserParameters] = None
    """Specify the user for execution on Devbox.

    If not set, default `user` will be used.
    """
