"""Raw httpx HTTP/1.1 keep-alive baseline."""

from __future__ import annotations

import asyncio
import math
import os
import time

import httpx

REQUEST_COUNT = int(os.environ.get("REQUEST_COUNT", "500"))
NUM_CONNECTIONS = int(os.environ.get("NUM_CONNECTIONS", "20"))
BASE_URL = os.environ.get("RUNLOOP_BASE_URL", "https://api.runloop.ai")
API_KEY = os.environ["RUNLOOP_API_KEY"]

BODY = {
    "blueprint_id": "bp_nonexistent_loadtest_00000",
    "name": "loadtest-raw-0",
    "environment_variables": {"TEST_VAR_1": "value_one", "TEST_VAR_2": "value_two"},
    "metadata": {"test_run": "raw", "index": "0"},
    "launch_parameters": {"resource_size_request": "SMALL", "keep_alive_time_seconds": 300},
}


def percentile(sorted_vals: list[float], p: float) -> float:
    idx = math.ceil(p / 100 * len(sorted_vals)) - 1
    return sorted_vals[max(0, idx)]


async def main() -> None:
    print(f"HTTP/1.1 test: {REQUEST_COUNT} requests, {NUM_CONNECTIONS} keep-alive connections to {BASE_URL}")

    client = httpx.AsyncClient(
        base_url=BASE_URL,
        http2=False,
        limits=httpx.Limits(max_connections=NUM_CONNECTIONS, max_keepalive_connections=NUM_CONNECTIONS),
        timeout=httpx.Timeout(120.0),
    )

    completed = 0

    async def progress_printer() -> None:
        while True:
            await asyncio.sleep(2)
            pct = completed / REQUEST_COUNT * 100
            print(f"  progress: {completed}/{REQUEST_COUNT} ({pct:.1f}%)")

    async def send_one() -> dict[str, object]:
        nonlocal completed
        start = time.perf_counter()
        status: int | None = None
        try:
            response = await client.post(
                "/v1/devboxes",
                json=BODY,
                headers={"authorization": f"Bearer {API_KEY}"},
            )
            status = response.status_code
        except Exception:
            pass
        finally:
            completed += 1
        return {"latency_ms": (time.perf_counter() - start) * 1000, "status": status}

    wall_start = time.perf_counter()
    progress_task = asyncio.create_task(progress_printer())
    results = await asyncio.gather(*(send_one() for _ in range(REQUEST_COUNT)))
    progress_task.cancel()
    wall_ms = (time.perf_counter() - wall_start) * 1000

    await client.aclose()

    latencies = sorted(r["latency_ms"] for r in results)  # type: ignore[arg-type]
    status_counts: dict[str, int] = {}
    for r in results:
        key = str(r["status"]) if r["status"] is not None else "network_error"
        status_counts[key] = status_counts.get(key, 0) + 1

    print(f"\n=== HTTP/1.1 Results ===")
    print(f"Requests:    {REQUEST_COUNT}")
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
