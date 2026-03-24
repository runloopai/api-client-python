# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AxonPublishParams"]


class AxonPublishParams(TypedDict, total=False):
    event_type: Required[str]
    """The event type (e.g. push, pull_request)."""

    origin: Required[Literal["EXTERNAL_EVENT", "AGENT_EVENT", "USER_EVENT"]]
    """Event origin."""

    payload: Required[str]
    """Event payload."""

    source: Required[str]
    """The source of the event (e.g. github, slack)."""
