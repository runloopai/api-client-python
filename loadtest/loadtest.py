"""SDK load test: fires devboxes.create bursts via AsyncRunloop.

Imports the installed package from this checkout so the benchmark always
exercises the exact code here — not a separately published build.

USE_HTTP2=0  → HTTP/1.1 (httpx with http2=False)
default      → HTTP/2  (shared httpx pool with http2=True)
REQUEST_COUNT defaults to 100 000.
"""

from __future__ import annotations

import asyncio
import math
import os
import time

import httpx

from runloop_api_client import AsyncRunloop

REQUEST_COUNT = int(os.environ.get("REQUEST_COUNT", "100000"))
RUNLOOP_BASE_URL = os.environ.get("RUNLOOP_BASE_URL")
# HTTP/2 is the SDK default; set USE_HTTP2=0 to benchmark HTTP/1.1.
USE_HTTP2 = os.environ.get("USE_HTTP2", "1") == "1"
PROGRESS_INTERVAL = 2.0


def build_client() -> AsyncRunloop:
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


async def send_request(client: AsyncRunloop, index: int, run_id: str) -> dict[str, object]:
    start = time.perf_counter()
    status: int | None = None
    try:
        await client.devboxes.create(
            blueprint_id="bp_nonexistent_loadtest_00000",
            name=f"loadtest-{run_id}-{index}",
            environment_variables={"TEST_VAR_1": "value_one", "TEST_VAR_2": "value_two"},
            metadata={"test_run": run_id, "index": str(index)},
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 300},
        )
        status = 200
    except Exception as exc:
        status = getattr(exc, "status_code", None)
    return {"index": index, "latency_ms": (time.perf_counter() - start) * 1000, "status": status}


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


async def main() -> None:
    fd_limit: int | None = None
    try:
        import resource as _resource

        fd_limit = _resource.getrlimit(_resource.RLIMIT_NOFILE)[0]
    except Exception:
        pass

    if not USE_HTTP2 and fd_limit is not None and fd_limit < 10000:
        print(f"\nWARNING: File descriptor limit is {fd_limit}. For large HTTP/1.1 bursts, run:")
        print("  ulimit -n 65536")
        print("Or use HTTP/2 multiplexing: USE_HTTP2=1\n")

    client = build_client()
    run_id = f"run-{int(time.time())}"

    print(f"Starting load test: {REQUEST_COUNT} concurrent requests")
    print(f"Run ID:      {run_id}")
    print(f"HTTP mode:   {'HTTP/2 (shared httpx pool)' if USE_HTTP2 else 'HTTP/1.1 (httpx http2=False)'}")
    print(f"Base URL:    {RUNLOOP_BASE_URL or '(SDK default)'}")
    if fd_limit is not None:
        print(f"FD limit:    {fd_limit}")
    print()

    completed = 0

    async def progress_printer() -> None:
        while True:
            await asyncio.sleep(PROGRESS_INTERVAL)
            pct = completed / REQUEST_COUNT * 100
            print(f"  progress: {completed}/{REQUEST_COUNT} ({pct:.1f}%)")

    async def wrapped(idx: int) -> dict[str, object]:
        nonlocal completed
        r = await send_request(client, idx, run_id)
        completed += 1
        return r

    wall_start = time.perf_counter()
    progress_task = asyncio.create_task(progress_printer())
    results = list(await asyncio.gather(*(wrapped(i) for i in range(REQUEST_COUNT))))
    progress_task.cancel()
    wall_ms = (time.perf_counter() - wall_start) * 1000

    await client.close()
    print_metrics(results, wall_ms)


if __name__ == "__main__":
    asyncio.run(main())
