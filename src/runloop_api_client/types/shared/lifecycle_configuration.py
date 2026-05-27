# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from .after_idle import AfterIdle
from .lifecycle_hooks import LifecycleHooks
from .resume_triggers import ResumeTriggers

__all__ = ["LifecycleConfiguration"]


class LifecycleConfiguration(BaseModel):
    """Lifecycle configuration for Devbox idle and resume behavior.

    Configure idle policy via after_idle, resume triggers via resume_triggers, and optional lifecycle hooks via lifecycle_hooks.
    """

    after_idle: Optional[AfterIdle] = None
    """Configure Devbox lifecycle based on idle activity.

    If both this and the top-level after_idle are set, they must have the same
    value. Prefer this field for new integrations.
    """

    lifecycle_hooks: Optional[LifecycleHooks] = None
    """Lifecycle hooks for Devbox suspend.

    suspend_commands run sequentially as the configured Devbox user through the
    rage/vmagent suspend path before the Devbox suspends; failures are logged but do
    not block suspending. The suspend_deadline_ms budget defaults to 30000 ms, may
    not exceed 60000 ms, and covers broker drain plus suspend_commands. If the
    deadline is exceeded, suspend work is abandoned, the timeout is logged, and the
    Devbox still proceeds to suspend by shutting down vmagent and killing the VM.
    Resume hooks and resume deadline settings are persistence/internal only and
    hidden from the public API reference. launch_commands still run on every
    startup, including after resume.
    """

    resume_triggers: Optional[ResumeTriggers] = None
    """Triggers that can resume a suspended Devbox."""
