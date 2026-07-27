"""TLS+ALPN HTTP/2 integration tests for workload bulkhead pools.

Proves wire behavior (not just Python object identity):
- Blocking waits and creates land on different server connections.
- Create completes promptly even when background streams are saturated.
- Upload body stall does not delay create on the API pool.
"""

from __future__ import annotations

import ssl
import json
import time
import asyncio
import tempfile
import threading
import subprocess
from typing import Any, Iterator, cast
from pathlib import Path

import httpx
import pytest

h2 = pytest.importorskip("h2")
import h2.config  # noqa: E402
import h2.events  # noqa: E402
import h2.settings  # noqa: E402
import h2.connection  # noqa: E402
import h2.exceptions  # noqa: E402

import runloop_api_client._base_client as _base_mod
from runloop_api_client import AsyncRunloop
from runloop_api_client._base_client import make_request_options

pytestmark = pytest.mark.timeout(30)


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


@pytest.fixture(autouse=True)
def _reset_pools() -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    _clear_pool_state()
    yield
    _clear_pool_state()


def _ensure_certs(dir_path: Path) -> tuple[Path, Path]:
    cert = dir_path / "cert.pem"
    key = dir_path / "key.pem"
    if not cert.exists():
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-keyout",
                str(key),
                "-out",
                str(cert),
                "-days",
                "1",
                "-nodes",
                "-subj",
                "/CN=localhost",
            ],
            check=True,
            capture_output=True,
        )
    return cert, key


