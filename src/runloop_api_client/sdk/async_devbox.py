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
    """High-level async interface for managing a Runloop devbox.

    This class provides a Pythonic, awaitable API for interacting with devboxes,
    including command execution, file operations, networking, and lifecycle
    management.

    Example:
        >>> devbox = await sdk.devbox.create(name="my-devbox")
        >>> async with devbox:
        ...     result = await devbox.cmd.exec(command="echo 'hello'")
        ...     print(await result.stdout())
        # Devbox is automatically shut down on exit

    Attributes:
        id: The devbox identifier.
        cmd: Command execution interface (exec, exec_async).
        file: File operations interface (read, write, upload, download).
        net: Network operations interface (SSH keys, tunnels).
    """

    def __init__(self, client: AsyncRunloop, devbox_id: str) -> None:
        """Initialize the wrapper.

        :param client: Generated async Runloop client
        :type client: AsyncRunloop
        :param devbox_id: Devbox identifier returned by the API
        :type devbox_id: str
        """
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    @override
    def __repr__(self) -> str:
        return f"<AsyncDevbox id={self._id!r}>"

    async def __aenter__(self) -> "AsyncDevbox":
        """Enable ``async with devbox`` usage by returning ``self``.

        :return: The active devbox instance
        :rtype: AsyncDevbox
        """
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        """Ensure the devbox shuts down when leaving an async context manager."""
        try:
            await self.shutdown()
        except Exception:
            self._logger.exception("failed to shutdown async devbox %s on context exit", self._id)

    @property
    def id(self) -> str:
        """Return the devbox identifier.

        :return: Unique devbox ID
        :rtype: str
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxView:
        """Retrieve current devbox status and metadata.

        :param options: Optional request configuration
        :return: Current devbox state info
        :rtype: DevboxView
        """
        return await self._client.devboxes.retrieve(
            self._id,
            **options,
        )

    async def await_running(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach running state.

        :param polling_config: Optional polling behavior overrides, defaults to None
        :type polling_config: PollingConfig | None, optional
        :return: Devbox state info after it reaches running status
        :rtype: DevboxView
        """
        return await self._client.devboxes.await_running(self._id, polling_config=polling_config)

    async def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach suspended state.

        :param polling_config: Optional polling behavior overrides, defaults to None
        :type polling_config: PollingConfig | None, optional
        :return: Devbox state info after it reaches suspended status
        :rtype: DevboxView
        """
        return await self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    async def shutdown(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Shutdown the devbox, terminating all processes and releasing resources.

        :param options: Optional long-running request configuration
        :return: Final devbox state info
        :rtype: DevboxView
        """
        return await self._client.devboxes.shutdown(
            self._id,
            **options,
        )

    async def suspend(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Suspend the devbox without destroying state.

        Returns immediately after issuing the suspend request. Call
        :meth:`await_suspended` if you need to wait for the devbox to reach the
        ``suspended`` state (contrast with the synchronous SDK, which blocks).

        :param options: Optional long-running request configuration
        :return: Suspended devbox state info
        :rtype: DevboxView
        """
        return await self._client.devboxes.suspend(
            self._id,
            **options,
        )

    async def resume(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Resume a suspended devbox.

        Returns immediately after issuing the resume request. Call
        :meth:`await_running` if you need to wait for the devbox to reach the
        ``running`` state (contrast with the synchronous SDK, which blocks).

        :param options: Optional long-running request configuration
        :return: Resumed devbox state info
        :rtype: DevboxView
        """
        return await self._client.devboxes.resume(
            self._id,
            **options,
        )

    async def keep_alive(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        """Extend the devbox timeout, preventing automatic shutdown.

        Call this periodically for long-running workflows to prevent the devbox
        from being automatically shut down due to inactivity.

        :param options: Optional long-running request configuration
        :return: Response confirming the keep-alive request
        :rtype: object
        """
        return await self._client.devboxes.keep_alive(
            self._id,
            **options,
        )

    async def snapshot_disk(
        self,
        **params: Unpack[SDKDevboxSnapshotDiskParams],
    ) -> "AsyncSnapshot":
        """Create a disk snapshot of the devbox and wait for completion.

        Captures the current state of the devbox disk, which can be used to create
        new devboxes with the same state.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxSnapshotDiskParams` for available parameters
        :return: Wrapper representing the completed snapshot
        :rtype: AsyncSnapshot
        """
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
        """Create a disk snapshot of the devbox asynchronously.

        Starts the snapshot creation process and returns immediately without waiting
        for completion. Use snapshot.await_completed() to wait for completion.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxSnapshotDiskAsyncParams` for available parameters
        :return: Wrapper representing the snapshot request
        :rtype: AsyncSnapshot
        """
        snapshot_data = await self._client.devboxes.snapshot_disk_async(
            self._id,
            **params,
        )
        return self._snapshot_from_id(snapshot_data.id)

    async def close(self) -> None:
        """Alias for :meth:`shutdown` to support common resource patterns."""
        await self.shutdown()

    @property
    def cmd(self) -> AsyncCommandInterface:
        """Return the command execution interface.

        :return: Helper for running shell commands
        :rtype: AsyncCommandInterface
        """
        return _AsyncCommandInterface(self)

    @property
    def file(self) -> AsyncFileInterface:
        """Return the file operations interface.

        :return: Helper for reading/writing files
        :rtype: AsyncFileInterface
        """
        return _AsyncFileInterface(self)

    @property
    def net(self) -> AsyncNetworkInterface:
        """Return the networking interface.

        :return: Helper for SSH keys and tunnels
        :rtype: AsyncNetworkInterface
        """
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
    """Interface for executing commands on a devbox.

    Accessed via devbox.cmd property. Provides exec() for synchronous execution
    and exec_async() for asynchronous execution with process management.
    """

    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def exec(
        self,
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> AsyncExecutionResult:
        """Execute a command synchronously and wait for completion.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxExecuteParams` for available parameters
        :return: Wrapper with exit status and output helpers
        :rtype: AsyncExecutionResult

        Example:
            >>> result = await devbox.cmd.exec(command="echo 'hello'")
            >>> print(await result.stdout())
            >>> print(f"Exit code: {result.exit_code}")
        """
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
        """Execute a command asynchronously without waiting for completion.

        Starts command execution and returns immediately with an AsyncExecution object
        for process management. Use execution.result() to wait for completion or
        execution.kill() to terminate the process.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxExecuteAsyncParams` for available parameters
        :return: Handle for managing the running process
        :rtype: AsyncExecution

        Example:
            >>> execution = await devbox.cmd.exec_async(command="sleep 10")
            >>> state = await execution.get_state()
            >>> print(f"Status: {state.status}")
            >>> await execution.kill()  # Terminate early if needed
        """
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
    """Interface for file operations on a devbox.

    Accessed via devbox.file property. Provides coroutines for reading, writing,
    uploading, and downloading files.
    """

    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def read(
        self,
        **params: Unpack[SDKDevboxReadFileContentsParams],
    ) -> str:
        """Read a file from the devbox.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxReadFileContentsParams` for available parameters
        :return: File contents
        :rtype: str

        Example:
            >>> content = await devbox.file.read(path="/home/user/data.txt")
            >>> print(content)
        """
        return await self._devbox._client.devboxes.read_file_contents(
            self._devbox.id,
            **params,
        )

    async def write(
        self,
        **params: Unpack[SDKDevboxWriteFileContentsParams],
    ) -> DevboxExecutionDetailView:
        """Write contents to a file in the devbox.

        Creates or overwrites the file at the specified path.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxWriteFileContentsParams` for available parameters
        :return: Execution metadata for the write command
        :rtype: DevboxExecutionDetailView

        Example:
            >>> await devbox.file.write(file_path="/home/user/config.json", contents='{"key": "value"}')
        """
        return await self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            **params,
        )

    async def download(
        self,
        **params: Unpack[SDKDevboxDownloadFileParams],
    ) -> bytes:
        """Download a file from the devbox.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxDownloadFileParams` for available parameters
        :return: Raw file contents
        :rtype: bytes

        Example:
            >>> data = await devbox.file.download(path="/home/user/output.bin")
            >>> with open("local_output.bin", "wb") as f:
            ...     f.write(data)
        """
        response = await self._devbox._client.devboxes.download_file(
            self._devbox.id,
            **params,
        )
        return await response.read()

    async def upload(
        self,
        **params: Unpack[SDKDevboxUploadFileParams],
    ) -> object:
        """Upload a file to the devbox.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxUploadFileParams` for available parameters
        :return: API response confirming the upload
        :rtype: object

        Example:
            >>> from pathlib import Path
            >>> await devbox.file.upload(path="/home/user/data.csv", file=Path("local_data.csv"))
        """
        return await self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            **params,
        )


class _AsyncNetworkInterface:
    """Interface for networking operations on a devbox.

    Accessed via devbox.net property. Provides coroutines for SSH access and tunneling.
    """

    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def create_ssh_key(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxCreateSSHKeyResponse:
        """Create an SSH key for remote access to the devbox.

        :param options: Optional long-running request configuration
        :return: Response containing SSH connection info
        :rtype: DevboxCreateSSHKeyResponse

        Example:
            >>> ssh_key = await devbox.net.create_ssh_key()
            >>> print(f"SSH URL: {ssh_key.url}")
        """
        return await self._devbox._client.devboxes.create_ssh_key(
            self._devbox.id,
            **options,
        )

    async def create_tunnel(
        self,
        **params: Unpack[SDKDevboxCreateTunnelParams],
    ) -> DevboxTunnelView:
        """Create a network tunnel to expose a devbox port publicly.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateTunnelParams` for available parameters
        :return: Details about the public endpoint
        :rtype: DevboxTunnelView

        Example:
            >>> tunnel = await devbox.net.create_tunnel(port=8080)
            >>> print(f"Public URL: {tunnel.url}")
        """
        return await self._devbox._client.devboxes.create_tunnel(
            self._devbox.id,
            **params,
        )

    async def remove_tunnel(
        self,
        **params: Unpack[SDKDevboxRemoveTunnelParams],
    ) -> object:
        """Remove a network tunnel, disabling public access to the port.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxRemoveTunnelParams` for available parameters
        :return: Response confirming the tunnel removal
        :rtype: object

        Example:
            >>> await devbox.net.remove_tunnel(port=8080)
        """
        return await self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            **params,
        )
