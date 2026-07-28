"""Tests for sharded H2 background + transfer bulkhead pools."""

from __future__ import annotations

import os
import re
import threading
from typing import Any, Iterator
from pathlib import Path

import httpx
import pytest

import runloop_api_client._base_client as _base_mod
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client._base_client import (
    _is_transfer_path,
    _is_background_path,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"

# Invariant: every long-lived / bulk-body RPC in the resources tree must match
# these suffixes or it silently shares the API H2 pool. Update both the
# classification helpers and this list when adding endpoints.
_KNOWN_BACKGROUND_PATHS = (
    "/v1/devboxes/dbx_1/wait_for_status",
    "/v1/devboxes/dbx_1/executions/ex_1/wait_for_status",
)
_KNOWN_TRANSFER_PATHS = (
    "/v1/devboxes/dbx_1/upload_file",
    "/v1/devboxes/dbx_1/download_file",
)


@pytest.fixture(autouse=True)
def _reset_shared_pool() -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    _clear_pool_state()
    yield
    _clear_pool_state()


def _clear_pool_state() -> None:
    old = []
    old.extend(_base_mod._shared_sync_api_transports.take_all())
    old.extend(_base_mod._shared_sync_background_transports.take_all())
    old.extend(_base_mod._shared_sync_transfer_transports.take_all())
    _base_mod._shared_async_api_transports.clear()
    _base_mod._shared_async_background_transports.clear()
    _base_mod._shared_async_transfer_transports.clear()
    for transport in old:
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


def test_api_background_transfer_use_distinct_transports() -> None:
    client = _make_client(shared_http_pool=True, api_pool_shards=2, background_pool_shards=2, transfer_pool_shards=2)
    try:
        api_req = httpx.Request("POST", f"{base_url}/v1/devboxes")
        wait_req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_a/wait_for_status")
        upload_req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_a/upload_file")

        api = client._get_client_for_path(api_req.url.path)
        wait = client._get_client_for_path(wait_req.url.path)
        upload = client._get_client_for_path(upload_req.url.path)

        assert wait is not api
        assert upload is not api
        assert wait is not upload
        assert wait._transport is not api._transport  # type: ignore[attr-defined]
        assert upload._transport is not api._transport  # type: ignore[attr-defined]
        assert wait._transport is not upload._transport  # type: ignore[attr-defined]
    finally:
        client.close()


def test_round_robin_spreads_requests_across_shards() -> None:
    client = _make_client(background_pool_shards=2, transfer_pool_shards=2)
    assert client._background_pool is not None and client._transfer_pool is not None
    try:
        wait_req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_same/wait_for_status")
        w0 = client._get_client_for_path(wait_req.url.path)
        w1 = client._get_client_for_path(wait_req.url.path)
        w2 = client._get_client_for_path(wait_req.url.path)
        assert w0 is not w1
        assert w0 is w2
        assert set(client._background_pool._clients) == {0, 1}

        upload_req = httpx.Request("POST", f"{base_url}/v1/devboxes/dbx_same/upload_file")
        t0 = client._get_client_for_path(upload_req.url.path)
        t1 = client._get_client_for_path(upload_req.url.path)
        assert t0 is not t1
        assert set(client._transfer_pool._clients) == {0, 1}
        assert _base_mod._shared_sync_background_transports.shard_ids() == {0, 1}
        assert _base_mod._shared_sync_transfer_transports.shard_ids() == {0, 1}
    finally:
        client.close()


def test_many_clients_first_requests_use_both_shards() -> None:
    clients = [_make_client(background_pool_shards=2) for _ in range(40)]
    try:
        path = "/v1/devboxes/dbx_1/wait_for_status"
        seen_transports = {id(c._get_client_for_path(path)._transport) for c in clients}  # type: ignore[attr-defined]
        assert len(seen_transports) == 2
        assert _base_mod._shared_sync_background_transports.shard_ids() == {0, 1}
    finally:
        for c in clients:
            c.close()


def test_custom_http_client_skips_isolation() -> None:
    custom = httpx.Client()
    client = _make_client(http_client=custom)
    try:
        assert client._isolate_workload_pools is False
        assert client._get_client_for_path("/v1/devboxes/dbx_1/wait_for_status") is custom
        assert client._background_pool is None
    finally:
        client.close()
        custom.close()


def test_round_robin_is_per_client_while_transports_are_shared() -> None:
    c1 = _make_client(background_pool_shards=2)
    c2 = _make_client(background_pool_shards=2)
    assert c1._background_pool is not None and c2._background_pool is not None
    try:
        path = "/v1/devboxes/dbx_shared/wait_for_status"
        start1 = c1._background_pool._next
        start2 = c2._background_pool._next
        t1 = c1._get_client_for_path(path)
        t2 = c2._get_client_for_path(path)
        assert t1 is not t2
        if start1 % 2 == start2 % 2:
            assert t1._transport is t2._transport  # type: ignore[attr-defined]
        else:
            assert t1._transport is not t2._transport  # type: ignore[attr-defined]
        assert c1._background_pool._next == start1 + 1
        assert c2._background_pool._next == start2 + 1

        t1b = c1._get_client_for_path(path)
        assert t1b is not t1
        assert c1._background_pool._next == start1 + 2
        assert c2._background_pool._next == start2 + 1
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
        wait = client._get_client_for_path("/v1/devboxes/dbx_1/executions/ex_1/wait_for_status")
        upload = client._get_client_for_path("/v1/devboxes/dbx_1/upload_file")
        assert wait is not client._client
        assert upload is not client._client
        assert wait is not upload
    finally:
        await client.close()


def test_concurrent_background_client_init_is_singleton() -> None:
    client = _make_client(shared_http_pool=False, background_pool_shards=1)
    assert client._background_pool is not None
    barrier = threading.Barrier(16)
    results: list[httpx.Client] = []
    errors: list[BaseException] = []

    def worker() -> None:
        try:
            barrier.wait()
            results.append(client._background_pool.ensure(0))  # type: ignore[union-attr]
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(16)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == 16
    assert len({id(c) for c in results}) == 1
    client.close()


def test_known_long_lived_paths_are_classified() -> None:
    for path in _KNOWN_BACKGROUND_PATHS:
        assert _is_background_path(path), path
        assert not _is_transfer_path(path), path
    for path in _KNOWN_TRANSFER_PATHS:
        assert _is_transfer_path(path), path
        assert not _is_background_path(path), path


def test_resources_tree_long_lived_ops_match_classifier() -> None:
    """Fail if a new wait_for_status / upload_file / download_file path is added
    without being covered by the bulkhead suffixes.
    """
    root = Path(__file__).resolve().parents[1] / "src" / "runloop_api_client" / "resources"
    text = "\n".join(p.read_text() for p in root.rglob("*.py"))
    # Paths appear as f-strings or path_template("/v1/.../wait_for_status", ...)
    found_wait = set(re.findall(r'(/v1/[^"\s]*wait_for_status)', text))
    found_upload = set(re.findall(r'(/v1/[^"\s]*upload_file)', text))
    found_download = set(re.findall(r'(/v1/[^"\s]*download_file)', text))

    assert found_wait, "expected wait_for_status paths in resources/"
    assert found_upload, "expected upload_file paths in resources/"
    assert found_download, "expected download_file paths in resources/"

    for path in found_wait:
        concrete = path.replace("{id}", "dbx_1").replace("{devbox_id}", "dbx_1").replace("{execution_id}", "ex_1")
        assert _is_background_path(concrete), path
    for path in found_upload | found_download:
        concrete = path.replace("{id}", "dbx_1")
        assert _is_transfer_path(concrete), path