class _H2BulkheadServer:
    """Minimal TLS+ALPN h2 server that records per-connection request timing."""

    def __init__(self, *, max_concurrent_streams: int = 2, upload_stall_s: float = 0.0) -> None:
        self.max_concurrent_streams = max_concurrent_streams
        self.upload_stall_s = upload_stall_s
        self.observations: list[dict[str, Any]] = []
        self.active_waits = 0
        self.active_uploads = 0
        self.release_upload_credit = asyncio.Event()
        self._conn_seq = 0
        self._conn_lock = threading.Lock()
        self._server: asyncio.Server | None = None
        self._cert_dir = Path(tempfile.mkdtemp(prefix="h2-bulkhead-"))
        self.cert, self.key = _ensure_certs(self._cert_dir)
        self.host = "127.0.0.1"
        self.port = 0

    def _next_conn_id(self) -> int:
        with self._conn_lock:
            self._conn_seq += 1
            return self._conn_seq

    async def start(self) -> str:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(str(self.cert), str(self.key))
        ctx.set_alpn_protocols(["h2"])
        self._server = await asyncio.start_server(self._handle, self.host, 0, ssl=ctx)
        sockets = self._server.sockets
        assert sockets
        self.port = int(sockets[0].getsockname()[1])
        return f"https://{self.host}:{self.port}"

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        conn_id = self._next_conn_id()
        config = h2.config.H2Configuration(client_side=False, header_encoding="utf-8")
        conn = h2.connection.H2Connection(config=config)
        conn.initiate_connection()
        conn.update_settings(
            {
                h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS: self.max_concurrent_streams,
            }
        )
        writer.write(conn.data_to_send())
        await writer.drain()

        streams: dict[int, dict[str, Any]] = {}
        write_lock = asyncio.Lock()

        async def flush_withheld_credit() -> None:
            """When the test releases the stall, return WINDOW_UPDATE so the upload can finish."""
            await self.release_upload_credit.wait()
            for _ in range(200):
                async with write_lock:
                    for sid, st in list(streams.items()):
                        owed = int(st.get("flow_controlled") or 0)
                        if owed:
                            conn.acknowledge_received_data(owed, sid)
                            st["flow_controlled"] = 0
                    to_send = conn.data_to_send()
                    if to_send:
                        writer.write(to_send)
                        await writer.drain()
                if self.active_uploads == 0 and not any(int(st.get("flow_controlled") or 0) for st in streams.values()):
                    return
                await asyncio.sleep(0.05)

        credit_task = asyncio.create_task(flush_withheld_credit())

        async def respond(stream_id: int, st: dict[str, Any]) -> None:
            path = st["path"]
            method = st["method"]
            started = st["started"]
            hold_s = 0.0
            if path.endswith("/wait_for_status"):
                hold_s = float(st.get("hold_s") or 2.0)
            if hold_s > 0:
                await asyncio.sleep(hold_s)

            if st.get("flow_controlled"):
                async with write_lock:
                    conn.acknowledge_received_data(st["flow_controlled"], stream_id)
                    writer.write(conn.data_to_send())
                    await writer.drain()
                st["flow_controlled"] = 0

            finished = time.perf_counter()
            self.observations.append(
                {
                    "conn_id": conn_id,
                    "path": path,
                    "method": method,
                    "started": started,
                    "finished": finished,
                    "duration_s": finished - started,
                    "body_bytes": len(st.get("body") or b""),
                }
            )
            if path.endswith("/wait_for_status"):
                self.active_waits = max(0, self.active_waits - 1)
            if path.endswith("/upload_file"):
                self.active_uploads = max(0, self.active_uploads - 1)

            if path == "/v1/devboxes" and method == "POST":
                payload = {"id": "dbx_test", "status": "running"}
            else:
                payload = {"ok": True}
            raw = json.dumps(payload).encode()
            headers = [
                (":status", "200"),
                ("content-type", "application/json"),
                ("content-length", str(len(raw))),
            ]
            async with write_lock:
                conn.send_headers(stream_id, headers)
                conn.send_data(stream_id, raw, end_stream=True)
                writer.write(conn.data_to_send())
                await writer.drain()
            streams.pop(stream_id, None)

        try:
            while True:
                data = await reader.read(65535)
                if not data:
                    break
                try:
                    events = conn.receive_data(data)
                except h2.exceptions.ProtocolError:
                    break
                for raw_event in events:
                    # h2's Event hierarchy is poorly typed under pyright strict.
                    event = cast(Any, raw_event)
                    if isinstance(raw_event, h2.events.RequestReceived):
                        st = streams.setdefault(
                            event.stream_id,
                            {
                                "headers": [],
                                "body": bytearray(),
                                "method": "GET",
                                "path": "/",
                                "started": time.perf_counter(),
                                "flow_controlled": 0,
                                "hold_s": 2.0,
                            },
                        )
                        st["headers"] = list(event.headers)
                        for k, v in event.headers:
                            if k == ":method":
                                st["method"] = v
                            elif k == ":path":
                                st["path"] = v.split("?", 1)[0]
                            elif k.lower() == "x-hold-seconds":
                                try:
                                    st["hold_s"] = float(v)
                                except ValueError:
                                    pass
                        if str(st["path"]).endswith("/wait_for_status"):
                            self.active_waits += 1
                        if str(st["path"]).endswith("/upload_file"):
                            self.active_uploads += 1
                    elif isinstance(raw_event, h2.events.DataReceived):
                        st = streams.setdefault(event.stream_id, {"body": bytearray(), "flow_controlled": 0})
                        st["body"].extend(event.data)
                        stall_upload = self.upload_stall_s > 0 and str(st.get("path", "")).endswith("/upload_file")
                        if stall_upload and not self.release_upload_credit.is_set():
                            st["flow_controlled"] = st.get("flow_controlled", 0) + event.flow_controlled_length
                        else:
                            conn.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                    elif isinstance(raw_event, h2.events.StreamEnded):
                        st = streams.get(event.stream_id)
                        if st is not None:
                            asyncio.create_task(respond(event.stream_id, st))
                    elif isinstance(raw_event, h2.events.StreamReset):
                        streams.pop(event.stream_id, None)
                async with write_lock:
                    to_send = conn.data_to_send()
                    if to_send:
                        writer.write(to_send)
                        await writer.drain()
        except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
            pass
        finally:
            credit_task.cancel()
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass


async def _wait_until(predicate: Any, *, timeout_s: float = 5.0) -> None:
    deadline = time.perf_counter() + timeout_s
    while time.perf_counter() < deadline:
        if predicate():
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met before timeout")


