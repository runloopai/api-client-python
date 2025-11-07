from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Union, Callable, Optional, Sequence, Awaitable

from .._types import not_given
from .._client import AsyncRunloop
from ._helpers import UploadInput, normalize_upload_input
from .._streaming import AsyncStream
from ..lib.polling import PollingConfig
from .async_execution import AsyncExecution, _AsyncStreamingGroup
from .async_execution_result import AsyncExecutionResult
from ..types.devboxes.execution_update_chunk import ExecutionUpdateChunk

AsyncCallback = Callable[[str], Union[Awaitable[None], None]]


class AsyncDevboxClient:
    """
    High-level manager for creating and retrieving :class:`AsyncDevbox` instances.
    """

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    async def create(self, *, polling_config: PollingConfig | None = None, **params: Any) -> "AsyncDevbox":
        params = dict(params)
        if polling_config is None:
            polling_config = params.pop("polling_config", None)

        devbox_view = await self._client.devboxes.create_and_await_running(
            polling_config=polling_config,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)

    async def create_from_blueprint_id(
        self,
        blueprint_id: str,
        *,
        polling_config: PollingConfig | None = None,
        **params: Any,
    ) -> "AsyncDevbox":
        params = dict(params)
        params["blueprint_id"] = blueprint_id
        return await self.create(polling_config=polling_config, **params)

    async def create_from_blueprint_name(
        self,
        blueprint_name: str,
        *,
        polling_config: PollingConfig | None = None,
        **params: Any,
    ) -> "AsyncDevbox":
        params = dict(params)
        params["blueprint_name"] = blueprint_name
        return await self.create(polling_config=polling_config, **params)

    async def create_from_snapshot(
        self,
        snapshot_id: str,
        *,
        polling_config: PollingConfig | None = None,
        **params: Any,
    ) -> "AsyncDevbox":
        params = dict(params)
        params["snapshot_id"] = snapshot_id
        return await self.create(polling_config=polling_config, **params)

    def from_id(self, devbox_id: str) -> "AsyncDevbox":
        return AsyncDevbox(self._client, devbox_id)

    async def list(self, **params: Any) -> list["AsyncDevbox"]:
        page = await self._client.devboxes.list(**params)
        return [AsyncDevbox(self._client, item.id) for item in getattr(page, "devboxes", [])]


class AsyncDevbox:
    """
    Async object-oriented wrapper around devbox operations.
    """

    def __init__(self, client: AsyncRunloop, devbox_id: str) -> None:
        self._client = client
        self._id = devbox_id
        self._logger = logging.getLogger(__name__)

    def __repr__(self) -> str:
        return f"<AsyncDevbox id={self._id!r}>"

    async def __aenter__(self) -> "AsyncDevbox":
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        try:
            await self.shutdown()
        except Exception:
            self._logger.exception("failed to shutdown async devbox %s on context exit", self._id)

    @property
    def id(self) -> str:
        return self._id

    async def get_info(self, **request_options: Any) -> Any:
        return await self._client.devboxes.retrieve(self._id, **request_options)

    async def await_running(self, *, polling_config: PollingConfig | None = None) -> Any:
        return await self._client.devboxes.await_running(self._id, polling_config=polling_config)

    async def await_suspended(self, *, polling_config: PollingConfig | None = None) -> Any:
        return await self._client.devboxes.await_suspended(self._id, polling_config=polling_config)

    async def shutdown(self, **request_options: Any) -> Any:
        return await self._client.devboxes.shutdown(self._id, **request_options)

    async def suspend(self, **request_options: Any) -> Any:
        return await self._client.devboxes.suspend(self._id, **request_options)

    async def resume(self, **request_options: Any) -> Any:
        return await self._client.devboxes.resume(self._id, **request_options)

    async def keep_alive(self, **request_options: Any) -> Any:
        return await self._client.devboxes.keep_alive(self._id, **request_options)

    async def close(self) -> None:
        await self.shutdown()

    @property
    def cmd(self) -> "_AsyncCommandInterface":
        return _AsyncCommandInterface(self)

    @property
    def file(self) -> "_AsyncFileInterface":
        return _AsyncFileInterface(self)

    @property
    def net(self) -> "_AsyncNetworkInterface":
        return _AsyncNetworkInterface(self)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _start_streaming(
        self,
        execution_id: str,
        *,
        stdout: AsyncCallback | None,
        stderr: AsyncCallback | None,
        output: AsyncCallback | None,
    ) -> Optional[_AsyncStreamingGroup]:
        tasks: list[asyncio.Task[None]] = []

        if stdout or output:
            callbacks = [cb for cb in (stdout, output) if cb is not None]
            tasks.append(
                asyncio.create_task(
                    self._stream_worker(
                        name="stdout",
                        stream_factory=lambda: self._client.devboxes.executions.stream_stdout_updates(
                            execution_id,
                            devbox_id=self._id,
                        ),
                        callbacks=callbacks,
                    )
                )
            )

        if stderr or output:
            callbacks = [cb for cb in (stderr, output) if cb is not None]
            tasks.append(
                asyncio.create_task(
                    self._stream_worker(
                        name="stderr",
                        stream_factory=lambda: self._client.devboxes.executions.stream_stderr_updates(
                            execution_id,
                            devbox_id=self._id,
                        ),
                        callbacks=callbacks,
                    )
                )
            )

        if not tasks:
            return None

        return _AsyncStreamingGroup(tasks)

    async def _stream_worker(
        self,
        *,
        name: str,
        stream_factory: Callable[[], AsyncStream[ExecutionUpdateChunk]],
        callbacks: Sequence[AsyncCallback],
    ) -> None:
        logger = self._logger
        try:
            async with stream_factory() as stream:
                async for chunk in stream:
                    text = getattr(chunk, "output", "")
                    for callback in callbacks:
                        try:
                            result = callback(text)
                            if inspect.isawaitable(result):
                                await result  # type: ignore[arg-type]
                        except Exception:
                            logger.exception("error in async %s callback for devbox %s", name, self._id)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("error streaming %s logs for devbox %s", name, self._id)


