"""Tests for shared HTTP connection pool behavior.

Verifies that SDK clients share (or don't share) the underlying httpx
transport, and that refcounting correctly manages the pool lifecycle.
"""

from __future__ import annotations

import os
import asyncio
from typing import Any, Iterator

import httpx
import pytest

import runloop_api_client._base_client as _base_mod
from runloop_api_client import Runloop, AsyncRunloop

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"


@pytest.fixture(autouse=True)
def _reset_shared_pool() -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    _clear_pool_state()
    yield
    _clear_pool_state()


def _clear_pool_state() -> None:
    with _base_mod._pool_lock:
        if _base_mod._shared_sync_client is not None and not _base_mod._shared_sync_client.is_closed:
            try:
                _base_mod._shared_sync_client.close()
            except Exception:
                pass
        _base_mod._shared_sync_client = None
        _base_mod._shared_sync_refcount = 0

        _base_mod._async_pools.clear()


def _make_client(**kwargs: Any) -> Runloop:
    kwargs.setdefault("base_url", base_url)
    kwargs.setdefault("bearer_token", bearer_token)
    return Runloop(**kwargs)


def _make_async_client(**kwargs: Any) -> AsyncRunloop:
    kwargs.setdefault("base_url", base_url)
    kwargs.setdefault("bearer_token", bearer_token)
    return AsyncRunloop(**kwargs)


# ---------------------------------------------------------------------------
# Sync: sharing behavior
# ---------------------------------------------------------------------------


class TestSyncSharedPool:
    def test_shared_pool_uses_same_client(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)

        assert c1._client is c2._client
        assert c1._uses_shared_pool is True
        assert c2._uses_shared_pool is True

        c1.close()
        c2.close()

    def test_private_pool_uses_different_clients(self):
        c1 = _make_client(shared_http_pool=False)
        c2 = _make_client(shared_http_pool=False)

        assert c1._client is not c2._client
        assert c1._uses_shared_pool is False
        assert c2._uses_shared_pool is False

        c1.close()
        c2.close()

    def test_custom_http_client_bypasses_sharing(self):
        custom = httpx.Client()
        c1 = _make_client(http_client=custom, shared_http_pool=True)

        assert c1._client is custom
        assert c1._uses_shared_pool is False

        c1.close()
        custom.close()

    def test_default_is_shared(self):
        c1 = _make_client()
        assert c1._uses_shared_pool is True
        c1.close()


class TestSyncRefcounting:
    def test_close_one_keeps_pool_alive(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)
        pool = c1._client

        c1.close()
        assert not pool.is_closed
        assert _base_mod._shared_sync_refcount == 1

        c2.close()
        assert pool.is_closed
        assert _base_mod._shared_sync_client is None
        assert _base_mod._shared_sync_refcount == 0

    def test_double_close_is_safe(self):
        c1 = _make_client(shared_http_pool=True)
        c1.close()
        c1.close()  # should not raise or go negative
        assert _base_mod._shared_sync_refcount == 0

    def test_three_clients_refcount(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)
        c3 = _make_client(shared_http_pool=True)
        pool = c1._client

        assert _base_mod._shared_sync_refcount == 3

        c1.close()
        assert _base_mod._shared_sync_refcount == 2
        assert not pool.is_closed

        c2.close()
        assert _base_mod._shared_sync_refcount == 1
        assert not pool.is_closed

        c3.close()
        assert _base_mod._shared_sync_refcount == 0
        assert pool.is_closed

    def test_pool_recreated_after_full_release(self):
        c1 = _make_client(shared_http_pool=True)
        pool1 = c1._client
        c1.close()

        c2 = _make_client(shared_http_pool=True)
        pool2 = c2._client
        assert pool2 is not pool1
        assert not pool2.is_closed

        c2.close()


