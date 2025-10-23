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
_snapshot_id = None


@pytest.mark.timeout(30)
def test_snapshot_devbox(client: Runloop) -> None:
    global _devbox_id, _snapshot_id
    created = client.devboxes.create_and_await_running(
        name=unique_name("snap-devbox"),
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    _devbox_id = created.id

    snap = client.devboxes.snapshot_disk(_devbox_id, name=unique_name("snap"))
    assert snap.id
    _snapshot_id = snap.id


@pytest.mark.timeout(120)
def test_launch_devbox_from_snapshot(client: Runloop) -> None:
    assert _snapshot_id
    launched = None
    try:
        launched = client.devboxes.create_and_await_running(
            snapshot_id=_snapshot_id,
            polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
        )
        assert launched.snapshot_id == _snapshot_id
    finally:
        if launched:
            client.devboxes.shutdown(launched.id)
