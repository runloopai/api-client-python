# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DevboxSendStdInResult"]


class DevboxSendStdInResult(BaseModel):
    devbox_id: str
    """Devbox id where command is executing."""

    execution_id: str
    """Execution id that received the stdin."""

    success: bool
    """Whether the stdin was successfully sent."""
