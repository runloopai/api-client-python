"""Asynchronous devbox resource class."""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Callable, Optional, Sequence, Awaitable, cast
from typing_extensions import override

from ..types import (
    DevboxView,
    DevboxTunnelView,
    DevboxExecutionDetailView,
    DevboxCreateSSHKeyResponse,
)
from .._types import Body, Omit, Query, Headers, Timeout, NotGiven, FileTypes, omit, not_given
from .._client import AsyncRunloop
from ._helpers import LogCallback
from .protocols import AsyncFileInterface, AsyncCommandInterface, AsyncNetworkInterface
from .._streaming import AsyncStream
from ..lib.polling import PollingConfig
from .async_execution import AsyncExecution, _AsyncStreamingGroup
from .async_execution_result import AsyncExecutionResult
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView

StreamFactory = Callable[[], Awaitable[AsyncStream[ExecutionUpdateChunk]]]

if TYPE_CHECKING:
    from .async_snapshot import AsyncSnapshot


class AsyncDevbox:
    """
    Async object-oriented wrapper around devbox operations.
    """

    def __init__(self, client: AsyncRunloop, devbox_id: str) -> None:
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    @override
    def __repr__(self) -> str:
        return f"<AsyncDevbox id={self._id!r}>"

    async def __aenter__(self) -> "AsyncDevbox":
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        try:
            await self.shutdown()
        except Exception:
            self._logger.exception("failed to shutdown async devbox %s on context exit", self._id)

    @property
    def id(self) -> str:
        return self._id

    async def get_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> DevboxView:
        return await self._client.devboxes.retrieve(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def await_running(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        return await self._client.devboxes.await_running(self._id, polling_config=polling_config)

    async def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        return await self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    async def shutdown(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        return await self._client.devboxes.shutdown(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def suspend(
        self,
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        await self._client.devboxes.suspend(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return await self._client.devboxes.await_suspended(
            self._id,
            polling_config=polling_config,
        )

    async def resume(
        self,
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        await self._client.devboxes.resume(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return await self._client.devboxes.await_running(
            self._id,
            polling_config=polling_config,
        )

    async def keep_alive(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return await self._client.devboxes.keep_alive(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def snapshot_disk(
        self,
        *,
        commit_message: str | None | Omit = omit,
        metadata: dict[str, str] | None | Omit = omit,
        name: str | None | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> "AsyncSnapshot":
        snapshot_data = await self._client.devboxes.snapshot_disk_async(
            self._id,
            commit_message=commit_message,
            metadata=metadata,
            name=name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        snapshot = self._snapshot_from_id(snapshot_data.id)
        await snapshot.await_completed(
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return snapshot

    async def snapshot_disk_async(
        self,
        *,
        commit_message: str | None | Omit = omit,
        metadata: dict[str, str] | None | Omit = omit,
        name: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> "AsyncSnapshot":
        snapshot_data = await self._client.devboxes.snapshot_disk_async(
            self._id,
            commit_message=commit_message,
            metadata=metadata,
            name=name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return self._snapshot_from_id(snapshot_data.id)

    async def close(self) -> None:
        await self.shutdown()

    @property
    def cmd(self) -> AsyncCommandInterface:
        return _AsyncCommandInterface(self)

    @property
    def file(self) -> AsyncFileInterface:
        return _AsyncFileInterface(self)

    @property
    def net(self) -> AsyncNetworkInterface:
        return _AsyncNetworkInterface(self)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _snapshot_from_id(self, snapshot_id: str) -> "AsyncSnapshot":
        from .async_snapshot import AsyncSnapshot

        return AsyncSnapshot(self._client, snapshot_id)

    def _start_streaming(
        self,
        execution_id: str,
        *,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
    ) -> Optional[_AsyncStreamingGroup]:
        tasks: list[asyncio.Task[None]] = []

        if stdout or output:
            callbacks = [cb for cb in (stdout, output) if cb is not None]
            tasks.append(
                asyncio.create_task(
                    self._stream_worker(
                        name="stdout",
                        stream_factory=lambda: self._client.devboxes.executions.stream_stdout_updates(
                            execution_id,
                            devbox_id=self._id,
                        ),
                        callbacks=callbacks,
                    )
                )
            )

        if stderr or output:
            callbacks = [cb for cb in (stderr, output) if cb is not None]
            tasks.append(
                asyncio.create_task(
                    self._stream_worker(
                        name="stderr",
                        stream_factory=lambda: self._client.devboxes.executions.stream_stderr_updates(
                            execution_id,
                            devbox_id=self._id,
                        ),
                        callbacks=callbacks,
                    )
                )
            )

        if not tasks:
            return None

        return _AsyncStreamingGroup(tasks)

    async def _stream_worker(
        self,
        *,
        name: str,
        stream_factory: StreamFactory,
        callbacks: Sequence[LogCallback],
    ) -> None:
        logger = self._logger
        try:
            stream = await stream_factory()
            async with stream:
                async for chunk in stream:
                    text = chunk.output
                    for callback in callbacks:
                        try:
                            callback(text)
                        except Exception:
                            logger.exception("error in async %s callback for devbox %s", name, self._id)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("error streaming %s logs for devbox %s", name, self._id)


class _AsyncCommandInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def exec(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = omit,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
        polling_config: PollingConfig | None = None,
        attach_stdin: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncExecutionResult:
        devbox = self._devbox
        client = devbox._client

        if stdout or stderr or output:
            execution: DevboxAsyncExecutionDetailView = await client.devboxes.execute_async(
                devbox.id,
                command=command,
                shell_name=shell_name,
                attach_stdin=attach_stdin,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            )
            streaming_group = devbox._start_streaming(
                execution.execution_id,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )

            async def command_coro() -> DevboxAsyncExecutionDetailView:
                if execution.status == "completed":
                    return execution
                return await client.devboxes.executions.await_completed(
                    execution.execution_id,
                    devbox_id=devbox.id,
                    polling_config=polling_config,
                )

            awaitables: list[Awaitable[DevboxAsyncExecutionDetailView | None]] = [command_coro()]
            if streaming_group is not None:
                awaitables.append(streaming_group.wait())

            results = await asyncio.gather(*awaitables, return_exceptions=True)
            command_result = results[0]

            if isinstance(command_result, Exception):
                if streaming_group is not None:
                    await streaming_group.cancel()
                raise command_result

            # Streaming finishes asynchronously via the shared gather call; nothing more to do here.
            command_value = cast(DevboxAsyncExecutionDetailView, command_result)
            return AsyncExecutionResult(client, devbox.id, command_value)

        final = await client.devboxes.execute_and_await_completion(
            devbox.id,
            command=command,
            shell_name=shell_name,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return AsyncExecutionResult(client, devbox.id, final)

    async def exec_async(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = omit,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
        attach_stdin: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncExecution:
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = await client.devboxes.execute_async(
            devbox.id,
            command=command,
            shell_name=shell_name,
            attach_stdin=attach_stdin,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

        streaming_group = devbox._start_streaming(
            execution.execution_id,
            stdout=stdout,
            stderr=stderr,
            output=output,
        )

        return AsyncExecution(client, devbox.id, execution, streaming_group)


class _AsyncFileInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def read(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        return await self._devbox._client.devboxes.read_file_contents(
            self._devbox.id,
            file_path=path,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def write(
        self,
        path: str,
        contents: str | bytes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView:
        if isinstance(contents, bytes):
            contents_str = contents.decode("utf-8")
        else:
            contents_str = contents

        return await self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            file_path=path,
            contents=contents_str,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def download(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> bytes:
        response = await self._devbox._client.devboxes.download_file(
            self._devbox.id,
            path=path,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return await response.read()

    async def upload(
        self,
        path: str,
        file: FileTypes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return await self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            path=path,
            file=file,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )


class _AsyncNetworkInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def create_ssh_key(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxCreateSSHKeyResponse:
        return await self._devbox._client.devboxes.create_ssh_key(
            self._devbox.id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def create_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxTunnelView:
        return await self._devbox._client.devboxes.create_tunnel(
            self._devbox.id,
            port=port,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    async def remove_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return await self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            port=port,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