class _AsyncCommandInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def exec(
        self,
        command: str,
        *,
        shell_name: str | None = None,
        stdout: AsyncCallback | None = None,
        stderr: AsyncCallback | None = None,
        output: AsyncCallback | None = None,
        polling_config: PollingConfig | None = None,
        **request_options: Any,
    ) -> AsyncExecutionResult:
        devbox = self._devbox
        client = devbox._client
        request_options = dict(request_options)
        if "shell_name" in request_options:
            shell_name = request_options.pop("shell_name")

        if stdout or stderr or output:
            execution = await client.devboxes.execute_async(
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
                    final = await client.devboxes.executions.await_completed(
                        execution.execution_id,
                        devbox_id=devbox.id,
                        polling_config=polling_config,
                    )
            except Exception:
                if streaming_group is not None:
                    await streaming_group.cancel()
                raise
            else:
                if streaming_group is not None:
                    await streaming_group.wait()

            return AsyncExecutionResult(client, devbox.id, final)

        final = await client.devboxes.execute_and_await_completion(
            devbox.id,
            command=command,
            shell_name=shell_name if shell_name is not None else not_given,
            polling_config=polling_config,
            **request_options,
        )
        return AsyncExecutionResult(client, devbox.id, final)

    async def exec_async(
        self,
        command: str,
        *,
        shell_name: str | None = None,
        stdout: AsyncCallback | None = None,
        stderr: AsyncCallback | None = None,
        output: AsyncCallback | None = None,
        **request_options: Any,
    ) -> AsyncExecution:
        devbox = self._devbox
        client = devbox._client
        request_options = dict(request_options)
        if "shell_name" in request_options:
            shell_name = request_options.pop("shell_name")

        execution = await client.devboxes.execute_async(
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

        return AsyncExecution(client, devbox.id, execution, streaming_group)


class _AsyncFileInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def read(self, path: str, **request_options: Any) -> str:
        return await self._devbox._client.devboxes.read_file_contents(
            self._devbox.id, file_path=path, **request_options
        )

    async def write(self, path: str, contents: str | bytes, **request_options: Any) -> Any:
        if isinstance(contents, bytes):
            contents_str = contents.decode("utf-8")
        else:
            contents_str = contents

        return await self._devbox._client.devboxes.write_file_contents(
            self._devbox.id,
            file_path=path,
            contents=contents_str,
            **request_options,
        )

    async def download(self, path: str, **request_options: Any) -> bytes:
        response = await self._devbox._client.devboxes.download_file(
            self._devbox.id,
            path=path,
            **request_options,
        )
        return await response.read()

    async def upload(self, path: str, file: UploadInput, **request_options: Any) -> Any:
        file_param = normalize_upload_input(file)
        return await self._devbox._client.devboxes.upload_file(
            self._devbox.id,
            path=path,
            file=file_param,
            **request_options,
        )


class _AsyncNetworkInterface:
    def __init__(self, devbox: AsyncDevbox) -> None:
        self._devbox = devbox

    async def create_ssh_key(self, **request_options: Any) -> Any:
        return await self._devbox._client.devboxes.create_ssh_key(self._devbox.id, **request_options)

    async def create_tunnel(self, *, port: int, **request_options: Any) -> Any:
        return await self._devbox._client.devboxes.create_tunnel(self._devbox.id, port=port, **request_options)

    async def remove_tunnel(self, *, port: int, **request_options: Any) -> Any:
        return await self._devbox._client.devboxes.remove_tunnel(self._devbox.id, port=port, **request_options)
