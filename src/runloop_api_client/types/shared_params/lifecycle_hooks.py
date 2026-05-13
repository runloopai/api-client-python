# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from ..._types import SequenceNotStr

__all__ = ["LifecycleHooks"]


class LifecycleHooks(TypedDict, total=False):
    """Lifecycle hooks for Devbox suspend.

    suspend_commands run sequentially as the configured Devbox user through the rage/vmagent suspend path before the Devbox suspends; failures are logged but do not block suspending. The suspend_deadline_ms budget defaults to 30000 ms, may not exceed 60000 ms, and covers broker drain plus suspend_commands. If the deadline is exceeded, suspend work is abandoned, the timeout is logged, and the Devbox still proceeds to suspend by shutting down vmagent and killing the VM. Resume hooks and resume deadline settings are persistence/internal only and hidden from the public API reference. launch_commands still run on every startup, including after resume.
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
