"""Tests for shared HTTP transport pool behavior.

Verifies that SDK clients share (or don't share) the underlying httpx
transport, and that refcounting correctly manages the transport lifecycle.
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
        old_sync = _base_mod._shared_sync_transport
        _base_mod._shared_sync_transport = None
        _base_mod._shared_async_transports.clear()
    if old_sync is not None:
        try:
            old_sync._transport.close()
        except Exception:
            pass


def _make_client(**kwargs: Any) -> Runloop:
    kwargs.setdefault("base_url", base_url)
    kwargs.setdefault("bearer_token", bearer_token)
    return Runloop(**kwargs)


def _make_async_client(**kwargs: Any) -> AsyncRunloop:
    kwargs.setdefault("base_url", base_url)
    kwargs.setdefault("bearer_token", bearer_token)
    return AsyncRunloop(**kwargs)


def _get_transport(client: Runloop | AsyncRunloop) -> Any:
    return client._client._transport  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Sync: sharing behavior
# ---------------------------------------------------------------------------


class TestSyncSharedPool:
    def test_shared_pool_uses_same_transport(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)

        assert _get_transport(c1) is _get_transport(c2)
        assert c1._client is not c2._client
        assert c1._uses_shared_pool is True
        assert c2._uses_shared_pool is True

        c1.close()
        c2.close()

    def test_private_pool_uses_different_transports(self):
        c1 = _make_client(shared_http_pool=False)
        c2 = _make_client(shared_http_pool=False)

        assert _get_transport(c1) is not _get_transport(c2)
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

    def test_cookie_isolation(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)

        c1._client.cookies.set("session", "secret-123")
        assert "session" not in c2._client.cookies

        c1.close()
        c2.close()


class TestSyncRefcounting:
    def test_close_one_keeps_transport_alive(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)
        transport = _get_transport(c1)

        assert transport.refcount == 2

        c1.close()
        assert transport.refcount == 1
        assert not c2.is_closed()

        c2.close()
        assert transport.refcount == 0

    def test_double_close_is_safe(self):
        c1 = _make_client(shared_http_pool=True)
        transport = _get_transport(c1)

        c1.close()
        c1.close()  # should not raise or double-decrement
        assert transport.refcount == 0

    def test_three_clients_refcount(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = _make_client(shared_http_pool=True)
        c3 = _make_client(shared_http_pool=True)
        transport = _get_transport(c1)

        assert transport.refcount == 3

        c1.close()
        assert transport.refcount == 2

        c2.close()
        assert transport.refcount == 1

        c3.close()
        assert transport.refcount == 0

    def test_transport_recreated_after_full_release(self):
        c1 = _make_client(shared_http_pool=True)
        t1 = _get_transport(c1)
        c1.close()

        c2 = _make_client(shared_http_pool=True)
        t2 = _get_transport(c2)
        assert t2 is not t1
        assert t2.refcount == 1

        c2.close()


class TestSyncCopy:
    def test_copy_inherits_shared_pool(self):
        c1 = _make_client(shared_http_pool=True)
        c2 = c1.copy()
        transport = _get_transport(c1)

        assert c2._uses_shared_pool is True
        assert _get_transport(c2) is transport
        assert transport.refcount == 2

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
        assert _get_transport(c2) is not _get_transport(c1)

        c1.close()
        c2.close()


# ---------------------------------------------------------------------------
# Async: sharing behavior
# ---------------------------------------------------------------------------


class TestAsyncSharedPool:
    async def test_shared_pool_uses_same_transport(self):
        c1 = _make_async_client(shared_http_pool=True)
        c2 = _make_async_client(shared_http_pool=True)

        assert _get_transport(c1) is _get_transport(c2)
        assert c1._client is not c2._client
        assert c1._uses_shared_pool is True
        assert c2._uses_shared_pool is True

    def test_private_pool_uses_different_transports(self):
        c1 = _make_async_client(shared_http_pool=False)
        c2 = _make_async_client(shared_http_pool=False)

        assert _get_transport(c1) is not _get_transport(c2)
        assert c1._uses_shared_pool is False

    def test_custom_http_client_bypasses_sharing(self):
        custom = httpx.AsyncClient()
        c1 = _make_async_client(http_client=custom, shared_http_pool=True)

        assert c1._client is custom
        assert c1._uses_shared_pool is False

    async def test_default_is_shared(self):
        c1 = _make_async_client()
        assert c1._uses_shared_pool is True

    def test_no_loop_creates_private_client(self):
        c1 = _make_async_client(shared_http_pool=True)
        assert c1._uses_shared_pool is False


class TestAsyncRefcounting:
    async def test_close_one_keeps_transport_alive(self):
        c1 = _make_async_client(shared_http_pool=True)
        c2 = _make_async_client(shared_http_pool=True)
        transport = _get_transport(c1)

        assert transport.refcount == 2

        await c1.close()
        assert transport.refcount == 1
        assert not c2.is_closed()

        await c2.close()
        assert transport.refcount == 0

    async def test_double_close_is_safe(self):
        c1 = _make_async_client(shared_http_pool=True)
        transport = _get_transport(c1)

        await c1.close()
        await c1.close()  # should not raise or double-decrement
        assert transport.refcount == 0

    def test_no_loop_client_closes_properly(self):
        """Client created without a running loop should close without leaking."""
        c1 = _make_async_client(shared_http_pool=True)
        assert c1._uses_shared_pool is False

        asyncio.run(c1.close())
        assert c1.is_closed()


class TestAsyncCopy:
    async def test_copy_inherits_shared_pool(self):
        c1 = _make_async_client(shared_http_pool=True)
        c2 = c1.copy()
        transport = _get_transport(c1)

        assert c2._uses_shared_pool is True
        assert _get_transport(c2) is transport
        assert transport.refcount == 2

    async def test_copy_with_custom_client_disables_sharing(self):
        c1 = _make_async_client(shared_http_pool=True)
        custom = httpx.AsyncClient()
        c2 = c1.copy(http_client=custom)

        assert c2._uses_shared_pool is False
        assert c2._client is custom


class TestSyncConnectionLimits:
    def test_custom_limits_force_private_pool(self):
        limits = httpx.Limits(max_connections=42, max_keepalive_connections=7)
        c = _make_client(connection_limits=limits)

        assert c._uses_shared_pool is False
        assert c._connection_limits is limits
        transport = _get_transport(c)
        # Real httpx.HTTPTransport (not the shared wrapper)
        assert isinstance(transport, httpx.HTTPTransport)
        # Pool actually got the requested limits
        assert transport._pool._max_connections == 42
        assert transport._pool._max_keepalive_connections == 7

        c.close()

    def test_custom_limits_override_shared_pool_request(self):
        # Even with shared_http_pool=True (default), explicit limits take precedence
        # and the client gets a private pool.
        limits = httpx.Limits(max_connections=5)
        c = _make_client(shared_http_pool=True, connection_limits=limits)

        assert c._uses_shared_pool is False

        c.close()

    def test_copy_inherits_connection_limits(self):
        limits = httpx.Limits(max_connections=25)
        c1 = _make_client(connection_limits=limits)
        c2 = c1.copy()

        assert c2._connection_limits is limits
        assert c2._uses_shared_pool is False
        assert _get_transport(c2)._pool._max_connections == 25

        c1.close()
        c2.close()

    def test_copy_can_override_connection_limits(self):
        c1 = _make_client(connection_limits=httpx.Limits(max_connections=25))
        new_limits = httpx.Limits(max_connections=200, max_keepalive_connections=50)
        c2 = c1.copy(connection_limits=new_limits)

        assert c2._connection_limits is new_limits
        assert _get_transport(c2)._pool._max_connections == 200

        c1.close()
        c2.close()

    def test_copy_can_reset_connection_limits(self):
        c1 = _make_client(connection_limits=httpx.Limits(max_connections=25))
        # Passing None resets to the SDK default limits but keeps the inherited
        # sharing mode (parent was private, so the copy stays private). Use
        # shared_http_pool=True alongside to also re-enable sharing.
        c2 = c1.copy(connection_limits=None)

        assert c2._connection_limits is None
        assert c2._uses_shared_pool is False

        c3 = c1.copy(connection_limits=None, shared_http_pool=True)
        assert c3._connection_limits is None
        assert c3._uses_shared_pool is True

        c1.close()
        c2.close()
        c3.close()


class TestAsyncConnectionLimits:
    async def test_custom_limits_force_private_pool(self):
        limits = httpx.Limits(max_connections=42, max_keepalive_connections=7)
        c = _make_async_client(connection_limits=limits)

        assert c._uses_shared_pool is False
        assert c._connection_limits is limits
        transport = _get_transport(c)
        assert isinstance(transport, httpx.AsyncHTTPTransport)
        assert transport._pool._max_connections == 42
        assert transport._pool._max_keepalive_connections == 7

        await c.close()

    async def test_custom_limits_override_shared_pool_request(self):
        limits = httpx.Limits(max_connections=5)
        c = _make_async_client(shared_http_pool=True, connection_limits=limits)

        assert c._uses_shared_pool is False

        await c.close()

    async def test_copy_inherits_connection_limits(self):
        limits = httpx.Limits(max_connections=25)
        c1 = _make_async_client(connection_limits=limits)
        c2 = c1.copy()

        assert c2._connection_limits is limits
        assert c2._uses_shared_pool is False
        assert _get_transport(c2)._pool._max_connections == 25


class TestAsyncCrossLoop:
    def test_separate_loops_get_separate_transports(self):
        """Clients created in different asyncio.run() calls must not share a transport."""

        async def create_client() -> Any:
            c = _make_async_client(shared_http_pool=True)
            transport = _get_transport(c)
            await c.close()
            return transport

        t1 = asyncio.run(create_client())
        t2 = asyncio.run(create_client())

        assert t1 is not t2, "each loop should get its own transport"

    def test_same_loop_shares_transport(self):
        """Clients created in the same asyncio.run() must share a transport."""

        async def create_two() -> tuple[int, int]:
            c1 = _make_async_client(shared_http_pool=True)
            c2 = _make_async_client(shared_http_pool=True)
            id1 = id(_get_transport(c1))
            id2 = id(_get_transport(c2))
            await c1.close()
            await c2.close()
            return id1, id2

        id1, id2 = asyncio.run(create_two())
        assert id1 == id2
