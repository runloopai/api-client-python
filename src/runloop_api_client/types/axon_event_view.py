# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AxonEventView"]


class AxonEventView(BaseModel):
    axon_id: str
    """The axon identifier."""

    event_type: str
    """Event type (e.g. push, pull_request)."""

    origin: Literal["EXTERNAL_EVENT", "AGENT_EVENT", "USER_EVENT", "SYSTEM_EVENT"]
    """Event origin."""

    payload: str
    """JSON-encoded event payload."""

    sequence: int
    """Monotonic sequence number."""

    source: str
    """Event source (e.g. github, slack)."""

    timestamp_ms: int
    """Timestamp in milliseconds since epoch."""
