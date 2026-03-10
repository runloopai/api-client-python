"""Tests for command_id default generation in execute / execute_and_await_completion.

Verifies that each call generates a fresh UUIDv7 rather than reusing a frozen
default (the bug fixed in this change).
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from runloop_api_client import AsyncRunloop, Runloop

BASE = "http://localhost"
EXECUTE_PATTERN = f"{BASE}/v1/devboxes/dbx_test/execute"

STUB_RESPONSE = {
    "execution_id": "exec_1",
    "command_id": "ignored",
    "devbox_id": "dbx_test",
    "status": "completed",
    "exit_status": 0,
    "stdout": "",
    "stderr": "",
}


class TestCommandIdUniqueness:
    """Every call without an explicit command_id must produce a distinct UUID."""

    @respx.mock
    def test_sync_execute_generates_unique_ids(self) -> None:
        route = respx.post(EXECUTE_PATTERN).mock(
            return_value=httpx.Response(200, json=STUB_RESPONSE)
        )
        client = Runloop(base_url=BASE, bearer_token="test")

        for _ in range(5):
            client.devboxes.execute(id="dbx_test", command="echo hi")

        assert route.call_count == 5
        ids = [json.loads(call.request.content)["command_id"] for call in route.calls]
        assert len(set(ids)) == 5, f"All command_ids should be unique, got: {ids}"

    @respx.mock
    def test_sync_execute_respects_explicit_id(self) -> None:
        route = respx.post(EXECUTE_PATTERN).mock(
            return_value=httpx.Response(200, json=STUB_RESPONSE)
        )
        client = Runloop(base_url=BASE, bearer_token="test")

        client.devboxes.execute(id="dbx_test", command="echo hi", command_id="my-custom-id")

        body = json.loads(route.calls[0].request.content)
        assert body["command_id"] == "my-custom-id"

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_execute_generates_unique_ids(self) -> None:
        route = respx.post(EXECUTE_PATTERN).mock(
            return_value=httpx.Response(200, json=STUB_RESPONSE)
        )
        client = AsyncRunloop(base_url=BASE, bearer_token="test")

        for _ in range(5):
            await client.devboxes.execute(id="dbx_test", command="echo hi")

        assert route.call_count == 5
        ids = [json.loads(call.request.content)["command_id"] for call in route.calls]
        assert len(set(ids)) == 5, f"All command_ids should be unique, got: {ids}"

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_execute_respects_explicit_id(self) -> None:
        route = respx.post(EXECUTE_PATTERN).mock(
            return_value=httpx.Response(200, json=STUB_RESPONSE)
        )
        client = AsyncRunloop(base_url=BASE, bearer_token="test")

        await client.devboxes.execute(id="dbx_test", command="echo hi", command_id="my-custom-id")

        body = json.loads(route.calls[0].request.content)
        assert body["command_id"] == "my-custom-id"
