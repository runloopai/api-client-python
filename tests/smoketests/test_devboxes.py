from __future__ import annotations

from typing import Iterator

import pytest

from runloop_api_client import Runloop
from runloop_api_client.lib.polling import PollingConfig, PollingTimeout

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


@pytest.mark.timeout(30)
def test_create_devbox(client: Runloop) -> None:
    created = client.devboxes.create(name=unique_name("smoke-devbox"))
    assert created.id
    client.devboxes.shutdown(created.id)


@pytest.mark.timeout(120)
def test_await_running_create_and_await_running(client: Runloop) -> None:
    global _devbox_id
    created = client.devboxes.create_and_await_running(
        name=unique_name("smoketest-devbox2"),
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    assert created.status == "running"
    _devbox_id = created.id


def test_list_devboxes(client: Runloop) -> None:
    page = client.devboxes.list(limit=10)
    assert isinstance(page.devboxes, list)
    assert len(page.devboxes) > 0


def test_retrieve_devbox(client: Runloop) -> None:
    assert _devbox_id
    view = client.devboxes.retrieve(_devbox_id)
    assert view.id == _devbox_id


def test_shutdown_devbox(client: Runloop) -> None:
    assert _devbox_id
    view = client.devboxes.shutdown(_devbox_id)
    assert view.id == _devbox_id
    assert view.status == "shutdown"


@pytest.mark.timeout(120)
def test_create_and_await_running_long_set_up(client: Runloop) -> None:
    created = client.devboxes.create_and_await_running(
        name=unique_name("smoketest-devbox-await-running-long-set-up"),
        launch_parameters={"launch_commands": ["sleep 70"]},
        polling_config=PollingConfig(interval_seconds=5.0, timeout_seconds=80),
    )
    assert created.status == "running"
    client.devboxes.shutdown(created.id)


@pytest.mark.timeout(30)
def test_create_and_await_running_timeout(client: Runloop) -> None:
    with pytest.raises(PollingTimeout):
        client.devboxes.create_and_await_running(
            name=unique_name("smoketest-devbox-await-running-timeout"),
            launch_parameters={"launch_commands": ["sleep 70"]},
            polling_config=PollingConfig(max_attempts=1, interval_seconds=0.1),
        )


@pytest.mark.timeout(120)
def test_await_suspended(client: Runloop) -> None:
    """Test await_suspended: create devbox, wait for running, suspend, then await suspended"""
    created = client.devboxes.create_and_await_running(
        name=unique_name("smoketest-devbox-await-suspended"),
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    assert created.status == "running"

    # Suspend the devbox
    suspended = client.devboxes.suspend(created.id)
    assert suspended.id == created.id

    # Wait for suspended state
    result = client.devboxes.await_suspended(
        created.id,
        polling_config=PollingConfig(max_attempts=60, interval_seconds=2.0, timeout_seconds=5 * 60),
    )
    assert result.status == "suspended"
    assert result.id == created.id

    # Cleanup
    client.devboxes.shutdown(created.id)
