"""Async execution result wrapper for completed commands."""

from __future__ import annotations

from typing import Callable, Optional, Awaitable
from typing_extensions import override

from .._client import AsyncRunloop
from .._streaming import AsyncStream
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView


class AsyncExecutionResult:
    """Completed asynchronous command execution result.

    Provides convenient helpers to inspect process exit status and captured
    output.
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
        """Associated devbox identifier.

        Returns:
            str: Devbox ID where the command executed.
        """
        return self._devbox_id

    @property
    def execution_id(self) -> str:
        """Underlying execution identifier.

        Returns:
            str: Unique execution ID.
        """
        return self._result.execution_id

    @property
    def exit_code(self) -> int | None:
        """Process exit code, or ``None`` if unavailable.

        Returns:
            int | None: Exit status code.
        """
        return self._result.exit_status

    @property
    def success(self) -> bool:
        """Whether the process exited successfully (exit code ``0``).

        Returns:
            bool: ``True`` if the exit code is ``0``.
        """
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        """Whether the process exited with a non-zero exit code.

        Returns:
            bool: ``True`` if the exit code is non-zero.
        """
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
        # TODO: Fix inconsistency - _count_non_empty_lines counts non-empty lines but
        # _get_last_n_lines returns N lines (may include empty ones). This means
        # num_lines=50 might return fewer than 50 non-empty lines. Should either:
        # 1. Make _get_last_n_lines return N non-empty lines, OR
        # 2. Make _count_non_empty_lines count all lines
        # This affects both Python and TypeScript SDKs - fix together.
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
        """Common helper for fetching buffered or streamed output.

        Args:
            current_output: Cached output string from the API.
            is_truncated: Whether ``current_output`` is truncated.
            num_lines: Optional number of tail lines to return.
            stream_fn: Awaitable returning a streaming iterator for full output.

        Returns:
            str: Output string honoring ``num_lines`` if provided.
        """
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
            num_lines: Optional number of lines to return from the end (most recent).

        Returns:
            str: Stdout content, optionally limited to the last ``num_lines`` lines.
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
            num_lines: Optional number of lines to return from the end (most recent).

        Returns:
            str: Stderr content, optionally limited to the last ``num_lines`` lines.
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
    def result(self) -> DevboxAsyncExecutionDetailView:
        """Get the raw execution result.

        Returns:
            DevboxAsyncExecutionDetailView: Raw execution result.
        """
        return self._result
