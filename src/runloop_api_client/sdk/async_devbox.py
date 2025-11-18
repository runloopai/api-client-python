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

        Args:
            client: Generated async Runloop client.
            devbox_id: Devbox identifier returned by the API.
        """
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    @override
    def __repr__(self) -> str:
        return f"<AsyncDevbox id={self._id!r}>"

    async def __aenter__(self) -> "AsyncDevbox":
        """Enable ``async with devbox`` usage by returning ``self``.

        Returns:
            AsyncDevbox: The active devbox instance.
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

        Returns:
            str: Unique devbox ID.
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxView:
        """Retrieve current devbox status and metadata.

        Args:
            **options: Optional request configuration.

        Returns:
            DevboxView: Current devbox state info.
        """
        return await self._client.devboxes.retrieve(
            self._id,
            **options,
        )

    async def await_running(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach running state.

        Args:
            polling_config: Optional polling behavior overrides.

        Returns:
            DevboxView: Devbox state info after it reaches running status.
        """
        return await self._client.devboxes.await_running(self._id, polling_config=polling_config)

    async def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach suspended state.

        Args:
            polling_config: Optional polling behavior overrides.

        Returns:
            DevboxView: Devbox state info after it reaches suspended status.
        """
        return await self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    async def shutdown(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Shutdown the devbox, terminating all processes and releasing resources.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            DevboxView: Final devbox state info.
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

        Args:
            **options: Optional long-running request configuration.

        Returns:
            DevboxView: Suspended devbox state info.
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

        Args:
            **options: Optional long-running request configuration.

        Returns:
            DevboxView: Resumed devbox state info.
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

        Args:
            **options: Optional long-running request configuration.

        Returns:
            object: Response confirming the keep-alive request.
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

        Args:
            **params: Snapshot metadata, naming, and polling configuration.

        Returns:
            AsyncSnapshot: Wrapper representing the completed snapshot.
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

        Args:
            **params: Snapshot metadata and naming options.

        Returns:
            AsyncSnapshot: Wrapper representing the snapshot request.
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

        Returns:
            AsyncCommandInterface: Helper for running shell commands.
        """
        return _AsyncCommandInterface(self)

    @property
    def file(self) -> AsyncFileInterface:
        """Return the file operations interface.

        Returns:
            AsyncFileInterface: Helper for reading/writing files.
        """
        return _AsyncFileInterface(self)

    @property
    def net(self) -> AsyncNetworkInterface:
        """Return the networking interface.

        Returns:
            AsyncNetworkInterface: Helper for SSH keys and tunnels.
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

        Args:
            **params: Command parameters, streaming callbacks, and polling config.

        Returns:
            AsyncExecutionResult: Wrapper with exit status and output helpers.

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

        Args:
            **params: Command parameters and streaming callbacks.

        Returns:
            AsyncExecution: Handle for managing the running process.

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

        Args:
            **params: Parameters such as ``path``.

        Returns:
            str: File contents.

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

        Args:
            **params: Parameters such as ``file_path`` and ``contents``.

        Returns:
            DevboxExecutionDetailView: Execution metadata for the write command.

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

        Args:
            **params: Parameters such as ``path``.

        Returns:
            bytes: Raw file contents.

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

        Args:
            **params: Parameters such as destination ``path`` and local ``file``.

        Returns:
            object: API response confirming the upload.

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

        Args:
            **options: Optional long-running request configuration.

        Returns:
            DevboxCreateSSHKeyResponse: Response containing SSH connection info.

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

        Args:
            **params: Parameters such as the devbox ``port`` to expose.

        Returns:
            DevboxTunnelView: Details about the public endpoint.

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

        Args:
            **params: Parameters such as the ``port`` to close.

        Returns:
            object: Response confirming the tunnel removal.

        Example:
            >>> await devbox.net.remove_tunnel(port=8080)
        """
        return await self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            **params,
        )
