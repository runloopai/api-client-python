from __future__ import annotations

from types import SimpleNamespace
from typing import List

import pytest

from runloop_api_client import AsyncRunloopSDK
from runloop_api_client.sdk import AsyncDevbox, AsyncExecution, AsyncExecutionResult


@pytest.fixture()
async def async_sdk() -> AsyncRunloopSDK:
    sdk = AsyncRunloopSDK(bearer_token="test-token")
    try:
        yield sdk
    finally:
        await sdk.aclose()


@pytest.mark.asyncio
async def test_async_create_returns_devbox(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    devboxes_resource = async_sdk.api.devboxes

    async def fake_create_and_await_running(**_kwargs):
        return SimpleNamespace(id="adev_1")

    monkeypatch.setattr(devboxes_resource, "create_and_await_running", fake_create_and_await_running)

    devbox = await async_sdk.devbox.create(name="async")

    assert isinstance(devbox, AsyncDevbox)
    assert devbox.id == "adev_1"


@pytest.mark.asyncio
async def test_async_context_manager(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    devboxes_resource = async_sdk.api.devboxes
    calls: List[str] = []

    async def fake_shutdown(devbox_id: str, **_kwargs):
        calls.append(devbox_id)

    monkeypatch.setattr(devboxes_resource, "shutdown", fake_shutdown)

    async with async_sdk.devbox.from_id("adev_ctx") as devbox:
        assert devbox.id == "adev_ctx"

    assert calls == ["adev_ctx"]


@pytest.mark.asyncio
async def test_async_exec_without_streaming(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    devboxes_resource = async_sdk.api.devboxes

    result = SimpleNamespace(
        execution_id="exec-async-1",
        devbox_id="adev_exec",
        stdout="async hello",
        stderr="",
        exit_status=0,
        status="completed",
    )

    async def fake_execute_and_await_completion(devbox_id: str, **kwargs):
        assert devbox_id == "adev_exec"
        assert kwargs["command"] == "echo hi"
        return result

    monkeypatch.setattr(devboxes_resource, "execute_and_await_completion", fake_execute_and_await_completion)

    devbox = async_sdk.devbox.from_id("adev_exec")
    execution_result = await devbox.cmd.exec("echo hi")

    assert isinstance(execution_result, AsyncExecutionResult)
    assert execution_result.exit_code == 0
    assert await execution_result.stdout() == "async hello"


@pytest.mark.asyncio
async def test_async_exec_with_streaming(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    devboxes_resource = async_sdk.api.devboxes
    executions_resource = devboxes_resource.executions

    execution = SimpleNamespace(
        execution_id="exec-stream-async",
        devbox_id="adev_stream",
        stdout="",
        stderr="",
        exit_status=None,
        status="running",
    )

    final = SimpleNamespace(
        execution_id="exec-stream-async",
        devbox_id="adev_stream",
        stdout="done",
        stderr="",
        exit_status=0,
        status="completed",
    )

    async def fake_execute_async(devbox_id: str, **kwargs):
        assert kwargs["command"] == "long async task"
        return execution

    async def fake_await_completed(execution_id: str, *, devbox_id: str, **_kwargs):
        assert execution_id == "exec-stream-async"
        assert devbox_id == "adev_stream"
        return final

    class DummyAsyncStream:
        def __init__(self, values: list[str]):
            self._values = values

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        def __aiter__(self):
            async def generator():
                for value in self._values:
                    yield SimpleNamespace(output=value)

            return generator()

    monkeypatch.setattr(devboxes_resource, "execute_async", fake_execute_async)
    monkeypatch.setattr(executions_resource, "await_completed", fake_await_completed)
    monkeypatch.setattr(
        executions_resource,
        "stream_stdout_updates",
        lambda execution_id, *, devbox_id: DummyAsyncStream(["a", "b"]),
    )
    monkeypatch.setattr(
        executions_resource,
        "stream_stderr_updates",
        lambda execution_id, *, devbox_id: DummyAsyncStream([]),
    )

    stdout_logs: list[str] = []
    combined_logs: list[str] = []

    async def capture_stdout(line: str) -> None:
        stdout_logs.append(line)

    async def capture_output(line: str) -> None:
        combined_logs.append(line)

    devbox = async_sdk.devbox.from_id("adev_stream")
    result = await devbox.cmd.exec(
        "long async task",
        stdout=capture_stdout,
        output=capture_output,
    )

    assert stdout_logs == ["a", "b"]
    assert combined_logs == ["a", "b"]
    assert await result.stdout() == "done"


@pytest.mark.asyncio
async def test_async_exec_async_returns_execution(monkeypatch: pytest.MonkeyPatch, async_sdk: AsyncRunloopSDK) -> None:
    devboxes_resource = async_sdk.api.devboxes
    executions_resource = devboxes_resource.executions

    execution = SimpleNamespace(
        execution_id="exec-async-bg",
        devbox_id="adev_bg",
        stdout="",
        stderr="",
        exit_status=None,
        status="running",
    )

    final = SimpleNamespace(
        execution_id="exec-async-bg",
        devbox_id="adev_bg",
        stdout="finished",
        stderr="",
        exit_status=0,
        status="completed",
    )

    async def fake_execute_async(devbox_id: str, **kwargs):
        return execution

    async def fake_await_completed(execution_id: str, *, devbox_id: str, **_kwargs):
        return final

    class EmptyAsyncStream:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        def __aiter__(self):
            async def generator():
                if False:
                    yield  # pragma: no cover

            return generator()

    monkeypatch.setattr(devboxes_resource, "execute_async", fake_execute_async)
    monkeypatch.setattr(executions_resource, "await_completed", fake_await_completed)
    monkeypatch.setattr(
        executions_resource,
        "stream_stdout_updates",
        lambda execution_id, *, devbox_id: EmptyAsyncStream(),
    )
    monkeypatch.setattr(
        executions_resource,
        "stream_stderr_updates",
        lambda execution_id, *, devbox_id: EmptyAsyncStream(),
    )

    devbox = async_sdk.devbox.from_id("adev_bg")
    execution_obj = await devbox.cmd.exec_async("background async task")

    assert isinstance(execution_obj, AsyncExecution)
    result = await execution_obj.result()
    assert await result.stdout() == "finished"
