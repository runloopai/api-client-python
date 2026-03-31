# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .after_idle import AfterIdle

__all__ = ["LaunchParameters", "UserParameters"]


class UserParameters(BaseModel):
    """Specify the user for execution on Devbox.

    If not set, default `user` will be used.
    """

    uid: int
    """User ID (UID) for the Linux user. Must be a non-negative integer."""

    username: str
    """Username for the Linux user."""


class LaunchParameters(BaseModel):
    """
    LaunchParameters enable you to customize the resources available to your Devbox as well as the environment set up that should be completed before the Devbox is marked as 'running'.
    """

    after_idle: Optional[AfterIdle] = None
    """Configure Devbox lifecycle based on idle activity.

    If after_idle is set, Devbox will ignore keep_alive_time_seconds.
    """

    architecture: Optional[Literal["x86_64", "arm64"]] = None
    """The target architecture for the Devbox. If unset, defaults to x86_64."""

    available_ports: Optional[List[int]] = None
    """[Deprecated] A list of ports to make available on the Devbox.

    This field is ignored.
    """

    custom_cpu_cores: Optional[int] = None
    """Custom CPU cores. Must be 0.5, 1, or a multiple of 2. Max is 16."""

    custom_disk_size: Optional[int] = None
    """Custom disk size in GiB. Must be a multiple of 2. Min is 2GiB, max is 64GiB."""

    custom_gb_memory: Optional[int] = None
    """Custom memory size in GiB. Must be 1 or a multiple of 2. Max is 64GiB."""

    keep_alive_time_seconds: Optional[int] = None
    """Time in seconds after which Devbox will automatically shutdown.

    Default is 1 hour. Maximum is 48 hours (172800 seconds).
    """

    launch_commands: Optional[List[str]] = None
    """Set of commands to be run at launch time, before the entrypoint process is run."""

    network_policy_id: Optional[str] = None
    """
    (Optional) ID of the network policy to apply to Devboxes launched with these
    parameters. When set on a Blueprint launch parameters, Devboxes created from it
    will inherit this policy unless explicitly overridden.
    """

    required_services: Optional[List[str]] = None
    """A list of ContainerizedService names to be started when a Devbox is created.

    A valid ContainerizedService must be specified in Blueprint to be started.
    """

    resource_size_request: Optional[
        Literal["X_SMALL", "SMALL", "MEDIUM", "LARGE", "X_LARGE", "XX_LARGE", "CUSTOM_SIZE"]
    ] = None
    """Preset Devbox resources (vCPU, RAM in GiB, ephemeral disk in GiB).

    If not set, SMALL is used. X_SMALL: 0.5 vCPU, 1 GiB RAM, 4 GiB disk. SMALL: 1
    vCPU, 2 GiB RAM, 4 GiB disk. MEDIUM: 2 vCPU, 4 GiB RAM, 8 GiB disk. LARGE: 2
    vCPU, 8 GiB RAM, 16 GiB disk. X_LARGE: 4 vCPU, 16 GiB RAM, 16 GiB disk.
    XX_LARGE: 8 vCPU, 32 GiB RAM, 16 GiB disk. CUSTOM_SIZE: set custom_cpu_cores,
    custom_gb_memory, and optionally custom_disk_size.
    """

    user_parameters: Optional[UserParameters] = None
    """Specify the user for execution on Devbox.

    If not set, default `user` will be used.
    """
