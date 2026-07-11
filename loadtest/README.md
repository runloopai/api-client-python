# Load tests

Manual transport comparison scripts for the Runloop Python SDK. These hit the
real API and are not part of `pytest`; run on demand.

## End-to-end transport comparison (real API)

All scripts require `RUNLOOP_API_KEY`. Set `RUNLOOP_BASE_URL` to override the
default endpoint (`https://api.runloop.ai`).

Every script sends `devboxes.create` requests against a **deliberately
nonexistent blueprint** (`bp_nonexistent_loadtest_00000`), so every request
fails fast server-side (HTTP `400`) and **no devboxes are created** — isolating
client + server _request handling_ from provisioning.

| Script | Transport under test |
| --- | --- |
| `loadtest.py` | The **SDK** itself. `USE_HTTP2=0` → HTTP/1.1; default / `USE_HTTP2=1` → HTTP/2 (shared httpx pool). `USE_SYNC=0` (default) → async `AsyncRunloop` via asyncio; `USE_SYNC=1` → blocking `Runloop` via a thread pool. Always runs against the installed package in this checkout. |
| `h2_test.py` | Raw `httpx` HTTP/2, bypassing the SDK. Configurable connection count. |
| `h2_single_conn.py` | Raw `httpx` HTTP/2 on a single warmed connection (50-request burst). |
| `raw_fetch_test.py` | Raw `httpx` HTTP/1.1 keep-alive baseline. |
| `alpn_check.py` | Confirms the origin negotiates `h2` via TLS ALPN. |

The raw-transport probes compare httpx HTTP/2 multiplexing against HTTP/1.1
directly — the same comparison that motivates the SDK's shared HTTP/2 pool.
They're kept so the comparison stays reproducible.

```sh
# Install the SDK from this checkout (editable):
cd /path/to/api-client-python && uv sync

# SDK: HTTP/2 (default) vs HTTP/1.1, 2000-request burst
source ~/env && REQUEST_COUNT=2000 uv run python loadtest/loadtest.py            # HTTP/2
source ~/env && REQUEST_COUNT=2000 USE_HTTP2=0 uv run python loadtest/loadtest.py # HTTP/1.1

# SDK: async (default) vs sync client
source ~/env && REQUEST_COUNT=2000 USE_SYNC=1 uv run python loadtest/loadtest.py             # sync, HTTP/2
source ~/env && REQUEST_COUNT=2000 USE_SYNC=1 CONCURRENCY=500 uv run python loadtest/loadtest.py  # cap the thread pool

# Raw httpx HTTP/2 vs HTTP/1.1 comparison
source ~/env && uv run python loadtest/h2_test.py
source ~/env && uv run python loadtest/raw_fetch_test.py

# Single-connection burst
source ~/env && uv run python loadtest/h2_single_conn.py

# ALPN check
source ~/env && uv run python loadtest/alpn_check.py
```

HTTP/1.1 opens a socket per in-flight request; for large bursts raise the
file-descriptor limit (`ulimit -n 65536`) or keep `REQUEST_COUNT` small.

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `RUNLOOP_API_KEY` | *(required)* | API key |
| `RUNLOOP_BASE_URL` | `https://api.runloop.ai` | Override API endpoint |
| `REQUEST_COUNT` | `100000` (`loadtest.py`) / `10000` (`h2_test.py`) / `500` (`raw_fetch_test.py`) | Total requests |
| `NUM_CONNECTIONS` | `10` (`h2_test.py`) / `20` (`raw_fetch_test.py`) | Parallel connections |
| `USE_HTTP2` | `1` | `0` to force HTTP/1.1 in `loadtest.py` |
| `USE_SYNC` | `0` | `1` to benchmark the blocking `Runloop` client (thread pool) instead of async `AsyncRunloop` |
| `CONCURRENCY` | `5000` | Worker-thread cap for the sync path. Effective workers = `min(REQUEST_COUNT, CONCURRENCY)`; above the cap, requests queue through the pool. Lower it (e.g. `500`) if thread/FD pressure dominates. |
