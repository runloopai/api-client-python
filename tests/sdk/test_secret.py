"""HTTP routing and request forwarding that lifecycle smoke tests cannot observe."""

from __future__ import annotations

import json

import httpx
import pytest

from runloop_api_client import NotFoundError
from runloop_api_client.sdk import RunloopSDK, SecretById


@pytest.mark.parametrize(
    "operation, suffix, method", [("get_info", "", "GET"), ("update", "/update", "POST"), ("delete", "/delete", "POST")]
)
def test_id_request_forwards_options_without_name_fallback(operation: str, suffix: str, method: str) -> None:
    requests: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(404, json={"message": "Secret not found"})

    with RunloopSDK(
        bearer_token="synthetic",
        base_url="https://sdk.invalid",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(respond)),
    ) as sdk:
        exact = sdk.secret.from_id("sec_missing")
        assert isinstance(exact, SecretById)
        assert not requests
        with pytest.raises(NotFoundError):
            if operation == "get_info":
                exact.get_info(extra_headers={"x-probe": "probe"})
            elif operation == "update":
                exact.update("synthetic", extra_headers={"x-probe": "probe"}, idempotency_key="probe")
            else:
                exact.delete(extra_headers={"x-probe": "probe"}, idempotency_key="probe")
        assert len(requests) == 1  # No fallback request to a name route.
        request = requests[0]
        assert (request.method, request.url.path) == (method, f"/v1/secrets/id/sec_missing{suffix}")
        assert request.headers["x-probe"] == "probe"
        if operation != "get_info":
            assert request.headers["x-request-id"] == "probe"
        if operation == "update":
            assert json.loads(request.content) == {"value": "synthetic"}
