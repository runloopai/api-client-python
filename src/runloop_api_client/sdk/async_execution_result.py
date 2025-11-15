"""Async execution result wrapper for completed commands."""

from __future__ import annotations

from typing_extensions import Optional, override

from .._client import AsyncRunloop
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

    # TODO: add pagination support once we have it in the API
    async def stdout(self, num_lines: Optional[int] = None) -> str:
        if not num_lines or num_lines <= 0 or not self._result.stdout:
            return ""
        return self._result.stdout[-num_lines:]

    # TODO: add pagination support once we have it in the API
    async def stderr(self, num_lines: Optional[int] = None) -> str:
        if not num_lines or num_lines <= 0 or not self._result.stderr:
            return ""
        return self._result.stderr[-num_lines:]

    @property
    def raw(self) -> DevboxAsyncExecutionDetailView:
        return self._result
