# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ResumeTriggers"]


class ResumeTriggers(BaseModel):
    """Triggers that can resume a suspended Devbox."""

    axon_event: Optional[bool] = None
    """When true, axon events targeting a suspended Devbox will trigger a resume."""

    http: Optional[bool] = None
    """When true, HTTP traffic to a suspended Devbox via tunnel will trigger a resume."""
