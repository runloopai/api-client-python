"""Execution result wrapper for completed commands."""

from __future__ import annotations

from typing import Optional
from typing_extensions import override

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
        result: DevboxAsyncExecutionDetailView,
    ) -> None:
        self._client = client
        self._devbox_id = devbox_id
        self._result = result

    @override
    def __repr__(self) -> str:
        return f"<ExecutionResult id={self.execution_id!r} exit={self.exit_code}>"

    @property
    def devbox_id(self) -> str:
        """Associated devbox identifier."""
        return self._devbox_id

    @property
    def execution_id(self) -> str:
        """Underlying execution identifier."""
        return self._result.execution_id

    @property
    def exit_code(self) -> int | None:
        """Process exit code, or ``None`` if unavailable."""
        return self._result.exit_status

    @property
    def success(self) -> bool:
        """Whether the process exited successfully (exit code ``0``)."""
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        """Whether the process exited with a non-zero exit code."""
        exit_code = self.exit_code
        return exit_code is not None and exit_code != 0

    # TODO: add pagination support once we have it in the API
    def stdout(self, num_lines: Optional[int] = None) -> str:
        """Return captured standard output."""
        if not num_lines or num_lines <= 0 or not self._result.stdout:
            return ""
        return self._result.stdout[-num_lines:]

    # TODO: add pagination support once we have it in the API
    def stderr(self, num_lines: Optional[int] = None) -> str:
        """Return captured standard error."""
        if not num_lines or num_lines <= 0 or not self._result.stderr:
            return ""
        return self._result.stderr[-num_lines:]

    @property
    def raw(self) -> DevboxAsyncExecutionDetailView:
        """Access the underlying API response."""
        return self._result