@pytest.mark.asyncio
async def test_waits_and_create_use_different_h2_connections(monkeypatch: pytest.MonkeyPatch) -> None:
    # Force trust of the ephemeral self-signed cert used by the local h2 server.
    orig_transport_init = httpx.AsyncHTTPTransport.__init__

    def _transport_init(self: Any, *args: Any, **kwargs: Any) -> None:
        kwargs["verify"] = False
        orig_transport_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.AsyncHTTPTransport, "__init__", _transport_init)

    server = _H2BulkheadServer(max_concurrent_streams=2)
    base = await server.start()
    try:
        client = AsyncRunloop(
            bearer_token="test-token",
            base_url=base,
            shared_http_pool=False,
            background_pool_shards=1,
            transfer_pool_shards=1,
            max_retries=0,
        )
        try:
            wait_headers = {"X-Hold-Seconds": "2.5"}

            async def wait_call() -> object:
                return await client.post(
                    "/v1/devboxes/dbx_shared/wait_for_status",
                    body={"statuses": ["running"], "timeout_seconds": 5},
                    options=make_request_options(extra_headers=wait_headers),
                    cast_to=object,
                )

            wait_tasks = [asyncio.create_task(wait_call()) for _ in range(2)]
            await _wait_until(lambda: server.active_waits >= 2, timeout_s=5.0)

            t0 = time.perf_counter()
            create_result = await client.post(
                "/v1/devboxes",
                body={"name": "bulkhead-create"},
                cast_to=object,
            )
            create_s = time.perf_counter() - t0

            assert isinstance(create_result, dict)
            assert create_result["id"] == "dbx_test"
            assert create_s < 0.75, f"create blocked by waits: {create_s:.3f}s"

            await asyncio.gather(*wait_tasks)

            wait_obs = [o for o in server.observations if o["path"].endswith("/wait_for_status")]
            create_obs = [o for o in server.observations if o["path"] == "/v1/devboxes"]
            assert len(wait_obs) == 2
            assert len(create_obs) == 1
            wait_conns = {o["conn_id"] for o in wait_obs}
            create_conn = create_obs[0]["conn_id"]
            assert create_conn not in wait_conns, f"create conn {create_conn} overlapped wait conns {wait_conns}"
        finally:
            await client.close()
    finally:
        await server.stop()


@pytest.mark.asyncio
async def test_upload_stall_does_not_block_create(monkeypatch: pytest.MonkeyPatch) -> None:
    orig_transport_init = httpx.AsyncHTTPTransport.__init__

    def _transport_init(self: Any, *args: Any, **kwargs: Any) -> None:
        kwargs["verify"] = False
        orig_transport_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.AsyncHTTPTransport, "__init__", _transport_init)

    server = _H2BulkheadServer(max_concurrent_streams=100, upload_stall_s=2.5)
    base = await server.start()
    try:
        client = AsyncRunloop(
            bearer_token="test-token",
            base_url=base,
            shared_http_pool=False,
            background_pool_shards=1,
            transfer_pool_shards=1,
            max_retries=0,
        )
        try:
            payload = b"x" * (256 * 1024)

            async def upload() -> object:
                return await client.post(
                    "/v1/devboxes/dbx_up/upload_file",
                    content=payload,
                    cast_to=object,
                    options=make_request_options(
                        extra_headers={"content-type": "application/octet-stream"},
                    ),
                )

            upload_task = asyncio.create_task(upload())
            await _wait_until(lambda: server.active_uploads >= 1, timeout_s=5.0)

            t0 = time.perf_counter()
            create_result = await client.post(
                "/v1/devboxes",
                body={"name": "during-upload"},
                cast_to=object,
            )
            create_s = time.perf_counter() - t0

            assert isinstance(create_result, dict)
            assert create_result["id"] == "dbx_test"
            assert create_s < 0.75, f"create blocked by upload stall: {create_s:.3f}s"

            # Unblock the stalled upload body so the test can finish cleanly.
            server.release_upload_credit.set()
            # Nudge the connection by allowing the client to finish sending.
            await asyncio.wait_for(upload_task, timeout=10.0)

            upload_obs = [o for o in server.observations if o["path"].endswith("/upload_file")]
            create_obs = [o for o in server.observations if o["path"] == "/v1/devboxes"]
            assert len(upload_obs) == 1
            assert len(create_obs) == 1
            assert create_obs[0]["conn_id"] != upload_obs[0]["conn_id"]
            assert create_obs[0]["finished"] < upload_obs[0]["finished"]
        finally:
            await client.close()
    finally:
        await server.stop()
