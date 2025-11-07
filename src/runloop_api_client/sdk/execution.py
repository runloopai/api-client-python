from __future__ import annotations

import logging
import threading
from typing import Optional

from .._client import Runloop
from ..lib.polling import PollingConfig
from .execution_result import ExecutionResult
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView


class _StreamingGroup:
    """
    Internal helper used to coordinate stdout/stderr streaming threads.
    """

    def __init__(self, threads: list[threading.Thread], stop_event: threading.Event) -> None:
        self._threads = threads
        self._stop_event = stop_event
        self._logger = logging.getLogger(__name__)

    def stop(self) -> None:
        self._stop_event.set()

    def join(self, timeout: float = 5.0) -> None:
        for thread in self._threads:
            thread.join(timeout)
            if thread.is_alive():
                self._logger.debug("streaming thread %s still running after join timeout", thread.name)

    @property
    def active(self) -> bool:
        return any(thread.is_alive() for thread in self._threads)


class Execution:
    """
    Represents an asynchronous command execution on a devbox.
    """

    def __init__(
        self,
        client: Runloop,
        devbox_id: str,
        execution: DevboxAsyncExecutionDetailView,
        streaming_group: Optional[_StreamingGroup] = None,
    ) -> None:
        self._client = client
        self._devbox_id = devbox_id
        self._execution_id = execution.execution_id
        self._latest = execution
        self._streaming_group = streaming_group

    @property
    def execution_id(self) -> str:
        return self._execution_id

    @property
    def devbox_id(self) -> str:
        return self._devbox_id

    def result(self, *, polling_config: PollingConfig | None = None) -> ExecutionResult:
        """
        Wait for completion and return an :class:`ExecutionResult`.
        """
        try:
            if self._latest.status == "completed":
                final = self._latest
            else:
                final = self._client.devboxes.executions.await_completed(
                    self._execution_id,
                    devbox_id=self._devbox_id,
                    polling_config=polling_config,
                )
        finally:
            self._stop_streaming()

        self._latest = final
        return ExecutionResult(self._client, self._devbox_id, final)

    def get_state(self) -> DevboxAsyncExecutionDetailView:
        """
        Fetch the latest execution state.
        """
        self._latest = self._client.devboxes.executions.retrieve(
            self._execution_id,
            devbox_id=self._devbox_id,
        )
        return self._latest

    def kill(self, *, kill_process_group: bool | None = None) -> None:
        """
        Request termination of the running execution.
        """
        self._client.devboxes.executions.kill(
            self._execution_id,
            devbox_id=self._devbox_id,
            kill_process_group=kill_process_group,
        )
        self._stop_streaming()

    def _stop_streaming(self) -> None:
        if self._streaming_group is None:
            return
        self._streaming_group.stop()
        self._streaming_group.join()
        self._streaming_group = None
