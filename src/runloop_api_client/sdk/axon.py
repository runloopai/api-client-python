"""Axon resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
    SDKAxonPublishParams,
)
from .._client import Runloop
from .._streaming import Stream
from ..types.axon_view import AxonView
from ..types.axon_event_view import AxonEventView
from ..types.publish_result_view import PublishResultView


class Axon:
    """[Beta] Wrapper around synchronous axon operations.

    Axons are event communication channels that support publishing events
    and subscribing to event streams via server-sent events (SSE).
    Obtain instances via ``runloop.axon.create()`` or ``runloop.axon.from_id()``.

    Example:
        >>> runloop = RunloopSDK()
        >>> axon = runloop.axon.create()
        >>> axon.publish(event_type="task_done", origin="AGENT_EVENT", payload="{}", source="my-agent")
    """

    def __init__(self, client: Runloop, axon_id: str) -> None:
        self._client = client
        self._id = axon_id

    @override
    def __repr__(self) -> str:
        return f"<Axon id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    def get_info(self, **options: Unpack[BaseRequestOptions]) -> AxonView:
        """[Beta] Retrieve the latest axon information."""
        return self._client.axons.retrieve(self._id, **options)

    def publish(self, **params: Unpack[SDKAxonPublishParams]) -> PublishResultView:
        """[Beta] Publish an event to this axon."""
        return self._client.axons.publish(self._id, **params)

    def subscribe_sse(self, **options: Unpack[BaseRequestOptions]) -> Stream[AxonEventView]:
        """[Beta] Subscribe to this axon's event stream via SSE."""
        return self._client.axons.subscribe_sse(self._id, **options)
