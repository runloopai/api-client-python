"""Tests for dedicated HTTP/1.1 transfer pool used by upload/download."""

from __future__ import annotations

import os
from typing import Any, Iterator

import httpx
import pytest

import runloop_api_client._base_client as _base_mod
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client._base_client import _is_file_transfer_path

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"


@pytest.fixture(autouse=True)
def _reset_shared_pool() -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    _clear_pool_state()
    yield
    _clear_pool_state()


def _clear_pool_state() -> None:
    with _base_mod._pool_lock:
        old_sync = _base_mod._shared_sync_transport
        old_sync_transfer = _base_mod._shared_sync_transfer_transport
        _base_mod._shared_sync_transport = None
        _base_mod._shared_sync_transfer_transport = None
        _base_mod._shared_async_transports.clear()
        _base_mod._shared_async_transfer_transports.clear()
    for transport in (old_sync, old_sync_transfer):
        if transport is not None:
            try:
                transport._transport.close()
            except Exception:
                pass


def _make_client(**kwargs: Any) -> Runloop:
    kwargs.setdefault("base_url", base_url)
    kwargs.setdefault("bearer_token", bearer_token)
    return Runloop(**kwargs)


def test_is_file_transfer_path() -> None:
    assert _is_file_transfer_path("/v1/devboxes/dbx_1/upload_file") is True
    assert _is_file_transfer_path("/v1/devboxes/dbx_1/download_file") is True
    assert _is_file_transfer_path("/v1/devboxes") is False
    assert _is_file_transfer_path("/v1/objects/obj_1/download") is False
    assert _is_file_transfer_path("/v1/scenarios/runs/run_1/download_logs") is False


def test_transfer_client_is_http1_and_separate_from_api_pool() -> None:
    client = _make_client(shared_http_pool=True)
    try:
        assert client._isolate_file_transfers is True
        assert client._transfer_client is None

        api_request = httpx.Request("POST", f"{base_url}/v1/devboxes")
        transfer_request = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/upload_file")

        assert client._send_client_for_request(api_request) is client._client

        transfer = client._send_client_for_request(transfer_request)
        assert transfer is not client._client
        assert transfer is client._transfer_client

        api_transport = client._client._transport  # type: ignore[attr-defined]
        transfer_transport = transfer._transport  # type: ignore[attr-defined]
        assert api_transport is not transfer_transport
        assert _base_mod._shared_sync_transfer_transport is transfer_transport
        # Real httpx transport under the shared wrapper is HTTP/1.1-only.
        inner = transfer_transport._transport
        assert getattr(inner, "_http2", False) is False
    finally:
        client.close()


def test_transfer_pool_is_shared_across_sdk_clients() -> None:
    c1 = _make_client(shared_http_pool=True)
    c2 = _make_client(shared_http_pool=True)
    try:
        req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/download_file")
        t1 = c1._send_client_for_request(req)
        t2 = c2._send_client_for_request(req)
        assert t1 is not t2
        assert t1._transport is t2._transport  # type: ignore[attr-defined]
        assert _base_mod._shared_sync_transfer_transport is not None
        assert _base_mod._shared_sync_transfer_transport.refcount == 2
    finally:
        c1.close()
        c2.close()
    assert _base_mod._shared_sync_transfer_transport is not None
    assert _base_mod._shared_sync_transfer_transport.refcount == 0


def test_custom_http_client_skips_transfer_isolation() -> None:
    custom = httpx.Client()
    client = _make_client(http_client=custom)
    try:
        assert client._isolate_file_transfers is False
        req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/upload_file")
        assert client._send_client_for_request(req) is custom
        assert client._transfer_client is None
    finally:
        client.close()
        custom.close()


def test_private_pool_still_isolates_transfers() -> None:
    client = _make_client(shared_http_pool=False)
    try:
        req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/upload_file")
        transfer = client._send_client_for_request(req)
        assert transfer is not client._client
        assert client._uses_shared_pool is False
    finally:
        client.close()


@pytest.mark.asyncio
async def test_async_transfer_client_is_separate() -> None:
    client = AsyncRunloop(base_url=base_url, bearer_token=bearer_token, shared_http_pool=True)
    try:
        req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/upload_file")
        transfer = client._send_client_for_request(req)
        assert transfer is not client._client
        assert client._transfer_client is transfer
    finally:
        await client.close()
