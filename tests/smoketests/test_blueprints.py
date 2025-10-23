from __future__ import annotations

import os
from typing import Iterator

import pytest

from runloop_api_client import Runloop
from runloop_api_client.lib.polling import PollingConfig

from .utils import unique_name

pytestmark = [pytest.mark.smoketest]


@pytest.fixture(autouse=True, scope="module")
def _cleanup(client: Runloop) -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    yield
    global _blueprint_id
    if _blueprint_id:
        try:
            client.blueprints.delete(_blueprint_id)
        except Exception:
            pass


"""
Tests are run sequentially and can be dependent on each other. 
This is to avoid overloading resources and save efficiency.
"""
_blueprint_id = None
_blueprint_name = unique_name("bp")


@pytest.mark.timeout(120)  # 2 minutes
def test_create_blueprint_and_await_build(client: Runloop) -> None:
    global _blueprint_id
    created = client.blueprints.create_and_await_build_complete(
        name=_blueprint_name,
        polling_config=PollingConfig(max_attempts=180, interval_seconds=5.0, timeout_seconds=30 * 60),
    )
    assert created.status == "build_complete"
    _blueprint_id = created.id


@pytest.mark.timeout(120)
def test_start_devbox_from_base_blueprint_by_id(client: Runloop) -> None:
    assert _blueprint_id
    devbox = None
    try:
        devbox = client.devboxes.create_and_await_running(
            blueprint_id=_blueprint_id,
            polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
        )
        assert devbox.blueprint_id == _blueprint_id
        assert devbox.status == "running"
    finally:
        if devbox:
            client.devboxes.shutdown(devbox.id)


@pytest.mark.timeout(120)
def test_start_devbox_from_base_blueprint_by_name(client: Runloop) -> None:
    devbox = None
    try:
        devbox = client.devboxes.create_and_await_running(
            blueprint_name=_blueprint_name,
            polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
        )
        assert devbox.blueprint_id
        assert devbox.status == "running"
    finally:
        if devbox:
            client.devboxes.shutdown(devbox.id)


@pytest.mark.timeout(120)
@pytest.mark.skipif(
    os.getenv("RUN_SMOKETESTS") != "1",
    reason="Skip blueprint secrets test in local testing (requires RUN_SMOKETESTS=1)",
)
def test_create_blueprint_with_secret_and_await_build(client: Runloop) -> None:
    bpt = None
    try:
        bpt = client.blueprints.create(
            name=unique_name("bp-secrets"),
            dockerfile=(
                "FROM runloop:runloop/starter-arm64\n"
                "ARG GITHUB_TOKEN\n"
                'RUN git config --global credential.helper \'!f() { echo "username=x-access-token"; echo "password=$GITHUB_TOKEN"; }; f\' '
                "&& git clone https://github.com/runloopai/runloop-fe.git /workspace/runloop-fe "
                "&& git config --global --unset credential.helper\n"
                "WORKDIR /workspace/runloop-fe"
            ),
            secrets={"GITHUB_TOKEN": "GITHUB_TOKEN_FOR_SMOKETESTS"},
        )

        completed = client.blueprints.await_build_complete(
            bpt.id,
            polling_config=PollingConfig(max_attempts=180, interval_seconds=5.0, timeout_seconds=30 * 60),
        )
        assert completed.status == "build_complete"
        assert completed.parameters.secrets is not None
        assert completed.parameters.secrets.get("GITHUB_TOKEN") == "GITHUB_TOKEN_FOR_SMOKETESTS"
    finally:
        if bpt:
            client.blueprints.delete(bpt.id)
