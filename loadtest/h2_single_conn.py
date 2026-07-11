"""Raw httpx HTTP/2 single-connection burst: 50 requests on one warmed connection."""

from __future__ import annotations

import asyncio
import os
import time
from typing import cast

import httpx

BASE_URL = os.environ.get("RUNLOOP_BASE_URL", "https://api.runloop.ai")
API_KEY = os.environ["RUNLOOP_API_KEY"]

BODY = {
    "blueprint_id": "bp_nonexistent_loadtest_00000",
    "name": "loadtest-h2s-0",
    "environment_variables": {"TEST_VAR_1": "value_one"},
    "launch_parameters": {"resource_size_request": "SMALL"},
}


async def send_request(client: httpx.AsyncClient) -> dict[str, object]:
    start = time.perf_counter()
    response = await client.post(
        "/v1/devboxes",
        json=BODY,
        headers={"authorization": f"Bearer {API_KEY}"},
    )
    return {"latency_ms": (time.perf_counter() - start) * 1000, "status": response.status_code}


async def main() -> None:
    client = httpx.AsyncClient(
        base_url=BASE_URL,
        http2=True,
        limits=httpx.Limits(max_connections=1, max_keepalive_connections=1),
        timeout=httpx.Timeout(120.0),
    )

    # Warmup
    w = await send_request(client)
    print(f"Warmup: status={w['status']}, latency={w['latency_ms']:.0f}ms")

    count = 50
    print(f"\nBursting {count} requests on 1 warmed connection...")
    wall_start = time.perf_counter()
    results = await asyncio.gather(*(send_request(client) for _ in range(count)))
    wall_ms = (time.perf_counter() - wall_start) * 1000

    await client.aclose()

    lats: list[float] = sorted(cast(float, r["latency_ms"]) for r in results)
    print(f"{count} requests in {wall_ms:.0f}ms ({count / (wall_ms / 1000):.1f} req/s)")
    print(
        f"Latency: min={lats[0]:.0f}ms  p50={lats[count // 2]:.0f}ms  max={lats[-1]:.0f}ms"
    )


if __name__ == "__main__":
    asyncio.run(main())
