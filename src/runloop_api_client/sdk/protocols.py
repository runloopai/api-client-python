"""Public protocol interfaces for SDK components.

This module defines Protocol interfaces that provide clean type hints for SDK
interface classes without exposing private implementation details in documentation.
"""

from __future__ import annotations

from typing import Callable, Optional, Protocol
from typing_extensions import runtime_checkable

from ..types import DevboxTunnelView, DevboxExecutionDetailView, DevboxCreateSSHKeyResponse
from .._types import Body, Omit, Query, Headers, Timeout, NotGiven, FileTypes
from .execution import Execution
from ..lib.polling import PollingConfig
from .async_execution import AsyncExecution
from .execution_result import ExecutionResult
from .async_execution_result import AsyncExecutionResult


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
        command: str,
        *,
        shell_name: Optional[str] | Omit = ...,
        stdout: Optional[Callable[[str], None]] = None,
        stderr: Optional[Callable[[str], None]] = None,
        output: Optional[Callable[[str], None]] = None,
        polling_config: PollingConfig | None = None,
        attach_stdin: bool | Omit = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> "ExecutionResult": ...

    def exec_async(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = ...,
        stdout: Optional[Callable[[str], None]] = None,
        stderr: Optional[Callable[[str], None]] = None,
        output: Optional[Callable[[str], None]] = None,
        attach_stdin: bool | Omit = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> "Execution": ...


@runtime_checkable
class FileInterface(Protocol):
    """Interface for file operations on a devbox.

    Accessed via `devbox.file` property. Provides methods for reading, writing,
    uploading, and downloading files.
    """

    def read(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> str: ...

    def write(
        self,
        path: str,
        contents: str | bytes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView: ...

    def download(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> bytes: ...

    def upload(
        self,
        path: str,
        file: FileTypes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> object: ...


@runtime_checkable
class NetworkInterface(Protocol):
    """Interface for network operations on a devbox.

    Accessed via `devbox.net` property. Provides methods for managing SSH keys
    and network tunnels.
    """

    def create_ssh_key(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> DevboxCreateSSHKeyResponse: ...

    def create_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> DevboxTunnelView: ...

    def remove_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> object: ...


@runtime_checkable
class AsyncCommandInterface(Protocol):
    """Async interface for executing commands on a devbox.

    Accessed via `devbox.cmd` property. Provides `exec()` and `exec_async()` for
    command execution with async/await support.

    Important: All streaming callbacks (stdout, stderr, output) must be synchronous
    functions, not async functions. The devbox operations are async, but the callbacks
    themselves are called synchronously.
    """

    async def exec(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = ...,
        stdout: Optional[Callable[[str], None]] = None,
        stderr: Optional[Callable[[str], None]] = None,
        output: Optional[Callable[[str], None]] = None,
        polling_config: PollingConfig | None = None,
        attach_stdin: bool | Omit = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> "AsyncExecutionResult": ...

    async def exec_async(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = ...,
        stdout: Optional[Callable[[str], None]] = None,
        stderr: Optional[Callable[[str], None]] = None,
        output: Optional[Callable[[str], None]] = None,
        attach_stdin: bool | Omit = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> "AsyncExecution": ...


@runtime_checkable
class AsyncFileInterface(Protocol):
    """Async interface for file operations on a devbox.

    Accessed via `devbox.file` property. Provides async methods for reading, writing,
    uploading, and downloading files.
    """

    async def read(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> str: ...

    async def write(
        self,
        path: str,
        contents: str | bytes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView: ...

    async def download(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> bytes: ...

    async def upload(
        self,
        path: str,
        file: FileTypes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> object: ...


@runtime_checkable
class AsyncNetworkInterface(Protocol):
    """Async interface for network operations on a devbox.

    Accessed via `devbox.net` property. Provides async methods for managing SSH keys
    and network tunnels.
    """

    async def create_ssh_key(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> DevboxCreateSSHKeyResponse: ...

    async def create_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> DevboxTunnelView: ...

    async def remove_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = ...,
        idempotency_key: str | None = None,
    ) -> object: ...
