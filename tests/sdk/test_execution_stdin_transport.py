"""Stdin wrappers use generated routing and preserve request configuration."""

from __future__ import annotations

import json

import httpx
import pytest

from runloop_api_client import RunloopError
from runloop_api_client.sdk import Execution, RunloopSDK, AsyncExecution, AsyncRunloopSDK
from runloop_api_client.types import DevboxAsyncExecutionDetailView


class StdinTransport:
    def __init__(self, success: bool) -> None:
        self.success = success
        self.bodies: list[object] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/devboxes/dbx_test/executions/execution_test/send_std_in"
        assert request.headers["x-request-id"] == "synthetic-idempotency-key"
        assert request.headers["x-probe"] == "probe"
        assert request.extensions["timeout"]["read"] == 12
        self.bodies.append(json.loads(request.content))
        return httpx.Response(
            200, json={"devbox_id": "dbx_test", "execution_id": "execution_test", "success": self.success}
        )


@pytest.mark.parametrize("success", [True, False])
def test_stdin_generated_routing_and_unsuccessful_delivery(success: bool) -> None:
    transport = StdinTransport(success)
    with RunloopSDK(
        bearer_token="synthetic",
        base_url="https://api.invalid",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(transport)),
    ) as sdk:
        execution = Execution(
            sdk.api, "dbx_test", DevboxAsyncExecutionDetailView.model_construct(execution_id="execution_test")
        )
        for operation in [
            lambda: execution.send_std_in(
                "hello\n", extra_headers={"x-probe": "probe"}, idempotency_key="synthetic-idempotency-key", timeout=12
            ),
            lambda: execution.close_std_in(
                extra_headers={"x-probe": "probe"}, idempotency_key="synthetic-idempotency-key", timeout=12
            ),
        ]:
            if success:
                assert operation() is None
            else:
                with pytest.raises(RunloopError, match="Failed to send stdin"):
                    operation()
    assert transport.bodies == [{"text": "hello\n"}, {"signal": "EOF"}]


@pytest.mark.parametrize("success", [True, False])
@pytest.mark.asyncio
async def test_async_stdin_generated_routing_and_unsuccessful_delivery(success: bool) -> None:
    transport = StdinTransport(success)
    async with AsyncRunloopSDK(
        bearer_token="synthetic",
        base_url="https://api.invalid",
        max_retries=0,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(transport)),
    ) as sdk:
        execution = AsyncExecution(
            sdk.api, "dbx_test", DevboxAsyncExecutionDetailView.model_construct(execution_id="execution_test")
        )
        for operation in [
            lambda: execution.send_std_in(
                "hello\n", extra_headers={"x-probe": "probe"}, idempotency_key="synthetic-idempotency-key", timeout=12
            ),
            lambda: execution.close_std_in(
                extra_headers={"x-probe": "probe"}, idempotency_key="synthetic-idempotency-key", timeout=12
            ),
        ]:
            if success:
                assert await operation() is None
            else:
                with pytest.raises(RunloopError, match="Failed to send stdin"):
                    await operation()
    assert transport.bodies == [{"text": "hello\n"}, {"signal": "EOF"}]
