"""SDK load test: fires devboxes.create bursts via the Runloop SDK.

Imports the installed package from this checkout so the benchmark always
exercises the exact code here — not a separately published build.

USE_HTTP2=0  → HTTP/1.1 (httpx with http2=False)
default      → HTTP/2  (shared httpx pool with http2=True)

USE_SYNC=1   → blocking sync `Runloop` client driven by a thread pool
default      → async `AsyncRunloop` client driven by asyncio

REQUEST_COUNT defaults to 100 000.

Sync concurrency model
----------------------
The sync `Runloop` client is blocking, so a concurrent burst is driven by a
`ThreadPoolExecutor` rather than `asyncio.gather`. One OS thread per request is
infeasible at high request counts (memory + scheduler overhead, and on most
hosts the open-file-descriptor limit caps real socket concurrency well below
that anyway), so the worker pool is capped:

    workers = min(REQUEST_COUNT, CONCURRENCY)   # CONCURRENCY default 5000

At request counts above the cap, requests queue through the pool — so for the
sync path "concurrency" means the worker count, not REQUEST_COUNT. 5000 is the
starting default; lower `CONCURRENCY` (e.g. 500) if thread/FD pressure makes it
counterproductive on your host.
"""

from __future__ import annotations

import os
import math
import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

from runloop_api_client import Runloop, AsyncRunloop

REQUEST_COUNT = int(os.environ.get("REQUEST_COUNT", "100000"))
RUNLOOP_BASE_URL = os.environ.get("RUNLOOP_BASE_URL")
# HTTP/2 is the SDK default; set USE_HTTP2=0 to benchmark HTTP/1.1.
USE_HTTP2 = os.environ.get("USE_HTTP2", "1") == "1"
# Async (asyncio) by default; set USE_SYNC=1 to benchmark the blocking client.
USE_SYNC = os.environ.get("USE_SYNC", "0") == "1"
# Worker-thread cap for the sync path (see module docstring).
SYNC_WORKER_CAP = int(os.environ.get("CONCURRENCY", "5000"))
PROGRESS_INTERVAL = 2.0


def build_async_client() -> AsyncRunloop:
    kwargs: dict[str, object] = {"max_retries": 0, "timeout": 120.0}
    if RUNLOOP_BASE_URL:
        kwargs["base_url"] = RUNLOOP_BASE_URL
    if not USE_HTTP2:
        # A custom http_client disables the shared HTTP/2 pool.
        # Set http2: false explicitly — omitting it would select HTTP/2.
        kwargs["http_client"] = httpx.AsyncClient(
            http2=False,
            limits=httpx.Limits(max_connections=None, max_keepalive_connections=100),
            timeout=httpx.Timeout(120.0),
        )
    return AsyncRunloop(**kwargs)  # type: ignore[arg-type]


def build_sync_client() -> Runloop:
    kwargs: dict[str, object] = {"max_retries": 0, "timeout": 120.0}
    if RUNLOOP_BASE_URL:
        kwargs["base_url"] = RUNLOOP_BASE_URL
    if not USE_HTTP2:
        kwargs["http_client"] = httpx.Client(
            http2=False,
            limits=httpx.Limits(max_connections=None, max_keepalive_connections=100),
            timeout=httpx.Timeout(120.0),
        )
    return Runloop(**kwargs)  # type: ignore[arg-type]


_CREATE_KWARGS = {
    "blueprint_id": "bp_nonexistent_loadtest_00000",
    "environment_variables": {"TEST_VAR_1": "value_one", "TEST_VAR_2": "value_two"},
    "launch_parameters": {"resource_size_request": "SMALL", "keep_alive_time_seconds": 300},
}


async def send_request_async(client: AsyncRunloop, index: int, run_id: str) -> dict[str, object]:
    start = time.perf_counter()
    status: int | None = None
    error: str | None = None
    try:
        await client.devboxes.create(
            name=f"loadtest-{run_id}-{index}",
            metadata={"test_run": run_id, "index": str(index)},
            **_CREATE_KWARGS,  # type: ignore[arg-type]
        )
        status = 200
    except Exception as exc:
        status = getattr(exc, "status_code", None)
        error = str(exc) or type(exc).__name__
    return {
        "index": index,
        "latency_ms": (time.perf_counter() - start) * 1000,
        "status": status,
        "error": error,
    }


def send_request_sync(client: Runloop, index: int, run_id: str) -> dict[str, object]:
    start = time.perf_counter()
    status: int | None = None
    error: str | None = None
    try:
        client.devboxes.create(
            name=f"loadtest-{run_id}-{index}",
            metadata={"test_run": run_id, "index": str(index)},
            **_CREATE_KWARGS,  # type: ignore[arg-type]
        )
        status = 200
    except Exception as exc:
        status = getattr(exc, "status_code", None)
        error = str(exc) or type(exc).__name__
    return {
        "index": index,
        "latency_ms": (time.perf_counter() - start) * 1000,
        "status": status,
        "error": error,
    }


def percentile(sorted_vals: list[float], p: float) -> float:
    idx = math.ceil(p / 100 * len(sorted_vals)) - 1
    return sorted_vals[max(0, idx)]


