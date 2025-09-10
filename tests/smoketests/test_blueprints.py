import pytest

from runloop_api_client.lib.polling import PollingConfig

from .utils import make_client, unique_name

pytestmark = [pytest.mark.smoketest]


client = make_client()


"""
Tests are run sequentially and can be dependent on each other. 
This is to avoid overloading resources and save efficiency.
"""
_blueprint_id = None
_blueprint_name = unique_name("bp")


def teardown_module() -> None:
    global _blueprint_id
    if _blueprint_id:
        try:
            client.blueprints.delete(_blueprint_id)
        except Exception:
            pass


@pytest.mark.timeout(30)
def test_create_blueprint_and_await_build() -> None:
    global _blueprint_id
    created = client.blueprints.create_and_await_build_complete(
        name=_blueprint_name,
        polling_config=PollingConfig(max_attempts=180, interval_seconds=5.0, timeout_seconds=30 * 60),
    )
    assert created.status == "build_complete"
    _blueprint_id = created.id


@pytest.mark.timeout(30)
def test_start_devbox_from_base_blueprint_by_id() -> None:
    assert _blueprint_id
    devbox = client.devboxes.create_and_await_running(
        blueprint_id=_blueprint_id,
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    assert devbox.blueprint_id == _blueprint_id
    assert devbox.status == "running"
    client.devboxes.shutdown(devbox.id)


@pytest.mark.timeout(30)
def test_start_devbox_from_base_blueprint_by_name() -> None:
    devbox = client.devboxes.create_and_await_running(
        blueprint_name=_blueprint_name,
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    assert devbox.blueprint_id
    assert devbox.status == "running"
    client.devboxes.shutdown(devbox.id)
