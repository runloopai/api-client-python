from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Any, Dict, Callable, Optional, Sequence
from typing_extensions import override

from ..types import (
    DevboxView,
    DevboxTunnelView,
    DevboxExecutionDetailView,
    DevboxCreateSSHKeyResponse,
)
from .._types import Body, Omit, Query, Headers, Timeout, NotGiven, FileTypes, omit, not_given
from .._client import Runloop
from ._helpers import LogCallback
from .execution import Execution, _StreamingGroup
from .._streaming import Stream
from ..lib.polling import PollingConfig
from .execution_result import ExecutionResult
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ..types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView

if TYPE_CHECKING:
    from .snapshot import Snapshot


class Devbox:
    """
    Object-oriented wrapper around devbox operations.
    """

    def __init__(self, client: Runloop, devbox_id: str) -> None:
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    @override
    def __repr__(self) -> str:
        return f"<Devbox id={self._id!r}>"

    def __enter__(self) -> "Devbox":
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        try:
            self.shutdown()
        except Exception:
            self._logger.exception("failed to shutdown devbox %s on context exit", self._id)

    @property
    def id(self) -> str:
        return self._id

    def get_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> DevboxView:
        return self._client.devboxes.retrieve(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def await_running(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        return self._client.devboxes.await_running(self._id, polling_config=polling_config)

    def await_suspended(self, *, polling_config: PollingConfig | None = None) -> DevboxView:
        return self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    def shutdown(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        return self._client.devboxes.shutdown(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def suspend(
        self,
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        self._client.devboxes.suspend(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    def resume(
        self,
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        self._client.devboxes.resume(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return self._client.devboxes.await_running(self._id, polling_config=polling_config)

    def keep_alive(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return self._client.devboxes.keep_alive(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def snapshot_disk(
        self,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> "Snapshot":
        snapshot_data = self._client.devboxes.snapshot_disk_async(
            self._id,
            commit_message=commit_message,
            metadata=metadata,
            name=name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        snapshot = self._snapshot_from_id(snapshot_data.id)
        snapshot.await_completed(
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return snapshot

    def snapshot_disk_async(
        self,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> "Snapshot":
        snapshot_data = self._client.devboxes.snapshot_disk_async(
            self._id,
            commit_message=commit_message,
            metadata=metadata,
            name=name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return self._snapshot_from_id(snapshot_data.id)

    def close(self) -> None:
        self.shutdown()

    @property
    def cmd(self) -> "_CommandInterface":
        return _CommandInterface(self)

    @property
    def file(self) -> "_FileInterface":
        return _FileInterface(self)

    @property
    def net(self) -> "_NetworkInterface":
        return _NetworkInterface(self)

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _snapshot_from_id(self, snapshot_id: str) -> "Snapshot":
        from .snapshot import Snapshot

        return Snapshot(self._client, snapshot_id)

    def _start_streaming(
        self,
        execution_id: str,
        *,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
    ) -> Optional[_StreamingGroup]:
        threads: list[threading.Thread] = []
        stop_event = threading.Event()

        if stdout or output:
            callbacks = [cb for cb in (stdout, output) if cb is not None]
            threads.append(
                self._spawn_stream_thread(
                    name="stdout",
                    stream_factory=lambda: self._client.devboxes.executions.stream_stdout_updates(
                        execution_id,
                        devbox_id=self._id,
                    ),
                    callbacks=callbacks,
                    stop_event=stop_event,
                )
            )

        if stderr or output:
            callbacks = [cb for cb in (stderr, output) if cb is not None]
            threads.append(
                self._spawn_stream_thread(
                    name="stderr",
                    stream_factory=lambda: self._client.devboxes.executions.stream_stderr_updates(
                        execution_id,
                        devbox_id=self._id,
                    ),
                    callbacks=callbacks,
                    stop_event=stop_event,
                )
            )

        if not threads:
            return None

        return _StreamingGroup(threads, stop_event)

    def _spawn_stream_thread(
        self,
        *,
        name: str,
        stream_factory: Callable[[], Stream[ExecutionUpdateChunk]],
        callbacks: Sequence[LogCallback],
        stop_event: threading.Event,
    ) -> threading.Thread:
        logger = self._logger

        def worker() -> None:
            try:
                with stream_factory() as stream:
                    for chunk in stream:
                        if stop_event.is_set():
                            break
                        text = chunk.output
                        for callback in callbacks:
                            try:
                                callback(text)
                            except Exception:
                                logger.exception("error in %s callback for devbox %s", name, self._id)
            except Exception:
                logger.exception("error streaming %s logs for devbox %s", name, self._id)

        thread = threading.Thread(
            target=worker,
            name=f"runloop-devbox-{self._id}-{name}",
            daemon=True,
        )
        thread.start()
        return thread


class _CommandInterface:
    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def exec(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = omit,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
        polling_config: PollingConfig | None = None,
        attach_stdin: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ExecutionResult:
        devbox = self._devbox
        client = devbox._client

        if stdout or stderr or output:
            execution: DevboxAsyncExecutionDetailView = client.devboxes.execute_async(
                devbox.id,
                command=command,
                shell_name=shell_name,
                attach_stdin=attach_stdin,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            )
            streaming_group = devbox._start_streaming(
                execution.execution_id,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
            final = execution
            if execution.status == "completed":
                final: DevboxAsyncExecutionDetailView = execution
            else:
                final = client.devboxes.executions.await_completed(
                    execution.execution_id,
                    devbox_id=devbox.id,
                    polling_config=polling_config,
                )

            if streaming_group is not None:
                # Ensure log streaming has drained before returning the result. _stop_streaming()
                # below will perform the final cleanup, but we still join here so callers only
                # resume once all logs have been delivered.
                streaming_group.join()

            return ExecutionResult(client, devbox.id, final)

        final = client.devboxes.execute_and_await_completion(
            devbox.id,
            command=command,
            shell_name=shell_name,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return ExecutionResult(client, devbox.id, final)

    def exec_async(
        self,
        command: str,
        *,
        shell_name: Optional[str] | Omit = omit,
        stdout: Optional[LogCallback] = None,
        stderr: Optional[LogCallback] = None,
        output: Optional[LogCallback] = None,
        attach_stdin: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Execution:
        devbox = self._devbox
        client = devbox._client

        execution: DevboxAsyncExecutionDetailView = client.devboxes.execute_async(
            devbox.id,
            command=command,
            shell_name=shell_name,
            attach_stdin=attach_stdin,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

        streaming_group = devbox._start_streaming(
            execution.execution_id,
            stdout=stdout,
            stderr=stderr,
            output=output,
        )

        return Execution(client, devbox.id, execution, streaming_group)


class _FileInterface:
    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def read(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        return self._devbox._client.devboxes.read_file_contents(
            self._devbox.id,
            file_path=path,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def write(
        self,
        path: str,
        contents: str | bytes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView:
        if isinstance(contents, bytes):
            contents_str = contents.decode("utf-8")
        else:
            contents_str = contents

        return self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            file_path=path,
            contents=contents_str,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def download(
        self,
        path: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> bytes:
        response = self._devbox._client.devboxes.download_file(
            self._devbox.id,
            path=path,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return response.read()

    def upload(
        self,
        path: str,
        file: FileTypes,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            path=path,
            file=file,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )


class _NetworkInterface:
    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def create_ssh_key(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxCreateSSHKeyResponse:
        return self._devbox._client.devboxes.create_ssh_key(
            self._devbox.id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def create_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxTunnelView:
        return self._devbox._client.devboxes.create_tunnel(
            self._devbox.id,
            port=port,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def remove_tunnel(
        self,
        *,
        port: int,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return self._devbox._client.devboxes.remove_tunnel(
            self._devbox.id,
            port=port,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