def print_metrics(results: list[dict[str, object]], wall_ms: float) -> None:
    latencies = sorted(float(r["latency_ms"]) for r in results)  # type: ignore[arg-type]
    status_counts: dict[str, int] = {}
    for r in results:
        key = str(r["status"]) if r["status"] is not None else "network_error"
        status_counts[key] = status_counts.get(key, 0) + 1

    print("\n=== Load Test Results ===")
    print(f"Requests:        {len(results)}")
    print(f"Wall clock:      {wall_ms / 1000:.2f}s")
    print(f"Throughput:      {len(results) / (wall_ms / 1000):.1f} req/s")
    if latencies:
        print("\nLatency (ms):")
        print(f"  min:           {latencies[0]:.1f}")
        print(f"  p50:           {percentile(latencies, 50):.1f}")
        print(f"  p90:           {percentile(latencies, 90):.1f}")
        print(f"  p95:           {percentile(latencies, 95):.1f}")
        print(f"  p99:           {percentile(latencies, 99):.1f}")
        print(f"  max:           {latencies[-1]:.1f}")
    print("\nStatus codes:")
    for s, c in sorted(status_counts.items()):
        print(f"  {s}: {c}")

    # Break down the opaque "network_error" bucket by exception message so
    # transport-level failures (timeouts, resets, pool exhaustion) are diagnosable.
    error_counts: dict[str, int] = {}
    for r in results:
        if r["status"] is None and r["error"] is not None:
            msg = str(r["error"])
            error_counts[msg] = error_counts.get(msg, 0) + 1
    if error_counts:
        print("\nErrors (network_error breakdown):")
        for msg, c in sorted(error_counts.items(), key=lambda kv: kv[1], reverse=True):
            print(f"  {c}x  {msg}")


def _fd_limit() -> int | None:
    try:
        import resource as _resource

        return _resource.getrlimit(_resource.RLIMIT_NOFILE)[0]
    except Exception:
        return None


def _print_header(run_id: str, fd_limit: int | None, workers: int | None) -> None:
    print(f"Starting load test: {REQUEST_COUNT} requests")
    print(f"Run ID:      {run_id}")
    mode = "sync (ThreadPoolExecutor)" if USE_SYNC else "async (asyncio)"
    print(f"Concurrency: {mode}")
    if USE_SYNC:
        print(f"Workers:     {workers} threads")
    print(f"HTTP mode:   {'HTTP/2 (shared httpx pool)' if USE_HTTP2 else 'HTTP/1.1 (httpx http2=False)'}")
    print(f"Base URL:    {RUNLOOP_BASE_URL or '(SDK default)'}")
    if fd_limit is not None:
        print(f"FD limit:    {fd_limit}")
    print()


async def run_async() -> None:
    client = build_async_client()
    run_id = f"run-{int(time.time())}"
    _print_header(run_id, _fd_limit(), workers=None)

    completed = 0

    async def progress_printer() -> None:
        while True:
            await asyncio.sleep(PROGRESS_INTERVAL)
            pct = completed / REQUEST_COUNT * 100
            print(f"  progress: {completed}/{REQUEST_COUNT} ({pct:.1f}%)")

    async def wrapped(idx: int) -> dict[str, object]:
        nonlocal completed
        r = await send_request_async(client, idx, run_id)
        completed += 1
        return r

    wall_start = time.perf_counter()
    progress_task = asyncio.create_task(progress_printer())
    results = list(await asyncio.gather(*(wrapped(i) for i in range(REQUEST_COUNT))))
    progress_task.cancel()
    wall_ms = (time.perf_counter() - wall_start) * 1000

    await client.close()
    print_metrics(results, wall_ms)


def run_sync() -> None:
    workers = max(1, min(REQUEST_COUNT, SYNC_WORKER_CAP))
    client = build_sync_client()
    run_id = f"run-{int(time.time())}"
    _print_header(run_id, _fd_limit(), workers=workers)

    completed = 0
    stop = threading.Event()

    def progress_printer() -> None:
        while not stop.wait(PROGRESS_INTERVAL):
            pct = completed / REQUEST_COUNT * 100
            print(f"  progress: {completed}/{REQUEST_COUNT} ({pct:.1f}%)")

    progress_thread = threading.Thread(target=progress_printer, daemon=True)
    progress_thread.start()

    results: list[dict[str, object]] = []
    wall_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(send_request_sync, client, i, run_id) for i in range(REQUEST_COUNT)]
        for fut in as_completed(futures):
            results.append(fut.result())
            completed += 1
    wall_ms = (time.perf_counter() - wall_start) * 1000

    stop.set()
    client.close()
    print_metrics(results, wall_ms)


def main() -> None:
    fd_limit = _fd_limit()
    if not USE_HTTP2 and fd_limit is not None and fd_limit < 10000:
        print(f"\nWARNING: File descriptor limit is {fd_limit}. For large HTTP/1.1 bursts, run:")
        print("  ulimit -n 65536")
        print("Or use HTTP/2 multiplexing: USE_HTTP2=1\n")

    if USE_SYNC:
        run_sync()
    else:
        asyncio.run(run_async())


if __name__ == "__main__":
    main()
