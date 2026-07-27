"""Tests for sharded H2 background + transfer bulkhead pools."""

from __future__ import annotations

import os
from typing import Any, Iterator

import httpx
import pytest

import runloop_api_client._base_client as _base_mod
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client._base_client import (
    _is_background_path,
    _is_transfer_path,
    _pool_affinity_key,
    _shard_index,
)

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
        old_bg = list(_base_mod._shared_sync_background_transports.values())
        old_xfer = list(_base_mod._shared_sync_transfer_transports.values())
        _base_mod._shared_sync_transport = None
        _base_mod._shared_sync_background_transports.clear()
        _base_mod._shared_sync_transfer_transports.clear()
        _base_mod._shared_async_transports.clear()
        _base_mod._shared_async_background_transports.clear()
        _base_mod._shared_async_transfer_transports.clear()
    for transport in [old_sync, *old_bg, *old_xfer]:
        if transport is not None:
            try:
                transport._transport.close()
            except Exception:
                pass


def _make_client(**kwargs: Any) -> Runloop:
    kwargs.setdefault("base_url", base_url)
    kwargs.setdefault("bearer_token", bearer_token)
    return Runloop(**kwargs)


def test_path_classification() -> None:
    assert _is_background_path("/v1/devboxes/dbx_1/wait_for_status") is True
    assert _is_background_path("/v1/devboxes/dbx_1/executions/ex_1/wait_for_status") is True
    assert _is_transfer_path("/v1/devboxes/dbx_1/upload_file") is True
    assert _is_transfer_path("/v1/devboxes/dbx_1/download_file") is True
    assert _is_background_path("/v1/devboxes") is False
    assert _is_transfer_path("/v1/objects/obj_1/download") is False


def test_affinity_key_and_shard() -> None:
    assert _pool_affinity_key("/v1/devboxes/dbx_1/upload_file") == "dbx_1"
    assert _pool_affinity_key("/v1/devboxes/dbx_1/wait_for_status") == "dbx_1"
    assert _pool_affinity_key("/v1/devboxes/dbx_1/executions/ex_9/wait_for_status") == "ex_9"
    assert _shard_index("dbx_1", 1) == 0
    assert _shard_index("dbx_1", 2) in (0, 1)
    assert _shard_index("dbx_1", 2) == _shard_index("dbx_1", 2)


def test_api_background_transfer_use_distinct_transports() -> None:
    client = _make_client(shared_http_pool=True, background_pool_shards=2, transfer_pool_shards=2)
    try:
        api_req = httpx.Request("POST", f"{base_url}/v1/devboxes")
        wait_req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_a/wait_for_status")
        upload_req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_a/upload_file")

        api = client._send_client_for_request(api_req)
        wait = client._send_client_for_request(wait_req)
        upload = client._send_client_for_request(upload_req)

        assert api is client._client
        assert wait is not api
        assert upload is not api
        assert wait is not upload
        assert wait._transport is not api._transport  # type: ignore[attr-defined]
        assert upload._transport is not api._transport  # type: ignore[attr-defined]
        assert wait._transport is not upload._transport  # type: ignore[attr-defined]
    finally:
        client.close()


def test_same_resource_affinity_uses_same_shard() -> None:
    client = _make_client(background_pool_shards=2, transfer_pool_shards=2)
    try:
        w1 = client._send_client_for_request(
            httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_same/wait_for_status")
        )
        w2 = client._send_client_for_request(
            httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_same/wait_for_status")
        )
        assert w1 is w2
    finally:
        client.close()


def test_different_resources_can_land_on_different_shards() -> None:
    client = _make_client(background_pool_shards=2)
    try:
        seen: set[int] = set()
        for i in range(40):
            req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_{i}/wait_for_status")
            c = client._send_client_for_request(req)
            seen.add(id(c._transport))  # type: ignore[attr-defined]
        assert len(seen) == 2
        assert len(_base_mod._shared_sync_background_transports) == 2
    finally:
        client.close()


def test_custom_http_client_skips_isolation() -> None:
    custom = httpx.Client()
    client = _make_client(http_client=custom)
    try:
        assert client._isolate_workload_pools is False
        req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/wait_for_status")
        assert client._send_client_for_request(req) is custom
        assert client._background_clients == {}
    finally:
        client.close()
        custom.close()


def test_shards_shared_across_sdk_clients() -> None:
    c1 = _make_client(background_pool_shards=2)
    c2 = _make_client(background_pool_shards=2)
    try:
        req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_shared/wait_for_status")
        t1 = c1._send_client_for_request(req)
        t2 = c2._send_client_for_request(req)
        assert t1 is not t2
        assert t1._transport is t2._transport  # type: ignore[attr-defined]
    finally:
        c1.close()
        c2.close()


@pytest.mark.asyncio
async def test_async_bulkheads() -> None:
    client = AsyncRunloop(
        base_url=base_url,
        bearer_token=bearer_token,
        shared_http_pool=True,
        background_pool_shards=2,
        transfer_pool_shards=2,
    )
    try:
        wait = client._send_client_for_request(
            httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/executions/ex_1/wait_for_status")
        )
        upload = client._send_client_for_request(
            httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_1/upload_file")
        )
        assert wait is not client._client
        assert upload is not client._client
        assert wait is not upload
    finally:
        await client.close()
