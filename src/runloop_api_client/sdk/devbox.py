from __future__ import annotations

import logging
import threading
from typing import Any, Callable, Optional, Sequence

from .._types import not_given
from .._client import Runloop
from ._helpers import UploadInput, normalize_upload_input
from .execution import Execution, _StreamingGroup
from .._streaming import Stream
from ..lib.polling import PollingConfig
from .execution_result import ExecutionResult
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk

LogCallback = Callable[[str], None]


class DevboxClient:
    """
    High-level manager for creating and retrieving :class:`Devbox` instances.
    """

    def __init__(self, client: Runloop) -> None:
        self._client = client

    def create(self, *, polling_config: PollingConfig | None = None, **params: Any) -> "Devbox":
        """
        Create a new devbox and block until it is running.
        """
        params = dict(params)
        if polling_config is None:
            polling_config = params.pop("polling_config", None)

        devbox_view = self._client.devboxes.create_and_await_running(
            polling_config=polling_config,
            **params,
        )
        return Devbox(self._client, devbox_view.id)

    def create_from_blueprint_id(
        self,
        blueprint_id: str,
        *,
        polling_config: PollingConfig | None = None,
        **params: Any,
    ) -> "Devbox":
        params = dict(params)
        params["blueprint_id"] = blueprint_id
        return self.create(polling_config=polling_config, **params)

    def create_from_blueprint_name(
        self,
        blueprint_name: str,
        *,
        polling_config: PollingConfig | None = None,
        **params: Any,
    ) -> "Devbox":
        params = dict(params)
        params["blueprint_name"] = blueprint_name
        return self.create(polling_config=polling_config, **params)

    def create_from_snapshot(
        self,
        snapshot_id: str,
        *,
        polling_config: PollingConfig | None = None,
        **params: Any,
    ) -> "Devbox":
        params = dict(params)
        params["snapshot_id"] = snapshot_id
        return self.create(polling_config=polling_config, **params)

    def from_id(self, devbox_id: str) -> "Devbox":
        """
        Create a :class:`Devbox` wrapper for an existing devbox ID.
        """
        return Devbox(self._client, devbox_id)

    def list(self, **params: Any) -> list["Devbox"]:
        """
        List devboxes and return lightweight :class:`Devbox` wrappers.
        """
        page = self._client.devboxes.list(**params)
        return [Devbox(self._client, item.id) for item in getattr(page, "devboxes", [])]


class Devbox:
    """
    Object-oriented wrapper around devbox operations.
    """

    def __init__(self, client: Runloop, devbox_id: str) -> None:
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

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

    def get_info(self, **request_options: Any) -> Any:
        return self._client.devboxes.retrieve(self._id, **request_options)

    def await_running(self, *, polling_config: PollingConfig | None = None) -> Any:
        return self._client.devboxes.await_running(self._id, polling_config=polling_config)

    def await_suspended(self, *, polling_config: PollingConfig | None = None) -> Any:
        return self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    def shutdown(self, **request_options: Any) -> Any:
        return self._client.devboxes.shutdown(self._id, **request_options)

    def suspend(self, **request_options: Any) -> Any:
        return self._client.devboxes.suspend(self._id, **request_options)

    def resume(self, **request_options: Any) -> Any:
        return self._client.devboxes.resume(self._id, **request_options)

    def snapshot_disk(
        self,
        *,
        commit_message: str | None | Omit = omit,
        metadata: dict[str, str] | None | Omit = omit,
        name: str | None | Omit = omit,
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
            idempotency_key=idempotency_key,
        )
        return snapshot

    def snapshot_disk_async(
        self,
        *,
        commit_message: str | None | Omit = omit,
        metadata: dict[str, str] | None | Omit = omit,
        name: str | None | Omit = omit,
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
        stdout: LogCallback | None,
        stderr: LogCallback | None,
        output: LogCallback | None,
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
                        text = getattr(chunk, "output", "")
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
        shell_name: str | None = None,
        stdout: LogCallback | None = None,
        stderr: LogCallback | None = None,
        output: LogCallback | None = None,
        polling_config: PollingConfig | None = None,
        **request_options: Any,
    ) -> ExecutionResult:
        devbox = self._devbox
        client = devbox._client
        request_options = dict(request_options)
        if "shell_name" in request_options:
            shell_name = request_options.pop("shell_name")

        if stdout or stderr or output:
            execution = client.devboxes.execute_async(
                devbox.id,
                command=command,
                shell_name=shell_name,
                **request_options,
            )
            streaming_group = devbox._start_streaming(
                execution.execution_id,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
            try:
                if execution.status == "completed":
                    final = execution
                else:
                    final = client.devboxes.executions.await_completed(
                        execution.execution_id,
                        devbox_id=devbox.id,
                        polling_config=polling_config,
                    )
            finally:
                if streaming_group is not None:
                    streaming_group.stop()
                    streaming_group.join()

            return ExecutionResult(client, devbox.id, final)

        final = client.devboxes.execute_and_await_completion(
            devbox.id,
            command=command,
            shell_name=shell_name if shell_name is not None else not_given,
            polling_config=polling_config,
            **request_options,
        )
        return ExecutionResult(client, devbox.id, final)

    def exec_async(
        self,
        command: str,
        *,
        shell_name: str | None = None,
        stdout: LogCallback | None = None,
        stderr: LogCallback | None = None,
        output: LogCallback | None = None,
        **request_options: Any,
    ) -> Execution:
        devbox = self._devbox
        client = devbox._client
        request_options = dict(request_options)
        if "shell_name" in request_options:
            shell_name = request_options.pop("shell_name")

        execution = client.devboxes.execute_async(
            devbox.id,
            command=command,
            shell_name=shell_name,
            **request_options,
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

    def read(self, path: str, **request_options: Any) -> str:
        return self._devbox._client.devboxes.read_file_contents(self._devbox.id, file_path=path, **request_options)

    def write(self, path: str, contents: str | bytes, **request_options: Any) -> Any:
        if isinstance(contents, bytes):
            contents_str = contents.decode("utf-8")
        else:
            contents_str = contents

        return self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            file_path=path,
            contents=contents_str,
            **request_options,
        )

    def download(self, path: str, **request_options: Any) -> bytes:
        response = self._devbox._client.devboxes.download_file(
            self._devbox.id,
            path=path,
            **request_options,
        )
        return response.read()

    def upload(self, path: str, file: UploadInput, **request_options: Any) -> Any:
        file_param = normalize_upload_input(file)
        return self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            path=path,
            file=file_param,
            **request_options,
        )


class _NetworkInterface:
    def __init__(self, devbox: Devbox) -> None:
        self._devbox = devbox

    def create_ssh_key(self, **request_options: Any) -> Any:
        return self._devbox._client.devboxes.create_ssh_key(self._devbox.id, **request_options)

    def create_tunnel(self, *, port: int, **request_options: Any) -> Any:
        return self._devbox._client.devboxes.create_tunnel(self._devbox.id, port=port, **request_options)

    def remove_tunnel(self, *, port: int, **request_options: Any) -> Any:
        return self._devbox._client.devboxes.remove_tunnel(self._devbox.id, port=port, **request_options)
