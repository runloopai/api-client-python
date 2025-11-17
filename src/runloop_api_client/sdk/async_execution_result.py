"""Async execution result wrapper for completed commands."""

from __future__ import annotations

from typing import Callable, Optional, Awaitable
from typing_extensions import override

from .._client import AsyncRunloop
from .._streaming import AsyncStream
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView


class AsyncExecutionResult:
    """
    Completed asynchronous command execution result.
    """

    def __init__(
        self,
        client: AsyncRunloop,
        devbox_id: str,
        result: DevboxAsyncExecutionDetailView,
    ) -> None:
        self._client = client
        self._devbox_id = devbox_id
        self._result = result

    @override
    def __repr__(self) -> str:
        return f"<AsyncExecutionResult id={self.execution_id!r} exit={self.exit_code}>"

    @property
    def devbox_id(self) -> str:
        return self._devbox_id

    @property
    def execution_id(self) -> str:
        return self._result.execution_id

    @property
    def exit_code(self) -> int | None:
        return self._result.exit_status

    @property
    def success(self) -> bool:
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        exit_code = self.exit_code
        return exit_code is not None and exit_code != 0

    def _count_non_empty_lines(self, text: str) -> int:
        """Count non-empty lines in text, excluding trailing empty strings."""
        if not text:
            return 0
        # Remove trailing newlines, split, and count non-empty lines
        return sum(1 for line in text.rstrip("\n").split("\n") if line)

    def _get_last_n_lines(self, text: str, n: int) -> str:
        """Extract the last N lines from text."""
        if n <= 0 or not text:
            return ""
        # Remove trailing newlines before splitting and slicing
        return "\n".join(text.rstrip("\n").split("\n")[-n:])

    async def _get_output(
        self,
        current_output: str,
        is_truncated: bool,
        num_lines: Optional[int],
        stream_fn: Callable[[], Awaitable[AsyncStream[ExecutionUpdateChunk]]],
    ) -> str:
        """Common logic for getting output with optional line limiting and streaming."""
        # Check if we have enough lines already
        if num_lines is not None and (not is_truncated or self._count_non_empty_lines(current_output) >= num_lines):
            return self._get_last_n_lines(current_output, num_lines)

        # Stream full output if truncated
        if is_truncated:
            stream = await stream_fn()
            output = "".join([chunk.output async for chunk in stream])
            return self._get_last_n_lines(output, num_lines) if num_lines is not None else output

        # Return current output, optionally limited to last N lines
        return self._get_last_n_lines(current_output, num_lines) if num_lines is not None else current_output

    async def stdout(self, num_lines: Optional[int] = None) -> str:
        """
        Return captured standard output, streaming full output if truncated.

        Args:
            num_lines: Optional number of lines to return from the end (most recent)

        Returns:
            stdout content, optionally limited to last N lines
        """
        return await self._get_output(
            self._result.stdout or "",
            self._result.stdout_truncated is True,
            num_lines,
            lambda: self._client.devboxes.executions.stream_stdout_updates(
                self.execution_id, devbox_id=self._devbox_id
            ),
        )

    async def stderr(self, num_lines: Optional[int] = None) -> str:
        """
        Return captured standard error, streaming full output if truncated.

        Args:
            num_lines: Optional number of lines to return from the end (most recent)

        Returns:
            stderr content, optionally limited to last N lines
        """
        return await self._get_output(
            self._result.stderr or "",
            self._result.stderr_truncated is True,
            num_lines,
            lambda: self._client.devboxes.executions.stream_stderr_updates(
                self.execution_id, devbox_id=self._devbox_id
            ),
        )

    @property
    def raw(self) -> DevboxAsyncExecutionDetailView:
        return self._result
