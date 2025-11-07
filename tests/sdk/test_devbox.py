from __future__ import annotations

from types import SimpleNamespace
from typing import List

import pytest

from runloop_api_client import RunloopSDK
from runloop_api_client.sdk import Devbox, Execution, ExecutionResult


@pytest.fixture()
def sdk() -> RunloopSDK:
    return RunloopSDK(bearer_token="test-token")


def test_create_returns_devbox(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    devboxes_resource = sdk.api.devboxes

    captured_kwargs: dict[str, object] = {}

    def fake_create_and_await_running(**kwargs):
        captured_kwargs.update(kwargs)
        return SimpleNamespace(id="dev_123")

    monkeypatch.setattr(devboxes_resource, "create_and_await_running", fake_create_and_await_running)

    devbox = sdk.devbox.create(name="my-devbox")

    assert isinstance(devbox, Devbox)
    assert devbox.id == "dev_123"
    assert captured_kwargs["name"] == "my-devbox"


def test_context_manager_shuts_down(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    devboxes_resource = sdk.api.devboxes
    shutdown_calls: List[str] = []

    def fake_shutdown(devbox_id: str, **_kwargs):
        shutdown_calls.append(devbox_id)
        return None

    monkeypatch.setattr(devboxes_resource, "shutdown", fake_shutdown)

    with sdk.devbox.from_id("dev_ctx") as devbox:
        assert devbox.id == "dev_ctx"

    assert shutdown_calls == ["dev_ctx"]


def test_exec_without_streaming(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    devboxes_resource = sdk.api.devboxes

    result = SimpleNamespace(
        execution_id="exec-1",
        devbox_id="dev_456",
        stdout="hello",
        stderr="",
        exit_status=0,
        status="completed",
    )

    def fake_execute_and_await_completion(devbox_id: str, **kwargs):
        assert devbox_id == "dev_456"
        assert kwargs["command"] == "echo hello"
        return result

    monkeypatch.setattr(devboxes_resource, "execute_and_await_completion", fake_execute_and_await_completion)

    devbox = sdk.devbox.from_id("dev_456")
    execution_result = devbox.cmd.exec("echo hello")

    assert isinstance(execution_result, ExecutionResult)
    assert execution_result.exit_code == 0
    assert execution_result.stdout() == "hello"


def test_exec_with_streaming_callbacks(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    devboxes_resource = sdk.api.devboxes
    executions_resource = devboxes_resource.executions

    execution = SimpleNamespace(
        execution_id="exec-stream",
        devbox_id="dev_stream",
        stdout="",
        stderr="",
        exit_status=None,
        status="running",
    )

    final = SimpleNamespace(
        execution_id="exec-stream",
        devbox_id="dev_stream",
        stdout="done",
        stderr="",
        exit_status=0,
        status="completed",
    )

    def fake_execute_async(devbox_id: str, **kwargs):
        assert kwargs["command"] == "long task"
        assert devbox_id == "dev_stream"
        return execution

    def fake_await_completed(execution_id: str, devbox_id: str, **_kwargs):
        assert execution_id == "exec-stream"
        assert devbox_id == "dev_stream"
        return final

    class DummyStream:
        def __init__(self, values: list[str]):
            self._values = values

        def __iter__(self):
            for value in self._values:
                yield SimpleNamespace(output=value)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(devboxes_resource, "execute_async", fake_execute_async)
    monkeypatch.setattr(executions_resource, "await_completed", fake_await_completed)
    monkeypatch.setattr(
        executions_resource,
        "stream_stdout_updates",
        lambda execution_id, *, devbox_id: DummyStream(["line 1", "line 2"]),
    )
    monkeypatch.setattr(
        executions_resource,
        "stream_stderr_updates",
        lambda execution_id, *, devbox_id: DummyStream([]),
    )

    stdout_logs: list[str] = []
    combined_logs: list[str] = []

    devbox = sdk.devbox.from_id("dev_stream")
    result = devbox.cmd.exec(
        "long task",
        stdout=stdout_logs.append,
        output=combined_logs.append,
    )

    assert stdout_logs == ["line 1", "line 2"]
    assert combined_logs == ["line 1", "line 2"]
    assert result.exit_code == 0
    assert result.stdout() == "done"


def test_exec_async_returns_execution(monkeypatch: pytest.MonkeyPatch, sdk: RunloopSDK) -> None:
    devboxes_resource = sdk.api.devboxes
    executions_resource = devboxes_resource.executions

    execution = SimpleNamespace(
        execution_id="exec-async",
        devbox_id="dev_async",
        stdout="",
        stderr="",
        exit_status=None,
        status="running",
    )

    final = SimpleNamespace(
        execution_id="exec-async",
        devbox_id="dev_async",
        stdout="async complete",
        stderr="",
        exit_status=0,
        status="completed",
    )

    monkeypatch.setattr(devboxes_resource, "execute_async", lambda devbox_id, **kwargs: execution)
    monkeypatch.setattr(
        executions_resource,
        "await_completed",
        lambda execution_id, *, devbox_id, **kwargs: final,
    )

    class EmptyStream:
        def __iter__(self):
            return iter(())

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(
        executions_resource,
        "stream_stdout_updates",
        lambda execution_id, *, devbox_id: EmptyStream(),
    )
    monkeypatch.setattr(
        executions_resource,
        "stream_stderr_updates",
        lambda execution_id, *, devbox_id: EmptyStream(),
    )

    devbox = sdk.devbox.from_id("dev_async")
    execution_obj = devbox.cmd.exec_async("background task")

    assert isinstance(execution_obj, Execution)
    result = execution_obj.result()
    assert result.stdout() == "async complete"
