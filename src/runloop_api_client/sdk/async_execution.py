"""Async execution management for async commands."""

from __future__ import annotations

import asyncio
import logging
from typing import Optional, Awaitable, cast
from typing_extensions import Unpack, override

from ._types import RequestOptions, LongRequestOptions
from .._client import AsyncRunloop
from .async_execution_result import AsyncExecutionResult
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView


class _AsyncStreamingGroup:
    """
    Internal helper to manage background streaming tasks.
    """

    def __init__(self, tasks: list[asyncio.Task[None]]) -> None:
        self._tasks = tasks
        self._logger = logging.getLogger(__name__)

    async def wait(self) -> None:
        results = await asyncio.gather(*self._tasks, return_exceptions=True)
        self._log_results(tuple(results))

    async def cancel(self) -> None:
        for task in self._tasks:
            task.cancel()
        results = await asyncio.gather(*self._tasks, return_exceptions=True)
        self._log_results(tuple(results))

    def _log_results(self, results: tuple[object | BaseException | None, ...]) -> None:
        for result in results:
            if isinstance(result, Exception) and not isinstance(result, asyncio.CancelledError):
                self._logger.debug("stream task error: %s", result)


class AsyncExecution:
    """
    Represents an asynchronous command execution on a devbox.
    """

    def __init__(
        self,
        client: AsyncRunloop,
        devbox_id: str,
        execution: DevboxAsyncExecutionDetailView,
        streaming_group: Optional[_AsyncStreamingGroup] = None,
    ) -> None:
        self._client = client
        self._devbox_id = devbox_id
        self._execution_id = execution.execution_id
        self._initial_result = execution
        self._streaming_group = streaming_group

    @override
    def __repr__(self) -> str:
        return f"<AsyncExecution id={self._execution_id!r}>"

    @property
    def execution_id(self) -> str:
        return self._execution_id

    @property
    def devbox_id(self) -> str:
        return self._devbox_id

    async def result(self, **options: Unpack[LongRequestOptions]) -> AsyncExecutionResult:
        # Wait for both command completion and streaming to finish
        awaitables: list[Awaitable[DevboxAsyncExecutionDetailView | None]] = [
            self._client.devboxes.wait_for_command(
                self._execution_id,
                devbox_id=self._devbox_id,
                statuses=["completed"],
                **options,
            )
        ]
        if self._streaming_group is not None:
            awaitables.append(self._streaming_group.wait())

        results = await asyncio.gather(*awaitables, return_exceptions=True)
        command_result = results[0]

        # Extract command result (throw if it failed, ignore streaming errors)
        if isinstance(command_result, Exception):
            raise command_result

        if self._streaming_group is not None:
            self._streaming_group = None

        # Streaming errors are already logged in _AsyncStreamingGroup._log_results()
        final = cast(DevboxAsyncExecutionDetailView, command_result)
        return AsyncExecutionResult(self._client, self._devbox_id, final)

    async def get_state(self, **options: Unpack[RequestOptions]) -> DevboxAsyncExecutionDetailView:
        return await self._client.devboxes.executions.retrieve(
            self._execution_id,
            devbox_id=self._devbox_id,
            **options,
        )

    async def kill(self, **options: Unpack[LongRequestOptions]) -> None:
        await self._client.devboxes.executions.kill(
            self._execution_id,
            devbox_id=self._devbox_id,
            **options,
        )
