"""Public protocol interfaces for SDK components.

This module defines Protocol interfaces that provide clean type hints for SDK
interface classes without exposing private implementation details in documentation.
"""

from __future__ import annotations

from typing import Protocol
from typing_extensions import Unpack, runtime_checkable

from ..types import DevboxTunnelView, DevboxExecutionDetailView, DevboxCreateSSHKeyResponse
from ._types import (
    LongRequestOptions,
    SDKDevboxExecuteParams,
    SDKDevboxUploadFileParams,
    SDKDevboxCreateTunnelParams,
    SDKDevboxDownloadFileParams,
    SDKDevboxExecuteAsyncParams,
    SDKDevboxRemoveTunnelParams,
    SDKDevboxReadFileContentsParams,
    SDKDevboxWriteFileContentsParams,
)
from .execution import Execution
from .async_execution import AsyncExecution
from .execution_result import ExecutionResult
from .async_execution_result import AsyncExecutionResult

# ==============================================================================
# Synchronous Interfaces
# ==============================================================================


@runtime_checkable
class CommandInterface(Protocol):
    """Interface for executing commands on a devbox.

    Accessed via `devbox.cmd` property. Provides `exec()` for synchronous execution
    and `exec_async()` for asynchronous process management.

    Important: All streaming callbacks (stdout, stderr, output) must be synchronous
    functions, not async functions.
    """

    def exec(
        self,
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> "ExecutionResult": ...

    def exec_async(
        self,
        **params: Unpack[SDKDevboxExecuteAsyncParams],
    ) -> "Execution": ...


@runtime_checkable
class FileInterface(Protocol):
    """Interface for file operations on a devbox.

    Accessed via `devbox.file` property. Provides methods for reading, writing,
    uploading, and downloading files.
    """

    def read(
        self,
        **params: Unpack[SDKDevboxReadFileContentsParams],
    ) -> str: ...

    def write(
        self,
        **params: Unpack[SDKDevboxWriteFileContentsParams],
    ) -> DevboxExecutionDetailView: ...

    def download(
        self,
        **params: Unpack[SDKDevboxDownloadFileParams],
    ) -> bytes: ...

    def upload(
        self,
        **params: Unpack[SDKDevboxUploadFileParams],
    ) -> object: ...


@runtime_checkable
class NetworkInterface(Protocol):
    """Interface for network operations on a devbox.

    Accessed via `devbox.net` property. Provides methods for managing SSH keys
    and network tunnels.
    """

    def create_ssh_key(
        self,
        **params: Unpack[LongRequestOptions],
    ) -> DevboxCreateSSHKeyResponse: ...

    def create_tunnel(
        self,
        **params: Unpack[SDKDevboxCreateTunnelParams],
    ) -> DevboxTunnelView: ...

    def remove_tunnel(
        self,
        **params: Unpack[SDKDevboxRemoveTunnelParams],
    ) -> object: ...


# ==============================================================================
# Asynchronous Interfaces
# ==============================================================================


@runtime_checkable
class AsyncCommandInterface(Protocol):
    """Async interface for executing commands on a devbox.

    Accessed via `devbox.cmd` property. Provides `exec()` and `exec_async()` for
    command execution with async/await support.

    Important: All streaming callbacks (stdout, stderr, output) must be synchronous
    functions, not async functions. The devbox operations are async, but the callbacks
    themselves are called synchronously.

    Examples:
        >>> # Async execution (waits for completion)
        >>> result = await devbox.cmd.exec(command="ls -la")
        >>> print(await result.stdout())

        >>> # Async non-blocking execution
        >>> execution = await devbox.cmd.exec_async(command="npm run dev")
        >>> result = await execution.result()  # Waits for completion

        >>> # Callbacks must still be synchronous!
        >>> def stdout_callback(line: str) -> None:  # Not async!
        ...     print(f">> {line}")
        >>> await devbox.cmd.exec(command="tail -f /var/log/app.log", stdout=stdout_callback)
    """

    async def exec(
        self,
        **params: Unpack[SDKDevboxExecuteParams],
    ) -> "AsyncExecutionResult": ...

    async def exec_async(
        self,
        **params: Unpack[SDKDevboxExecuteAsyncParams],
    ) -> "AsyncExecution": ...


@runtime_checkable
class AsyncFileInterface(Protocol):
    """Async interface for file operations on a devbox.

    Accessed via `devbox.file` property. Provides async methods for reading, writing,
    uploading, and downloading files.
    """

    async def read(
        self,
        **params: Unpack[SDKDevboxReadFileContentsParams],
    ) -> str: ...

    async def write(
        self,
        **params: Unpack[SDKDevboxWriteFileContentsParams],
    ) -> DevboxExecutionDetailView: ...

    async def download(
        self,
        **params: Unpack[SDKDevboxDownloadFileParams],
    ) -> bytes: ...

    async def upload(
        self,
        **params: Unpack[SDKDevboxUploadFileParams],
    ) -> object: ...


@runtime_checkable
class AsyncNetworkInterface(Protocol):
    """Async interface for network operations on a devbox.

    Accessed via `devbox.net` property. Provides async methods for managing SSH keys
    and network tunnels.
    """

    async def create_ssh_key(
        self,
        **params: Unpack[LongRequestOptions],
    ) -> DevboxCreateSSHKeyResponse: ...

    async def create_tunnel(
        self,
        **params: Unpack[SDKDevboxCreateTunnelParams],
    ) -> DevboxTunnelView: ...

    async def remove_tunnel(
        self,
        **params: Unpack[SDKDevboxRemoveTunnelParams],
    ) -> object: ...
