"""Synchronous devbox resource class."""

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Any, Callable, Optional, Sequence
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
    LongPollingRequestOptions,
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
from .._client import Runloop
from ._helpers import filter_params
from .execution import Execution, _StreamingGroup
from .protocols import FileInterface, CommandInterface, NetworkInterface
from .._streaming import Stream
from ..lib.polling import PollingConfig
from .execution_result import ExecutionResult
from ..types.devbox_execute_async_params import DevboxExecuteAsyncParams
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView

if TYPE_CHECKING:
    from .snapshot import Snapshot


class Devbox:
    """High-level interface for managing a Runloop devbox.

    This class provides a Pythonic, object-oriented API for interacting with devboxes,
    including command execution, file operations, networking, and lifecycle management.

    The Devbox class supports context manager protocol for automatic cleanup:
        >>> with sdk.devbox.create(name="my-devbox") as devbox:
        ...     result = devbox.cmd.exec("echo 'hello'")
        ...     print(result.stdout())
        # Devbox is automatically shutdown on exit

    Attributes:
        id: The devbox identifier.
        cmd: Command execution interface (exec, exec_async).
        file: File operations interface (read, write, upload, download).
        net: Network operations interface (SSH keys, tunnels).
    """

    def __init__(self, client: Runloop, devbox_id: str) -> None:
        """Initialize the wrapper.

        Args:
            client: Generated Runloop client.
            devbox_id: Devbox identifier returned by the API.
        """
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    @override
    def __repr__(self) -> str:
        return f"<Devbox id={self._id!r}>"

    def __enter__(self) -> "Devbox":
        """Enable ``with devbox`` usage by returning ``self``.

        Returns:
            Devbox: The active devbox instance.
        """
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        """Shutdown the devbox when leaving a context manager."""
        try:
            self.shutdown()
        except Exception:
            self._logger.exception("failed to shutdown devbox %s on context exit", self._id)

    @property
    def id(self) -> str:
        """Return the devbox identifier.

        Returns:
            str: Unique devbox ID.
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxView:
        """Retrieve current devbox status and metadata.

        Args:
            **options: Optional request configuration.

        Returns:
            DevboxView: Current devbox state info.
        """
        return self._client.devboxes.retrieve(
            self._id,
            **options,
        )

    def await_running(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach running state.

        Blocks until the devbox is running or the polling timeout is reached.

        Args:
            polling_config: Optional configuration for polling behavior (timeout, interval).

        Returns:
            DevboxView: Devbox state info after it reaches running status.
        """
        return self._client.devboxes.await_running(self._id, polling_config=polling_config)

    def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach suspended state.

        Blocks until the devbox is suspended or the polling timeout is reached.

        Args:
            polling_config: Optional configuration for polling behavior (timeout, interval).

        Returns:
            DevboxView: Devbox state info after it reaches suspended status.
        """
        return self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    def shutdown(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Shutdown the devbox, terminating all processes and releasing resources.

        Args:
            **options: Long-running request configuration (timeouts, retries, etc.).

        Returns:
            DevboxView: Final devbox state info.
        """
        return self._client.devboxes.shutdown(
            self._id,
            **options,
        )

    def suspend(
        self,
        **options: Unpack[LongPollingRequestOptions],
    ) -> DevboxView:
        """Suspend the devbox, pausing execution while preserving state.

        This saves resources while maintaining the devbox state for later resumption.
        Waits for the devbox to reach suspended state before returning.

        Args:
            **options: Optional long-running request and polling configuration.

        Returns:
            DevboxView: Suspended devbox state info.
        """
        self._client.devboxes.suspend(
            self._id,
            **filter_params(options, LongRequestOptions),
        )
        return self._client.devboxes.await_suspended(self._id, polling_config=options.get("polling_config"))

    def resume(
        self,
        **options: Unpack[LongPollingRequestOptions],
    ) -> DevboxView:
        """Resume a suspended devbox, restoring it to running state.

        Waits for the devbox to reach running state before returning.

        Args:
            **options: Optional long-running request and polling configuration.

        Returns:
            DevboxView: Resumed devbox state info.
        """
        self._client.devboxes.resume(
            self._id,
            **filter_params(options, LongRequestOptions),
        )
        return self._client.devboxes.await_running(self._id, polling_config=options.get("polling_config"))

    def keep_alive(
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
        return self._client.devboxes.keep_alive(
            self._id,
            **options,
        )

    def snapshot_disk(
        self,
        **params: Unpack[SDKDevboxSnapshotDiskParams],
    ) -> "Snapshot":
        """Create a disk snapshot of the devbox and wait for completion.

        Captures the current state of the devbox disk, which can be used to create
        new devboxes with the same state.

        Args:
            **params: Snapshot metadata, naming, and polling configuration.

        Returns:
            Snapshot: Wrapper representing the completed snapshot.
        """
        snapshot_data = self._client.devboxes.snapshot_disk_async(
            self._id,
            **filter_params(params, SDKDevboxSnapshotDiskAsyncParams),
        )
        snapshot = self._snapshot_from_id(snapshot_data.id)
        snapshot.await_completed(**filter_params(params, PollingRequestOptions))
        return snapshot

    def snapshot_disk_async(
        self,
        **params: Unpack[SDKDevboxSnapshotDiskAsyncParams],
    ) -> "Snapshot":
        """Create a disk snapshot of the devbox asynchronously.

        Starts the snapshot creation process and returns immediately without waiting
        for completion. Use snapshot.await_completed() to wait for completion.

        Args:
            **params: Snapshot metadata and naming options.

        Returns:
            Snapshot: Wrapper representing the snapshot (may still be processing).
        """
        snapshot_data = self._client.devboxes.snapshot_disk_async(
            self._id,
            **params,
        )
        return self._snapshot_from_id(snapshot_data.id)

    def close(self) -> None:
        """Alias for :meth:`shutdown` to support common resource patterns."""
        self.shutdown()

    @property
    def cmd(self) -> CommandInterface:
        """Return the command execution interface.

        Returns:
            CommandInterface: Helper for running shell commands.
        """
        return _CommandInterface(self)

    @property
    def file(self) -> FileInterface:
        """Return the file operations interface.

        Returns:
            FileInterface: Helper for reading/writing files.
        """
        return _FileInterface(self)

    @property
    def net(self) -> NetworkInterface:
        """Return the networking interface.

        Returns:
            NetworkInterface: Helper for SSH keys and tunnels.
        """
        return _NetworkInterface(self)

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _snapshot_from_id(self, snapshot_id: str) -> "Snapshot":
        from .snapshot import Snapshot

        return Snapshot(self._client, snapshot_id)

    def _start_streaming(
        self,
        execution_id: str,
        *,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
    ) -> Optional[_StreamingGroup]:
        """Set up background threads to stream command output to callbacks.

        Creates separate threads for stdout and stderr streams, allowing real-time
        processing of command output through user-provided callbacks.
        """
        threads: list[threading.Thread] = []
        stop_event = threading.Event()

        # Set up stdout streaming if stdout or output callbacks are provided
        if stdout or output:
            callbacks = [cb for cb in (stdout, output) if cb is not None]
            threads.append(
                self._spawn_stream_thread(
                    name="stdout",
                    stream_factory=lambda: self._client.devboxes.executions.stream_stdout_updates(
                        execution_id,
                        devbox_id=self._id,
                    ),
                    callbacks=callbacks,
                    stop_event=stop_event,
                )
            )

        # Set up stderr streaming if stderr or output callbacks are provided
        if stderr or output:
            callbacks = [cb for cb in (stderr, output) if cb is not None]
            threads.append(
                self._spawn_stream_thread(
                    name="stderr",
                    stream_factory=lambda: self._client.devboxes.executions.stream_stderr_updates(
                        execution_id,
                        devbox_id=self._id,
                    ),
                    callbacks=callbacks,
                    stop_event=stop_event,
                )
            )

        if not threads:
            return None

        return _StreamingGroup(threads, stop_event)

    def _spawn_stream_thread(
        self,
        *,
        name: str,
        stream_factory: Callable[[], Stream[ExecutionUpdateChunk]],
        callbacks: Sequence[LogCallback],
        stop_event: threading.Event,
    ) -> threading.Thread:
        logger = self._logger

        def worker() -> None:
            try:
                with stream_factory() as stream:
                    for chunk in stream:
                        if stop_event.is_set():
                            break
                        text = chunk.output
                        for callback in callbacks:
                            try:
                                callback(text)
                            except Exception:
                                logger.exception("error in %s callback for devbox %s", name, self._id)
            except Exception:
                logger.exception("error streaming %s logs for devbox %s", name, self._id)

        thread = threading.Thread(
            target=worker,
            name=f"runloop-devbox-{self._id}-{name}",
            daemon=True,
        )
        thread.start()
        return thread


class _CommandInterface:
    """Interface for executing commands on a devbox.

    Accessed via devbox.cmd property. Provides exec() for synchronous execution
    and exec_async() for asynchronous execution with process management.
    """

    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def exec(
        self,
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> ExecutionResult:
        """Execute a command synchronously and wait for completion.

        Args:
            **params: Command parameters, streaming callbacks, and polling config.

        Returns:
            ExecutionResult: Wrapper with exit status and output helpers.

        Example:
            >>> result = devbox.cmd.exec(command="ls -la")
            >>> print(result.stdout())
            >>> print(f"Exit code: {result.exit_code}")
        """
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = client.devboxes.execute_async(
            devbox.id,
            **filter_params(params, DevboxExecuteAsyncParams),
            **filter_params(params, LongRequestOptions),
        )
        streaming_group = devbox._start_streaming(
            execution.execution_id,
            **filter_params(params, ExecuteStreamingCallbacks),
        )
        final = execution
        if execution.status == "completed":
            final: DevboxAsyncExecutionDetailView = execution
        else:
            final = client.devboxes.executions.await_completed(
                execution.execution_id,
                devbox_id=devbox.id,
                polling_config=params.get("polling_config"),
            )

        if streaming_group is not None:
            # Ensure log streaming has completed before returning the result.
            streaming_group.join()

        return ExecutionResult(client, devbox.id, final)

    def exec_async(
        self,
        **params: Unpack[SDKDevboxExecuteAsyncParams],
    ) -> Execution:
        """Execute a command asynchronously without waiting for completion.

        Starts command execution and returns immediately with an Execution object
        for process management. Use execution.result() to wait for completion or
        execution.kill() to terminate the process.

        Args:
            **params: Command parameters and streaming callbacks.
        Returns:
            Execution: Handle for managing the running process.

        Example:
            >>> execution = devbox.cmd.exec_async(command="sleep 10")
            >>> state = execution.get_state()
            >>> print(f"Status: {state.status}")
            >>> execution.kill()  # Terminate early if needed
        """
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = client.devboxes.execute_async(
            devbox.id,
            **filter_params(params, DevboxExecuteAsyncParams),
            **filter_params(params, LongRequestOptions),
        )

        streaming_group = devbox._start_streaming(
            execution.execution_id,
            **filter_params(params, ExecuteStreamingCallbacks),
        )

        return Execution(client, devbox.id, execution, streaming_group)


class _FileInterface:
    """Interface for file operations on a devbox.

    Accessed via devbox.file property. Provides methods for reading, writing,
    uploading, and downloading files.
    """

    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def read(
        self,
        **params: Unpack[SDKDevboxReadFileContentsParams],
    ) -> str:
        """Read a file from the devbox.

        Args:
            **params: Parameters such as ``path``.

        Returns:
            str: File contents.

        Example:
            >>> content = devbox.file.read("/home/user/data.txt")
            >>> print(content)
        """
        return self._devbox._client.devboxes.read_file_contents(
            self._devbox.id,
            **params,
        )

    def write(
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
            >>> devbox.file.write(file_path="/home/user/config.json", contents='{"key": "value"}')
        """
        return self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            **params,
        )

    def download(
        self,
        **params: Unpack[SDKDevboxDownloadFileParams],
    ) -> bytes:
        """Download a file from the devbox.

        Args:
            **params: Parameters such as ``path``.

        Returns:
            bytes: Raw file contents.

        Example:
            >>> data = devbox.file.download("/home/user/output.bin")
            >>> with open("local_output.bin", "wb") as f:
            ...     f.write(data)
        """
        response = self._devbox._client.devboxes.download_file(
            self._devbox.id,
            **params,
        )
        return response.read()

    def upload(
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
            >>> devbox.file.upload("/home/user/data.csv", Path("local_data.csv"))
        """
        return self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            **params,
        )


class _NetworkInterface:
    """Interface for network operations on a devbox.

    Accessed via devbox.net property. Provides methods for SSH access and tunneling.
    """

    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def create_ssh_key(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxCreateSSHKeyResponse:
        """Create an SSH key for remote access to the devbox.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            DevboxCreateSSHKeyResponse: Response containing SSH connection info.

        Example:
            >>> ssh_key = devbox.net.create_ssh_key()
            >>> print(f"SSH URL: {ssh_key.url}")
        """
        return self._devbox._client.devboxes.create_ssh_key(
            self._devbox.id,
            **options,
        )

    def create_tunnel(
        self,
        **params: Unpack[SDKDevboxCreateTunnelParams],
    ) -> DevboxTunnelView:
        """Create a network tunnel to expose a devbox port publicly.

        Args:
            **params: Parameters such as the devbox ``port`` to expose.

        Returns:
            DevboxTunnelView: Details about the public endpoint.

        Example:
            >>> tunnel = devbox.net.create_tunnel(port=8080)
            >>> print(f"Public URL: {tunnel.url}")
        """
        return self._devbox._client.devboxes.create_tunnel(
            self._devbox.id,
            **params,
        )

    def remove_tunnel(
        self,
        **params: Unpack[SDKDevboxRemoveTunnelParams],
    ) -> object:
        """Remove a network tunnel, disabling public access to the port.

        Args:
            **params: Parameters such as the ``port`` to close.

        Returns:
            object: Response confirming the tunnel removal.

        Example:
            >>> devbox.net.remove_tunnel(port=8080)
        """
        return self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            **params,
        )
