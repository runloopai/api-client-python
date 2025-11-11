from __future__ import annotations

import asyncio
import logging
from typing import Optional, Awaitable, cast

from .._client import AsyncRunloop
from ..lib.polling import PollingConfig
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
        self._latest = execution
        self._streaming_group = streaming_group

    @property
    def execution_id(self) -> str:
        return self._execution_id

    @property
    def devbox_id(self) -> str:
        return self._devbox_id

    async def result(self, *, polling_config: PollingConfig | None = None) -> AsyncExecutionResult:
        async def command_coro() -> DevboxAsyncExecutionDetailView:
            if self._latest.status == "completed":
                return self._latest
            return await self._client.devboxes.executions.await_completed(
                self._execution_id,
                devbox_id=self._devbox_id,
                polling_config=polling_config,
            )

        awaitables: list[Awaitable[DevboxAsyncExecutionDetailView | None]] = [command_coro()]
        if self._streaming_group is not None:
            awaitables.append(self._streaming_group.wait())

        results = await asyncio.gather(*awaitables, return_exceptions=True)
        command_result = results[0]

        if isinstance(command_result, Exception):
            if self._streaming_group is not None:
                await self._streaming_group.cancel()
            raise command_result

        if self._streaming_group is not None:
            self._streaming_group = None

        # Streaming completion is orchestrated via the gather call above.
        command_value = cast(DevboxAsyncExecutionDetailView, command_result)
        self._latest = command_value
        return AsyncExecutionResult(self._client, self._devbox_id, command_value)

    async def get_state(self) -> DevboxAsyncExecutionDetailView:
        self._latest = await self._client.devboxes.executions.retrieve(
            self._execution_id,
            devbox_id=self._devbox_id,
        )
        return self._latest

    async def kill(self, *, kill_process_group: bool | None = None) -> None:
        await self._client.devboxes.executions.kill(
            self._execution_id,
            devbox_id=self._devbox_id,
            kill_process_group=kill_process_group,
        )
        await self._settle_streaming(cancel=True)

    async def _settle_streaming(self, *, cancel: bool) -> None:
        if self._streaming_group is None:
            return
        if cancel:
            await self._streaming_group.cancel()
        else:
            await self._streaming_group.wait()
        self._streaming_group = None
