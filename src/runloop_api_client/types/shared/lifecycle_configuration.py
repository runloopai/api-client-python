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
    """Optional lifecycle hooks.

    suspend_commands run through the suspend path before the Devbox suspends; see
    launch_commands for work on every startup.
    """

    resume_triggers: Optional[ResumeTriggers] = None
    """Triggers that can resume a suspended Devbox."""
