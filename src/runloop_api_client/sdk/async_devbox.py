"""Asynchronous devbox resource class."""

from __future__ import annotations

import asyncio
import logging
import warnings
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
    BaseRequestOptions,
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
from .._streaming import AsyncStream
from ..lib.polling import PollingConfig
from ..types.devboxes import ExecutionUpdateChunk
from .async_execution import AsyncExecution, _AsyncStreamingGroup
from .async_execution_result import AsyncExecutionResult
from ..types.devbox_execute_async_params import DevboxNiceExecuteAsyncParams
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
        >>> devbox = await runloop.devbox.create(name="my-devbox")
        >>> async with devbox:
        ...     result = await devbox.cmd.exec("echo 'hello'")
        ...     print(await result.stdout())
        # Devbox is automatically shut down on exit
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
        **options: Unpack[BaseRequestOptions],
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
        *,
        polling_config: PollingConfig | None = None,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Resume a suspended devbox, restoring it to running state.

        Waits for the devbox to reach running state before returning.

        :param polling_config: Optional polling behavior overrides, defaults to None
        :type polling_config: PollingConfig | None, optional
        :param options: Optional long-running request configuration
        :return: Resumed devbox state info
        :rtype: DevboxView
        """
        await self.resume_async(**options)
        return await self.await_running(polling_config=polling_config)

    async def resume_async(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Resume a suspended devbox without waiting for it to reach running state.

        Initiates the resume operation and returns immediately. Use :meth:`await_running`
        to wait for the devbox to reach running state if needed.

        :param options: Optional long-running request configuration
        :return: Devbox state info immediately after resume request
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
        return AsyncCommandInterface(self)

    @property
    def file(self) -> AsyncFileInterface:
        """Return the file operations interface.

        :return: Helper for reading/writing files
        :rtype: AsyncFileInterface
        """
        return AsyncFileInterface(self)

    @property
    def net(self) -> AsyncNetworkInterface:
        """Return the networking interface.

        :return: Helper for SSH keys and tunnels
        :rtype: AsyncNetworkInterface
        """
        return AsyncNetworkInterface(self)

    def shell(self, shell_name: str | None = None) -> AsyncNamedShell:
        """Create a named shell instance for stateful command execution.

        Named shells are stateful and maintain environment variables and the current working
        directory (CWD) across commands, just like a real shell on your local computer.
        Commands executed through the same named shell instance will execute sequentially -
        the shell can only run one command at a time with automatic queuing. This ensures
        that environment changes and directory changes from one command are preserved for
        the next command.

        :param shell_name: The name of the persistent shell session. If not provided, a UUID will be generated automatically.
        :type shell_name: str | None, optional
        :return: An AsyncNamedShell instance for executing commands in the named shell
        :rtype: AsyncNamedShell

        Example:
            >>> # Create a named shell with a custom name
            >>> shell = await devbox.shell("my-session")
            >>> # Create a named shell with an auto-generated UUID name
            >>> shell2 = await devbox.shell()
            >>> # Commands execute sequentially and share state
            >>> await shell.exec("cd /app")
            >>> await shell.exec("export MY_VAR=value")
            >>> result = await shell.exec("echo $MY_VAR")  # Will output 'value'
            >>> result = await shell.exec("pwd")  # Will output '/app'
        """
        if shell_name is None:
            # uuid_utils is not typed
            from uuid_utils import uuid7  # type: ignore

            shell_name = str(uuid7())
        return AsyncNamedShell(self, shell_name)

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


class AsyncCommandInterface:
    """Interface for executing commands on a devbox.

    Accessed via devbox.cmd property. Provides exec() for synchronous execution
    and exec_async() for asynchronous execution with process management.
    """

    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def exec(
        self,
        command: str,
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> AsyncExecutionResult:
        """Execute a command synchronously and wait for completion.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxExecuteParams` for available parameters
        :return: Wrapper with exit status and output helpers
        :rtype: AsyncExecutionResult

        Example:
            >>> result = await devbox.cmd.exec("echo 'hello'")
            >>> print(await result.stdout())
            >>> print(f"Exit code: {result.exit_code}")
        """
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = await client.devboxes.execute_async(
            devbox.id,
            command=command,
            **filter_params(params, DevboxNiceExecuteAsyncParams),
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
        command: str,
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
            >>> execution = await devbox.cmd.exec_async("sleep 10")
            >>> state = await execution.get_state()
            >>> print(f"Status: {state.status}")
            >>> await execution.kill()  # Terminate early if needed
        """
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = await client.devboxes.execute_async(
            devbox.id,
            command=command,
            **filter_params(params, DevboxNiceExecuteAsyncParams),
            **filter_params(params, LongRequestOptions),
        )

        streaming_group = devbox._start_streaming(
            execution.execution_id,
            **filter_params(params, ExecuteStreamingCallbacks),
        )

        return AsyncExecution(client, devbox.id, execution, streaming_group)


class AsyncFileInterface:
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


class AsyncNamedShell:
    """Interface for executing commands in a persistent, stateful shell session.

    Named shells are stateful and maintain environment variables and the current working
    directory (CWD) across commands. Commands executed through the same named shell
    instance will execute sequentially - the shell can only run one command at a time
    with automatic queuing. This ensures that environment changes and directory changes
    from one command are preserved for the next command.

    Use :meth:`AsyncDevbox.shell` to create a named shell instance. If you use the same
    shell name, it will re-attach to the existing named shell, preserving its state.

    Example:
        >>> shell = await devbox.shell("my-session")
        >>> await shell.exec("cd /app")
        >>> await shell.exec("export MY_VAR=value")
        >>> result = await shell.exec("echo $MY_VAR")  # Will output 'value'
        >>> result = await shell.exec("pwd")  # Will output '/app'
    """

    def __init__(self, devbox: AsyncDevbox, shell_name: str) -> None:
        """Initialize the named shell.

        :param devbox: The async devbox instance to execute commands on
        :type devbox: AsyncDevbox
        :param shell_name: The name of the persistent shell session
        :type shell_name: str
        """
        self._devbox = devbox
        self._shell_name = shell_name

    async def exec(
        self,
        command: str,
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> AsyncExecutionResult:
        """Execute a command in the named shell and wait for it to complete.

        The command will execute in the persistent shell session, maintaining environment
        variables and the current working directory from previous commands. Commands are
        queued and execute sequentially - only one command runs at a time in the named shell.

        Optionally provide callbacks to stream logs in real-time. When callbacks are provided,
        this method waits for both the command to complete AND all streaming data to be
        processed before returning.

        :param command: The command to execute
        :type command: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxExecuteParams` for available parameters
        :return: Wrapper with exit status and output helpers
        :rtype: AsyncExecutionResult

        Example:
            >>> shell = await devbox.shell("my-session")
            >>> result = await shell.exec("ls -la")
            >>> print(await result.stdout())
            >>> # With streaming callbacks
            >>> result = await shell.exec("npm install", stdout=lambda line: print(f"[LOG] {line}"))
        """
        # Ensure shell_name is set and cannot be overridden by user params
        params["shell_name"] = self._shell_name
        return await self._devbox.cmd.exec(command, **params)

    async def exec_async(
        self,
        command: str,
        **params: Unpack[SDKDevboxExecuteAsyncParams],
    ) -> AsyncExecution:
        """Execute a command in the named shell asynchronously without waiting for completion.

        The command will execute in the persistent shell session, maintaining environment
        variables and the current working directory from previous commands. Commands are
        queued and execute sequentially - only one command runs at a time in the named shell.

        Optionally provide callbacks to stream logs in real-time as they are produced.
        Callbacks fire in real-time as logs arrive. When you call execution.result(),
        it will wait for both the command to complete and all streaming to finish.

        :param command: The command to execute
        :type command: str
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxExecuteAsyncParams` for available parameters
        :return: Handle for managing the running process
        :rtype: AsyncExecution

        Example:
            >>> shell = await devbox.shell("my-session")
            >>> execution = await shell.exec_async("long-running-task.sh", stdout=lambda line: print(f"[LOG] {line}"))
            >>> # Do other work while command runs...
            >>> result = await execution.result()
            >>> if result.success:
            ...     print("Task completed successfully!")
        """
        # Ensure shell_name is set and cannot be overridden by user params
        params["shell_name"] = self._shell_name
        return await self._devbox.cmd.exec_async(command, **params)


class AsyncNetworkInterface:
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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return await self._devbox._client.devboxes.create_tunnel(  # type: ignore[deprecated]
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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return await self._devbox._client.devboxes.remove_tunnel(  # type: ignore[deprecated]
                self._devbox.id,
                **params,
            )
