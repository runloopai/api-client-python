"""Tests for HTTP/2 stream-overflow → new connection behavior."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from runloop_api_client._http2_pool_fix import (
    _stream_slots_saturated,
    install,
)


def test_install_is_idempotent() -> None:
    # Package import already installs the patch.
    assert install() is False


def test_stream_slots_saturated_helper() -> None:
    conn: Any = MagicMock()
    conn._max_streams = 100
    conn._events = {i: [] for i in range(1, 90)}  # 89 in flight → 11 free < 16
    assert _stream_slots_saturated(conn) is True

    conn._events = {i: [] for i in range(1, 80)}  # 79 in flight → 21 free
    assert _stream_slots_saturated(conn) is False

    conn._max_streams = 0
    assert _stream_slots_saturated(conn) is False


def _bare_async_h2_connection() -> Any:
    from httpcore._async.http2 import AsyncHTTP2Connection, HTTPConnectionState

    conn = object.__new__(AsyncHTTP2Connection)
    conn._state = HTTPConnectionState.ACTIVE
    conn._connection_error = False
    conn._used_all_stream_ids = False
    conn._h2_state = MagicMock()
    # Anything other than ConnectionState.CLOSED.
    conn._h2_state.state_machine.state = object()
    return conn


def test_is_available_false_when_streams_nearly_full() -> None:
    conn = _bare_async_h2_connection()
    conn._max_streams = 100
    conn._events = {i: [] for i in range(1, 95)}  # 6 free
    assert conn.is_available() is False


def test_is_available_true_when_stream_slots_remain() -> None:
    conn = _bare_async_h2_connection()
    conn._max_streams = 100
    conn._events = {i: [] for i in range(1, 50)}  # 51 free
    assert conn.is_available() is True


def test_sync_is_available_false_when_streams_nearly_full() -> None:
    from httpcore._sync.http2 import HTTP2Connection, HTTPConnectionState

    conn = object.__new__(HTTP2Connection)
    conn._state = HTTPConnectionState.ACTIVE
    conn._connection_error = False
    conn._used_all_stream_ids = False
    conn._h2_state = MagicMock()
    conn._h2_state.state_machine.state = object()
    conn._max_streams = 100
    conn._events = {i: [] for i in range(1, 95)}
    assert conn.is_available() is False
