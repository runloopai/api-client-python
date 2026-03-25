"""Axon resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
    SDKAxonPublishParams,
    SDKAxonSqlBatchParams,
    SDKAxonSqlQueryParams,
)
from .._client import AsyncRunloop
from .._streaming import AsyncStream
from ..types.axon_view import AxonView
from ..types.axon_event_view import AxonEventView
from ..types.publish_result_view import PublishResultView
from ..types.axons.sql_batch_result_view import SqlBatchResultView
from ..types.axons.sql_query_result_view import SqlQueryResultView


class AsyncAxonSqlOps:
    """[Beta] Async SQL operations for an axon's SQLite database.

    Access via ``axon.sql``.

    Example:
        >>> axon = await runloop.axon.create()
        >>> await axon.sql.query(sql="CREATE TABLE tasks (id INTEGER PRIMARY KEY, name TEXT)")
        >>> result = await axon.sql.query(sql="SELECT * FROM tasks WHERE id = ?", params=[1])
    """

    def __init__(self, client: AsyncRunloop, axon_id: str) -> None:
        self._client = client
        self._axon_id = axon_id

    async def query(self, **params: Unpack[SDKAxonSqlQueryParams]) -> SqlQueryResultView:
        """[Beta] Execute a single parameterized SQL statement against this axon's SQLite database."""
        return await self._client.axons.sql.query(self._axon_id, **params)

    async def batch(self, **params: Unpack[SDKAxonSqlBatchParams]) -> SqlBatchResultView:
        """[Beta] Execute multiple SQL statements atomically within a single transaction."""
        return await self._client.axons.sql.batch(self._axon_id, **params)


class AsyncAxon:
    """[Beta] Wrapper around asynchronous axon operations.

    Axons are event communication channels that support publishing events,
    subscribing to event streams via server-sent events (SSE), and executing
    SQL queries against an embedded SQLite database.
    Obtain instances via ``runloop.axon.create()`` or ``runloop.axon.from_id()``.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> axon = await runloop.axon.create()
        >>> await axon.publish(event_type="task_done", origin="AGENT_EVENT", payload="{}", source="my-agent")
        >>> async with await axon.subscribe_sse() as stream:
        ...     async for event in stream:
        ...         print(event.event_type, event.payload)
        >>> await axon.sql.query(sql="CREATE TABLE tasks (id INTEGER PRIMARY KEY, name TEXT)")
    """

    def __init__(self, client: AsyncRunloop, axon_id: str) -> None:
        self._client = client
        self._id = axon_id
        self.sql = AsyncAxonSqlOps(client, axon_id)

    @override
    def __repr__(self) -> str:
        return f"<AsyncAxon id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    async def get_info(self, **options: Unpack[BaseRequestOptions]) -> AxonView:
        """[Beta] Retrieve the latest axon information."""
        return await self._client.axons.retrieve(self._id, **options)

    async def publish(self, **params: Unpack[SDKAxonPublishParams]) -> PublishResultView:
        """[Beta] Publish an event to this axon."""
        return await self._client.axons.publish(self._id, **params)

    async def subscribe_sse(self, **options: Unpack[BaseRequestOptions]) -> AsyncStream[AxonEventView]:
        """[Beta] Subscribe to this axon's event stream via SSE."""
        return await self._client.axons.subscribe_sse(self._id, **options)
