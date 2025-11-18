"""Execution management for async commands."""

from __future__ import annotations

import logging
import threading
from typing import Optional
from typing_extensions import Unpack, override

from ._types import RequestOptions, LongRequestOptions
from .._client import Runloop
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
    """Manages an asynchronous command execution on a devbox.

    Provides methods to poll execution state, wait for completion, and terminate
    the running process. Created by ``devbox.cmd.exec_async()``.

    Attributes:
        execution_id: The unique execution identifier.
        devbox_id: The devbox where the command is executing.

    Example:
        >>> execution = devbox.cmd.exec_async(command="python train.py")
        >>> state = execution.get_state()
        >>> if state.status == "running":
        ...     execution.kill()
        >>> result = execution.result()  # Wait for completion
        >>> print(result.stdout())
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
        self._initial_result = execution
        self._streaming_group = streaming_group

    @override
    def __repr__(self) -> str:
        return f"<Execution id={self._execution_id!r}>"

    @property
    def execution_id(self) -> str:
        """Return the execution identifier.

        Returns:
            str: Unique execution ID.
        """
        return self._execution_id

    @property
    def devbox_id(self) -> str:
        """Return the devbox identifier.

        Returns:
            str: Devbox ID where the command is running.
        """
        return self._devbox_id

    def result(self, **options: Unpack[LongRequestOptions]) -> ExecutionResult:
        """Wait for completion and return an :class:`ExecutionResult`.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            ExecutionResult: Wrapper with exit status and output helpers.
        """
        # Wait for command completion
        final = self._client.devboxes.wait_for_command(
            self._execution_id,
            devbox_id=self._devbox_id,
            statuses=["completed"],
            **options,
        )

        # Wait for streaming to complete naturally (log but don't throw streaming errors)
        if self._streaming_group is not None:
            self._streaming_group.join()
            self._streaming_group = None

        return ExecutionResult(self._client, self._devbox_id, final)

    def get_state(self, **options: Unpack[RequestOptions]) -> DevboxAsyncExecutionDetailView:
        """Fetch the latest execution state.

        Args:
            **options: Optional request configuration.

        Returns:
            DevboxAsyncExecutionDetailView: Current execution metadata.
        """
        return self._client.devboxes.executions.retrieve(
            self._execution_id,
            devbox_id=self._devbox_id,
            **options,
        )

    def kill(self, **options: Unpack[LongRequestOptions]) -> None:
        """Request termination of the running execution.

        Args:
            **options: Optional long-running request configuration.
        """
        self._client.devboxes.executions.kill(
            self._execution_id,
            devbox_id=self._devbox_id,
            **options,
        )
