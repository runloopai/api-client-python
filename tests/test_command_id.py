"""Tests for command_id default generation in execute / execute_and_await_completion.

Verifies that each call generates a fresh UUIDv7 rather than reusing a frozen
default (the bug fixed in this change).
"""

from __future__ import annotations

import json
from typing import cast

import httpx
import pytest
from respx import Route, MockRouter

from runloop_api_client import Runloop, AsyncRunloop

base_url = "http://127.0.0.1:4010"
EXECUTE_PATH = "/v1/devboxes/dbx_test/execute"

STUB_RESPONSE = {
    "execution_id": "exec_1",
    "command_id": "ignored",
    "devbox_id": "dbx_test",
    "status": "completed",
    "exit_status": 0,
    "stdout": "",
    "stderr": "",
}


def _get_command_ids(route: Route) -> list[str]:
    return [
        json.loads(cast(bytes, call.request.content))["command_id"]  # type: ignore[union-attr]
        for call in route.calls  # type: ignore[union-attr]
    ]


def _get_request_body(route: Route, index: int = 0) -> dict[str, object]:
    return json.loads(cast(bytes, route.calls[index].request.content))  # type: ignore[union-attr]


class TestCommandIdGeneration:
    """command_id must be a fresh UUIDv7 per call when not explicitly provided."""

    @pytest.mark.respx(base_url=base_url)
    def test_execute_generates_unique_command_ids(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post(EXECUTE_PATH).mock(return_value=httpx.Response(200, json=STUB_RESPONSE))
        client = Runloop(base_url=base_url, bearer_token="test")

        for _ in range(5):
            client.devboxes.execute(id="dbx_test", command="echo hi")

        assert route.call_count == 5
        ids = _get_command_ids(route)
        assert len(set(ids)) == 5, f"command_ids should all be unique, got: {ids}"

    @pytest.mark.respx(base_url=base_url)
    def test_execute_preserves_explicit_command_id(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post(EXECUTE_PATH).mock(return_value=httpx.Response(200, json=STUB_RESPONSE))
        client = Runloop(base_url=base_url, bearer_token="test")

        client.devboxes.execute(id="dbx_test", command="echo hi", command_id="my-custom-id")

        body = _get_request_body(route)
        assert body["command_id"] == "my-custom-id"


class TestAsyncCommandIdGeneration:
    """Async variant: command_id must be a fresh UUIDv7 per call when not explicitly provided."""

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.asyncio
    async def test_execute_generates_unique_command_ids(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post(EXECUTE_PATH).mock(return_value=httpx.Response(200, json=STUB_RESPONSE))
        client = AsyncRunloop(base_url=base_url, bearer_token="test")

        for _ in range(5):
            await client.devboxes.execute(id="dbx_test", command="echo hi")

        assert route.call_count == 5
        ids = _get_command_ids(route)
        assert len(set(ids)) == 5, f"command_ids should all be unique, got: {ids}"

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.asyncio
    async def test_execute_preserves_explicit_command_id(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post(EXECUTE_PATH).mock(return_value=httpx.Response(200, json=STUB_RESPONSE))
        client = AsyncRunloop(base_url=base_url, bearer_token="test")

        await client.devboxes.execute(id="dbx_test", command="echo hi", command_id="my-custom-id")

        body = _get_request_body(route)
        assert body["command_id"] == "my-custom-id"
