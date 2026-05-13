# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from .after_idle import AfterIdle

__all__ = ["LaunchParameters", "Lifecycle", "LifecycleLifecycleHooks", "LifecycleResumeTriggers", "UserParameters"]


class LifecycleLifecycleHooks(TypedDict, total=False):
    """Optional lifecycle hooks.

    suspend_commands run through the suspend path before the Devbox suspends; see launch_commands for work on every startup.
    """

    suspend_commands: Optional[SequenceNotStr[str]]
    """Commands to run through the suspend path before the Devbox suspends (e.g.

    cleanup, quiesce daemons).
    """

    suspend_deadline_ms: Optional[int]
    """Deadline in milliseconds for broker drain and suspend_commands during suspend.

    Defaults to 30000 ms and may not exceed 60000 ms. If exceeded, suspend work is
    abandoned, the timeout is logged, and the Devbox still proceeds to suspend by
    shutting down vmagent and killing the VM.
    """


class LifecycleResumeTriggers(TypedDict, total=False):
    """Triggers that can resume a suspended Devbox."""

    axon_event: Optional[bool]
    """When true, axon events targeting a suspended Devbox will trigger a resume."""

    http: Optional[bool]
    """When true, HTTP traffic to a suspended Devbox via tunnel will trigger a resume."""


class Lifecycle(TypedDict, total=False):
    """Lifecycle configuration for idle and resume behavior.

    Configure idle policy via lifecycle.after_idle (if both this and the top-level after_idle are set, they must match), resume triggers via lifecycle.resume_triggers, and optional lifecycle hooks via lifecycle.lifecycle_hooks.
    """

    after_idle: Optional[AfterIdle]
    """Configure Devbox lifecycle based on idle activity.

    If both this and the top-level after_idle are set, they must have the same
    value. Prefer this field for new integrations.
    """

    lifecycle_hooks: Optional[LifecycleLifecycleHooks]
    """Optional lifecycle hooks.

    suspend_commands run through the suspend path before the Devbox suspends; see
    launch_commands for work on every startup.
    """

    resume_triggers: Optional[LifecycleResumeTriggers]
    """Triggers that can resume a suspended Devbox."""


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

    If after_idle is set, Devbox will ignore keep_alive_time_seconds. If both
    after_idle and lifecycle.after_idle are set, they must have the same value. Use
    lifecycle.after_idle instead.
    """

    architecture: Optional[Literal["x86_64", "arm64"]]
    """The target architecture for the Devbox. If unset, defaults to x86_64."""

    available_ports: Optional[Iterable[int]]
    """[Deprecated] A list of ports to make available on the Devbox.

    This field is ignored.
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

    lifecycle: Optional[Lifecycle]
    """Lifecycle configuration for idle and resume behavior.

    Configure idle policy via lifecycle.after_idle (if both this and the top-level
    after_idle are set, they must match), resume triggers via
    lifecycle.resume_triggers, and optional lifecycle hooks via
    lifecycle.lifecycle_hooks.
    """

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
    """Preset Devbox resources (vCPU, RAM in GiB, ephemeral disk in GiB).

    If not set, SMALL is used. X_SMALL: 0.5 vCPU, 1 GiB RAM, 4 GiB disk. SMALL: 1
    vCPU, 2 GiB RAM, 4 GiB disk. MEDIUM: 2 vCPU, 4 GiB RAM, 8 GiB disk. LARGE: 2
    vCPU, 8 GiB RAM, 16 GiB disk. X_LARGE: 4 vCPU, 16 GiB RAM, 16 GiB disk.
    XX_LARGE: 8 vCPU, 32 GiB RAM, 16 GiB disk. CUSTOM_SIZE: set custom_cpu_cores,
    custom_gb_memory, and optionally custom_disk_size.
    """

    user_parameters: Optional[UserParameters]
    """Specify the user for execution on Devbox.

    If not set, default `user` will be used.
    """