class TestSyncCopy:
    def test_copy_inherits_shared_pool(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = c1.copy()

        assert c2._uses_shared_pool is True
        assert c2._client is c1._client
        assert _base_mod._shared_sync_refcount == 2

        c1.close()
        c2.close()

    def test_copy_with_custom_client_disables_sharing(self):
        c1 = _make_client(shared_http_pool=True)
        custom = httpx.Client()
        c2 = c1.copy(http_client=custom)

        assert c2._uses_shared_pool is False
        assert c2._client is custom

        c1.close()
        c2.close()
        custom.close()

    def test_copy_of_non_shared_stays_non_shared(self):
        c1 = _make_client(shared_http_pool=False)
        c2 = c1.copy()

        assert c2._uses_shared_pool is False
        assert c2._client is not c1._client

        c1.close()
        c2.close()


# ---------------------------------------------------------------------------
# Async: sharing behavior
# ---------------------------------------------------------------------------


class TestAsyncSharedPool:
    async def test_shared_pool_uses_same_client(self):
        c1 = _make_async_client(shared_http_pool=True)
        c2 = _make_async_client(shared_http_pool=True)

        assert c1._client is c2._client
        assert c1._uses_shared_pool is True
        assert c2._uses_shared_pool is True

    def test_private_pool_uses_different_clients(self):
        c1 = _make_async_client(shared_http_pool=False)
        c2 = _make_async_client(shared_http_pool=False)

        assert c1._client is not c2._client
        assert c1._uses_shared_pool is False

    def test_custom_http_client_bypasses_sharing(self):
        custom = httpx.AsyncClient()
        c1 = _make_async_client(http_client=custom, shared_http_pool=True)

        assert c1._client is custom
        assert c1._uses_shared_pool is False

    async def test_default_is_shared(self):
        c1 = _make_async_client()
        assert c1._uses_shared_pool is True


def _async_pool_refcount(loop: asyncio.AbstractEventLoop | None) -> int:
    pool = _base_mod._async_pools.get(loop) if loop is not None else None
    return pool.refcount if pool is not None else 0


class TestAsyncRefcounting:
    async def test_close_one_keeps_pool_alive(self):
        c1 = _make_async_client(shared_http_pool=True)
        c2 = _make_async_client(shared_http_pool=True)
        loop = c1._pool_loop

        c1._release_shared_pool_sync()
        assert _async_pool_refcount(loop) == 1

        c2._release_shared_pool_sync()
        assert _async_pool_refcount(loop) == 0

    async def test_double_release_is_safe(self):
        c1 = _make_async_client(shared_http_pool=True)
        c1._release_shared_pool_sync()
        c1._release_shared_pool_sync()  # should not raise or go negative
        assert _async_pool_refcount(c1._pool_loop) == 0


class TestAsyncCopy:
    async def test_copy_inherits_shared_pool(self):
        c1 = _make_async_client(shared_http_pool=True)
        c2 = c1.copy()
        loop = c1._pool_loop

        assert c2._uses_shared_pool is True
        assert c2._client is c1._client
        assert _async_pool_refcount(loop) == 2

    async def test_copy_with_custom_client_disables_sharing(self):
        c1 = _make_async_client(shared_http_pool=True)
        custom = httpx.AsyncClient()
        c2 = c1.copy(http_client=custom)

        assert c2._uses_shared_pool is False
        assert c2._client is custom


class TestAsyncCrossLoop:
    def test_separate_loops_get_separate_pools(self):
        """Clients created in different asyncio.run() calls must not share a pool."""

        async def create_client() -> int:
            c = _make_async_client(shared_http_pool=True)
            client_id = id(c._client)
            await c.close()
            return client_id

        id1 = asyncio.run(create_client())
        id2 = asyncio.run(create_client())

        assert id1 != id2, "each loop should get its own httpx.AsyncClient"

    def test_same_loop_shares_pool(self):
        """Clients created in the same asyncio.run() must share a pool."""

        async def create_two() -> tuple[int, int]:
            c1 = _make_async_client(shared_http_pool=True)
            c2 = _make_async_client(shared_http_pool=True)
            id1 = id(c1._client)
            id2 = id(c2._client)
            await c1.close()
            await c2.close()
            return id1, id2

        id1, id2 = asyncio.run(create_two())
        assert id1 == id2
