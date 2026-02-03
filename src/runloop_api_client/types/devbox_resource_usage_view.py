# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DevboxResourceUsageView"]


class DevboxResourceUsageView(BaseModel):
    id: str
    """The devbox ID."""

    disk_gb_seconds: int
    """Disk usage in GB-seconds (total_elapsed_seconds multiplied by disk size in GB).

    Disk is billed for elapsed time since storage is consumed even when suspended.
    """

    memory_gb_seconds: int
    """Memory usage in GB-seconds (total_active_seconds multiplied by memory in GB)."""

    start_time_ms: int
    """The devbox creation time in milliseconds since epoch."""

    status: str
    """The current status of the devbox."""

    total_active_seconds: int
    """
    Total time in seconds the devbox was actively running (excludes time spent
    suspended).
    """

    total_elapsed_seconds: int
    """
    Total elapsed time in seconds from devbox creation to now (or end time if
    terminated). Includes all time regardless of devbox state.
    """

    vcpu_seconds: int
    """
    vCPU usage in vCPU-seconds (total_active_seconds multiplied by the number of
    vCPUs).
    """

    end_time_ms: Optional[int] = None
    """The devbox end time in milliseconds since epoch, or null if still running."""
