from __future__ import annotations

from typing import Iterator

import pytest

from runloop_api_client import Runloop
from runloop_api_client.lib.polling import PollingConfig

from .utils import unique_name

pytestmark = [pytest.mark.smoketest]


@pytest.fixture(autouse=True, scope="module")
def _cleanup(client: Runloop) -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    yield
    global _devbox_id
    if _devbox_id:
        try:
            client.devboxes.shutdown(_devbox_id)
        except Exception:
            pass


"""
Tests are run sequentially and can be dependent on each other. 
This is to avoid overloading resources and save efficiency.
"""
_devbox_id = None
_exec_id = None


@pytest.mark.timeout(30)
def test_launch_devbox(client: Runloop) -> None:
    global _devbox_id
    created = client.devboxes.create_and_await_running(
        name=unique_name("exec-devbox"),
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    _devbox_id = created.id


@pytest.mark.timeout(30)
def test_execute_async_and_await_completion(client: Runloop) -> None:
    assert _devbox_id
    global _exec_id
    started = client.devboxes.executions.execute_async(_devbox_id, command="echo hello && sleep 1")
    _exec_id = started.execution_id
    completed = client.devboxes.executions.await_completed(
        _exec_id,
        devbox_id=_devbox_id,
        polling_config=PollingConfig(max_attempts=120, interval_seconds=2.0, timeout_seconds=10 * 60),
    )
    assert completed.status == "completed"


@pytest.mark.timeout(30)
def test_tail_stdout_logs(client: Runloop) -> None:
    assert _devbox_id and _exec_id
    stream = client.devboxes.executions.stream_stdout_updates(execution_id=_exec_id, devbox_id=_devbox_id)
    received = ""
    for chunk in stream:
        received += getattr(chunk, "output", "") or ""
        if received:
            break
    assert isinstance(received, str)


@pytest.mark.timeout(30)
def test_execute_and_await_completion(client: Runloop) -> None:
    assert _devbox_id
    completed = client.devboxes.execute_and_await_completion(
        _devbox_id,
        command="echo hello && sleep 1",
        polling_config=PollingConfig(max_attempts=120, interval_seconds=2.0, timeout_seconds=10 * 60),
    )
    assert completed.status == "completed"


# @pytest.mark.timeout(90)
# def test_execute_and_await_completion_long_running(client: Runloop) -> None:
#     assert _devbox_id
#     completed = client.devboxes.execute_and_await_completion(
#         _devbox_id,
#         command="echo hello && sleep 70",
#         polling_config=PollingConfig(max_attempts=120, interval_seconds=2.0),
#     )
#     assert completed.status == "completed"


# TODO: Uncomment this test when we fix timeouts for polling
# @pytest.mark.timeout(30)
# def test_execute_and_await_completion_timeout() -> None:
#     assert _devbox_id
#     with pytest.raises(PollingTimeout):
#         client.devboxes.execute_and_await_completion(
#             devbox_id=_devbox_id,
#             command="echo hello && sleep 10",
#             polling_config=PollingConfig(max_attempts=1, interval_seconds=2.0, timeout_seconds=3),
#         )
