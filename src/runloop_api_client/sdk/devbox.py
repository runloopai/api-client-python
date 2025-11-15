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
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    @override
    def __repr__(self) -> str:
        return f"<Devbox id={self._id!r}>"

    def __enter__(self) -> "Devbox":
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        try:
            self.shutdown()
        except Exception:
            self._logger.exception("failed to shutdown devbox %s on context exit", self._id)

    @property
    def id(self) -> str:
        return self._id

    def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxView:
        """Retrieve current devbox status and metadata.

        Returns:
            DevboxView containing the devbox's current state, status, and metadata.
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
            DevboxView with the devbox in running state.
        """
        return self._client.devboxes.await_running(self._id, polling_config=polling_config)

    def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        """Wait for the devbox to reach suspended state.

        Blocks until the devbox is suspended or the polling timeout is reached.

        Args:
            polling_config: Optional configuration for polling behavior (timeout, interval).

        Returns:
            DevboxView with the devbox in suspended state.
        """
        return self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    def shutdown(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> DevboxView:
        """Shutdown the devbox, terminating all processes and releasing resources.

        Returns:
            DevboxView with the final devbox state.
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
            polling_config: Optional configuration for polling behavior (timeout, interval).

        Returns:
            DevboxView with the devbox in suspended state.
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
            polling_config: Optional configuration for polling behavior (timeout, interval).

        Returns:
            DevboxView with the devbox in running state.
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

        Returns:
            Response object confirming the keep-alive request.
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
            commit_message: Optional message describing the snapshot.
            metadata: Optional key-value metadata to attach to the snapshot.
            name: Optional name for the snapshot.
            polling_config: Optional configuration for polling behavior (timeout, interval).

        Returns:
            Snapshot object representing the completed snapshot.
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
            commit_message: Optional message describing the snapshot.
            metadata: Optional key-value metadata to attach to the snapshot.
            name: Optional name for the snapshot.

        Returns:
            Snapshot object (snapshot may still be in progress).
        """
        snapshot_data = self._client.devboxes.snapshot_disk_async(
            self._id,
            **params,
        )
        return self._snapshot_from_id(snapshot_data.id)

    def close(self) -> None:
        self.shutdown()

    @property
    def cmd(self) -> CommandInterface:
        return _CommandInterface(self)

    @property
    def file(self) -> FileInterface:
        return _FileInterface(self)

    @property
    def net(self) -> NetworkInterface:
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
            command: The shell command to execute.
            shell_name: Optional shell to use (e.g., "bash", "sh").
            stdout: Optional callback to receive stdout lines in real-time.
            stderr: Optional callback to receive stderr lines in real-time.
            output: Optional callback to receive combined output lines in real-time.
            polling_config: Optional configuration for polling behavior.
            attach_stdin: Whether to attach stdin for interactive commands.

        Returns:
            ExecutionResult with exit code and captured output.

        Example:
            >>> result = devbox.cmd.exec("ls -la")
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
            # Ensure log streaming has drained before returning the result. _stop_streaming()
            # below will perform the final cleanup, but we still join here so callers only
            # resume once all logs have been delivered.
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
            command: The shell command to execute.
            shell_name: Optional shell to use (e.g., "bash", "sh").
            stdout: Optional callback to receive stdout lines in real-time.
            stderr: Optional callback to receive stderr lines in real-time.
            output: Optional callback to receive combined output lines in real-time.
            attach_stdin: Whether to attach stdin for interactive commands.

        Returns:
            Execution object for managing the running process.

        Example:
            >>> execution = devbox.cmd.exec_async("sleep 10")
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
            path: Absolute path to the file in the devbox.

        Returns:
            File contents as a string.

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
            file_path: Absolute path to the file in the devbox.
            contents: File contents as string.

        Returns:
            Execution details for the write operation.

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
            path: Absolute path to the file in the devbox.

        Returns:
            File contents as bytes.

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
            path: Destination path in the devbox.
            file: File to upload (Path-like object or bytes).

        Returns:
            Response object confirming the upload.

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

        Returns:
            SSH key response containing the SSH URL and credentials.

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
            port: The port number in the devbox to expose.

        Returns:
            DevboxTunnelView containing the public URL for the tunnel.

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
            port: The port number of the tunnel to remove.

        Returns:
            Response object confirming the tunnel removal.

        Example:
            >>> devbox.net.remove_tunnel(port=8080)
        """
        return self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            **params,
        )
