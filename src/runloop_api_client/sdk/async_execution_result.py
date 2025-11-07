from __future__ import annotations

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
        execution: DevboxAsyncExecutionDetailView,
    ) -> None:
        self._client = client
        self._devbox_id = devbox_id
        self._execution = execution

    @property
    def devbox_id(self) -> str:
        return self._devbox_id

    @property
    def execution_id(self) -> str:
        return self._execution.execution_id

    @property
    def exit_code(self) -> int | None:
        return self._execution.exit_status

    @property
    def success(self) -> bool:
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        exit_code = self.exit_code
        return exit_code is not None and exit_code != 0

    async def stdout(self) -> str:
        return self._execution.stdout or ""

    async def stderr(self) -> str:
        return self._execution.stderr or ""

    @property
    def raw(self) -> DevboxAsyncExecutionDetailView:
        return self._execution
