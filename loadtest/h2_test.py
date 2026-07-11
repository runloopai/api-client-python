"""Raw httpx HTTP/2 load test: REQUEST_COUNT requests across NUM_CONNECTIONS connections."""

from __future__ import annotations

import asyncio
import math
import os
import time
from typing import cast

import httpx

REQUEST_COUNT = int(os.environ.get("REQUEST_COUNT", "10000"))
NUM_CONNECTIONS = int(os.environ.get("NUM_CONNECTIONS", "10"))
BASE_URL = os.environ.get("RUNLOOP_BASE_URL", "https://api.runloop.ai")
API_KEY = os.environ["RUNLOOP_API_KEY"]

BODY = {
    "blueprint_id": "bp_nonexistent_loadtest_00000",
    "name": "loadtest-h2-0",
    "environment_variables": {"TEST_VAR_1": "value_one", "TEST_VAR_2": "value_two"},
    "metadata": {"test_run": "h2", "index": "0"},
    "launch_parameters": {"resource_size_request": "SMALL", "keep_alive_time_seconds": 300},
}


def percentile(sorted_vals: list[float], p: float) -> float:
    idx = math.ceil(p / 100 * len(sorted_vals)) - 1
    return sorted_vals[max(0, idx)]


async def send_request(client: httpx.AsyncClient) -> dict[str, object]:
    start = time.perf_counter()
    response = await client.post(
        "/v1/devboxes",
        json=BODY,
        headers={"authorization": f"Bearer {API_KEY}"},
    )
    return {"latency_ms": (time.perf_counter() - start) * 1000, "status": response.status_code}


async def main() -> None:
    if NUM_CONNECTIONS < 1:
        print(f'NUM_CONNECTIONS must be a positive integer (got "{os.environ.get("NUM_CONNECTIONS")}")')
        return

    print(f"HTTP/2 test: {REQUEST_COUNT} requests, {NUM_CONNECTIONS} connections to {BASE_URL}")

    # One client per logical connection — each capped at 1 connection so requests
    # are distributed across NUM_CONNECTIONS distinct HTTP/2 sessions.
    clients = [
        httpx.AsyncClient(
            base_url=BASE_URL,
            http2=True,
            limits=httpx.Limits(max_connections=1, max_keepalive_connections=1),
            timeout=httpx.Timeout(120.0),
        )
        for _ in range(NUM_CONNECTIONS)
    ]

    print(f"{NUM_CONNECTIONS} connections established\n")

    completed = 0

    async def progress_printer() -> None:
        while True:
            await asyncio.sleep(2)
            pct = completed / REQUEST_COUNT * 100
            print(f"  progress: {completed}/{REQUEST_COUNT} ({pct:.1f}%)")

    async def wrapped(idx: int) -> dict[str, object]:
        nonlocal completed
        r = await send_request(clients[idx % NUM_CONNECTIONS])
        completed += 1
        return r

    wall_start = time.perf_counter()
    progress_task = asyncio.create_task(progress_printer())
    results = await asyncio.gather(*(wrapped(i) for i in range(REQUEST_COUNT)))
    progress_task.cancel()
    wall_ms = (time.perf_counter() - wall_start) * 1000

    for c in clients:
        await c.aclose()

    latencies: list[float] = sorted(cast(float, r["latency_ms"]) for r in results)
    status_counts: dict[int, int] = {}
    for r in results:
        s = cast(int, r["status"])
        status_counts[s] = status_counts.get(s, 0) + 1

    print(f"\n=== HTTP/2 Results ===")
    print(f"Requests:    {REQUEST_COUNT}")
    print(f"Connections: {NUM_CONNECTIONS}")
    print(f"Wall clock:  {wall_ms / 1000:.2f}s")
    print(f"Throughput:  {REQUEST_COUNT / (wall_ms / 1000):.1f} req/s")
    if latencies:
        print("\nLatency (ms):")
        print(f"  min: {latencies[0]:.1f}")
        print(f"  p50: {percentile(latencies, 50):.1f}")
        print(f"  p90: {percentile(latencies, 90):.1f}")
        print(f"  p95: {percentile(latencies, 95):.1f}")
        print(f"  p99: {percentile(latencies, 99):.1f}")
        print(f"  max: {latencies[-1]:.1f}")
    print("\nStatus codes:")
    for s, c_count in sorted(status_counts.items()):
        print(f"  {s}: {c_count}")


if __name__ == "__main__":
    asyncio.run(main())
