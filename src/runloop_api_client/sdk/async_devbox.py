"""Asynchronous devbox resource class."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Callable, Optional, Sequence, Awaitable, cast
from typing_extensions import Unpack, override

from ..types import (
    DevboxView,
    DevboxTunnelView,
    DevboxExecutionDetailView,
    DevboxCreateSSHKeyResponse,
)
from ._types import (
    LogCallback,
    RequestOptions,
    LongRequestOptions,
    PollingRequestOptions,
    SDKDevboxExecuteParams,
    ExecuteStreamingCallbacks,
    SDKDevboxUploadFileParams,
    SDKDevboxCreateTunnelParams,
    SDKDevboxDownloadFileParams,
    SDKDevboxExecuteAsyncParams,
    SDKDevboxRemoveTunnelParams,
    SDKDevboxSnapshotDiskParams,
    SDKDevboxReadFileContentsParams,
    SDKDevboxSnapshotDiskAsyncParams,
    SDKDevboxWriteFileContentsParams,
)
from .._client import AsyncRunloop
from ._helpers import filter_params
from .protocols import AsyncFileInterface, AsyncCommandInterface, AsyncNetworkInterface
from .._streaming import AsyncStream
from ..lib.polling import PollingConfig
from .async_execution import AsyncExecution, _AsyncStreamingGroup
from .async_execution_result import AsyncExecutionResult
from ..types.devbox_execute_async_params import DevboxExecuteAsyncParams
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
        **options: Unpack[RequestOptions],
    ) -> DevboxView:
        return await self._client.devboxes.retrieve(
            self._id,
            **options,
        )

    async def await_running(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        return await self._client.devboxes.await_running(self._id, polling_config=polling_config)

    async def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        return await self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    async def shutdown(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        return await self._client.devboxes.shutdown(
            self._id,
            **options,
        )

    async def suspend(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        return await self._client.devboxes.suspend(
            self._id,
            **options,
        )

    async def resume(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        return await self._client.devboxes.resume(
            self._id,
            **options,
        )

    async def keep_alive(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        return await self._client.devboxes.keep_alive(
            self._id,
            **options,
        )

    async def snapshot_disk(
        self,
        **params: Unpack[SDKDevboxSnapshotDiskParams],
    ) -> "AsyncSnapshot":
        snapshot_data = await self._client.devboxes.snapshot_disk_async(
            self._id,
            **filter_params(params, SDKDevboxSnapshotDiskAsyncParams),
        )
        snapshot = self._snapshot_from_id(snapshot_data.id)
        await snapshot.await_completed(**filter_params(params, PollingRequestOptions))
        return snapshot

    async def snapshot_disk_async(
        self,
        **params: Unpack[SDKDevboxSnapshotDiskAsyncParams],
    ) -> "AsyncSnapshot":
        snapshot_data = await self._client.devboxes.snapshot_disk_async(
            self._id,
            **params,
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
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> AsyncExecutionResult:
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = await client.devboxes.execute_async(
            devbox.id,
            **filter_params(params, DevboxExecuteAsyncParams),
            **filter_params(params, LongRequestOptions),
        )
        streaming_group = devbox._start_streaming(
            execution.execution_id,
            **filter_params(params, ExecuteStreamingCallbacks),
        )

        async def command_coro() -> DevboxAsyncExecutionDetailView:
            if execution.status == "completed":
                return execution
            return await client.devboxes.executions.await_completed(
                execution.execution_id,
                devbox_id=devbox.id,
                polling_config=params.get("polling_config"),
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

    async def exec_async(
        self,
        **params: Unpack[SDKDevboxExecuteAsyncParams],
    ) -> AsyncExecution:
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = await client.devboxes.execute_async(
            devbox.id,
            **filter_params(params, DevboxExecuteAsyncParams),
            **filter_params(params, LongRequestOptions),
        )

        streaming_group = devbox._start_streaming(
            execution.execution_id,
            **filter_params(params, ExecuteStreamingCallbacks),
        )

        return AsyncExecution(client, devbox.id, execution, streaming_group)


class _AsyncFileInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def read(
        self,
        **params: Unpack[SDKDevboxReadFileContentsParams],
    ) -> str:
        return await self._devbox._client.devboxes.read_file_contents(
            self._devbox.id,
            **params,
        )

    async def write(
        self,
        **params: Unpack[SDKDevboxWriteFileContentsParams],
    ) -> DevboxExecutionDetailView:
        contents = params.get("contents")
        if isinstance(contents, bytes):
            params = {**params, "contents": contents.decode("utf-8")}

        return await self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            **params,
        )

    async def download(
        self,
        **params: Unpack[SDKDevboxDownloadFileParams],
    ) -> bytes:
        response = await self._devbox._client.devboxes.download_file(
            self._devbox.id,
            **params,
        )
        return await response.read()

    async def upload(
        self,
        **params: Unpack[SDKDevboxUploadFileParams],
    ) -> object:
        return await self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            **params,
        )


class _AsyncNetworkInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def create_ssh_key(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxCreateSSHKeyResponse:
        return await self._devbox._client.devboxes.create_ssh_key(
            self._devbox.id,
            **options,
        )

    async def create_tunnel(
        self,
        **params: Unpack[SDKDevboxCreateTunnelParams],
    ) -> DevboxTunnelView:
        return await self._devbox._client.devboxes.create_tunnel(
            self._devbox.id,
            **params,
        )

    async def remove_tunnel(
        self,
        **params: Unpack[SDKDevboxRemoveTunnelParams],
    ) -> object:
        return await self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            **params,
        )
