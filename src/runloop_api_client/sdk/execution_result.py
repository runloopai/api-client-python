"""Execution result wrapper for completed commands."""

from __future__ import annotations

from .._client import Runloop
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView


class ExecutionResult:
    """
    Completed command execution result.

    Provides convenient helpers to inspect process exit status and captured output.
    """

    def __init__(
        self,
        client: Runloop,
        devbox_id: str,
        execution: DevboxAsyncExecutionDetailView,
    ) -> None:
        self._client = client
        self._devbox_id = devbox_id
        self._execution = execution

    @property
    def devbox_id(self) -> str:
        """Associated devbox identifier."""
        return self._devbox_id

    @property
    def execution_id(self) -> str:
        """Underlying execution identifier."""
        return self._execution.execution_id

    @property
    def exit_code(self) -> int | None:
        """Process exit code, or ``None`` if unavailable."""
        return self._execution.exit_status

    @property
    def success(self) -> bool:
        """Whether the process exited successfully (exit code ``0``)."""
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        """Whether the process exited with a non-zero exit code."""
        exit_code = self.exit_code
        return exit_code is not None and exit_code != 0

    def stdout(self) -> str:
        """Return captured standard output."""
        return self._execution.stdout or ""

    def stderr(self) -> str:
        """Return captured standard error."""
        return self._execution.stderr or ""

    @property
    def raw(self) -> DevboxAsyncExecutionDetailView:
        """Access the underlying API response."""
        return self._execution
