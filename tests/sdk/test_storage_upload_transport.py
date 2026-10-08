"""Signed storage HTTP contract, independent of cloud credentials."""

from __future__ import annotations

import json
from typing import Any, Generator
from typing_extensions import override

import httpx
import pytest

from runloop_api_client.sdk import RunloopSDK, AsyncRunloopSDK


class StorageTransport:
    def __init__(self, headers: dict[str, str] | None, status: int = 200, *, binary: bool = False) -> None:
        self.headers = headers
        self.status = status
        self.binary = binary
        self.uploads: list[httpx.Request] = []
        self.completions = 0

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.host == "storage.invalid":
            self.uploads.append(request)
            assert request.method == "PUT"
            assert request.content == b"hello"
            assert request.headers.get("x-ms-blob-type") == (self.headers or {}).get("x-ms-blob-type")
            assert not {"authorization", "cookie", "x-api-default", "x-api-option"}.intersection(request.headers)
            return httpx.Response(
                self.status, text="synthetic-storage-secret", headers={"location": "https://elsewhere.invalid"}
            )
        assert request.headers["authorization"] == "Bearer synthetic-api-secret"
        if request.url.path.endswith("/complete"):
            self.completions += 1
        else:
            assert request.headers["x-api-option"] == "api-only"
            body = json.loads(request.content)
            assert body["name"] == "upload"
            assert body["content_type"] == ("binary" if self.binary else "text")
            assert body["metadata"] == {"key": "value"}
            assert body.get("ttl_ms") is None
        data: dict[str, Any] = {
            "id": "obj_upload",
            "upload_url": "https://storage.invalid/blob?sig=synthetic-signed-secret",
        }
        if self.headers is not None:
            data["upload_headers"] = self.headers
        return httpx.Response(200, json=data)


class APIOnlyAuth(httpx.Auth):
    @override
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        assert request.url.host == "api.invalid", "Client authentication must not run for signed storage requests"
        yield request


@pytest.mark.parametrize("headers", [None, {}, {"x-ms-blob-type": "BlockBlob"}])
@pytest.mark.parametrize("binary", [False, True], ids=["text", "bytes"])
def test_signed_upload_lifecycle(headers: dict[str, str] | None, binary: bool) -> None:
    transport = StorageTransport(headers, binary=binary)
    with RunloopSDK(
        bearer_token="synthetic-api-secret",
        base_url="https://api.invalid",
        max_retries=0,
        http_client=httpx.Client(
            transport=httpx.MockTransport(transport),
            headers={"x-api-default": "private", "Authorization": "Bearer private-default"},
            cookies={"session": "private"},
            auth=APIOnlyAuth(),
            follow_redirects=True,
        ),
    ) as sdk:
        if binary:
            obj = sdk.storage_object.upload_from_bytes(
                b"hello",
                name="upload",
                content_type="binary",
                metadata={"key": "value"},
                extra_headers={"x-api-option": "api-only"},
            )
        else:
            obj = sdk.storage_object.upload_from_text(
                "hello",
                name="upload",
                metadata={"key": "value"},
                extra_headers={"x-api-option": "api-only"},
            )
        assert obj.id == "obj_upload"
        assert obj.upload_url is None
    assert len(transport.uploads) == transport.completions == 1


@pytest.mark.parametrize("headers", [None, {}, {"x-ms-blob-type": "BlockBlob"}])
@pytest.mark.parametrize("binary", [False, True], ids=["text", "bytes"])
@pytest.mark.asyncio
async def test_async_signed_upload_lifecycle(headers: dict[str, str] | None, binary: bool) -> None:
    transport = StorageTransport(headers, binary=binary)
    async with AsyncRunloopSDK(
        bearer_token="synthetic-api-secret",
        base_url="https://api.invalid",
        max_retries=0,
        http_client=httpx.AsyncClient(
            transport=httpx.MockTransport(transport),
            headers={"x-api-default": "private", "Authorization": "Bearer private-default"},
            cookies={"session": "private"},
            auth=APIOnlyAuth(),
            follow_redirects=True,
        ),
    ) as sdk:
        if binary:
            obj = await sdk.storage_object.upload_from_bytes(
                b"hello",
                name="upload",
                content_type="binary",
                metadata={"key": "value"},
                extra_headers={"x-api-option": "api-only"},
            )
        else:
            obj = await sdk.storage_object.upload_from_text(
                "hello",
                name="upload",
                metadata={"key": "value"},
                extra_headers={"x-api-option": "api-only"},
            )
        assert obj.id == "obj_upload"
        assert obj.upload_url is None
    assert len(transport.uploads) == transport.completions == 1


@pytest.mark.parametrize("status", [307, 403, 500])
def test_failed_upload_does_not_complete_retry_redirect_or_expose_credentials(status: int) -> None:
    transport = StorageTransport({"x-ms-blob-type": "BlockBlob"}, status)
    with RunloopSDK(
        bearer_token="synthetic-api-secret",
        base_url="https://api.invalid",
        max_retries=2,
        http_client=httpx.Client(transport=httpx.MockTransport(transport), follow_redirects=True),
    ) as sdk:
        with pytest.raises(httpx.HTTPStatusError) as error:
            sdk.storage_object.upload_from_text(
                "hello", name="upload", metadata={"key": "value"}, extra_headers={"x-api-option": "api-only"}
            )
    assert str(status) in str(error.value)
    assert "synthetic" not in str(error.value)
    assert len(transport.uploads) == 1
    assert transport.completions == 0


def test_upload_instructions_are_copied_per_object() -> None:
    from runloop_api_client.sdk import StorageObject

    requests: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    headers = {"x-upload-object": "first"}
    with RunloopSDK(bearer_token="synthetic", http_client=httpx.Client(transport=httpx.MockTransport(respond))) as sdk:
        first = StorageObject(sdk.api, "first", "https://storage.invalid/first", headers)
        headers["x-upload-object"] = "second"
        second = StorageObject(sdk.api, "second", "https://storage.invalid/second", headers)
        headers.clear()
        first.upload_content(iter([b"one", b"two"]))
        second.upload_content(b"three")
    assert [(r.url.path, r.headers["x-upload-object"], r.content) for r in requests] == [
        ("/first", "first", b"onetwo"),
        ("/second", "second", b"three"),
    ]


@pytest.mark.asyncio
async def test_async_distinct_uploads_keep_independent_credentials() -> None:
    import asyncio

    from runloop_api_client.sdk import AsyncStorageObject

    requests: list[httpx.Request] = []
    both_started = asyncio.Event()

    async def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 2:
            both_started.set()
        await both_started.wait()
        return httpx.Response(200)

    headers = {"x-upload-object": "first"}
    async with AsyncRunloopSDK(
        bearer_token="synthetic", http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))
    ) as sdk:
        first = AsyncStorageObject(sdk.api, "first", "https://storage.invalid/first", headers)
        headers["x-upload-object"] = "second"
        second = AsyncStorageObject(sdk.api, "second", "https://storage.invalid/second", headers)
        headers.clear()
        await asyncio.wait_for(
            asyncio.gather(first.upload_content("first"), second.upload_content("second")), timeout=10
        )
    assert len(requests) == 2
    for request in requests:
        assert request.url.path == "/" + request.headers["x-upload-object"]
        assert request.content.decode() == request.headers["x-upload-object"]
