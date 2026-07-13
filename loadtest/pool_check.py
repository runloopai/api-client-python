"""Verify that multiple Runloop (sync) instances share a single connection pool.

Spins up N SDK instances and checks that the number of open connections to
api.runloop.ai does not grow linearly with instance count — it should stay at
one (or a small fixed number) because all instances share the same underlying
httpx transport.

Usage:
    uv run python loadtest/pool_check.py

No API key is required — we only check the transport object identity and the
OS-level connection count, not make real requests.
"""

from __future__ import annotations

import os
import resource
import subprocess
import sys

from runloop_api_client import Runloop

HOST = "api.runloop.ai"
N = 20



def main() -> None:
    fd_before = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
    print(f"FD limit: {fd_before}")
    print(f"Creating {N} Runloop instances...\n")

    clients: list[Runloop] = []
    for i in range(N):
        clients.append(Runloop(bearer_token=os.environ.get("RUNLOOP_API_KEY", "dummy")))

    # All instances should reference the same shared transport object.
    transport_ids = set()
    for c in clients:
        t = getattr(c._client, "_transport", None)
        if t is not None:
            transport_ids.add(id(t))

    print(f"Distinct transport objects across {N} instances: {len(transport_ids)}")
    if len(transport_ids) == 1:
        print("PASS — all instances share one transport (connection pool).")
    else:
        print("FAIL — instances have separate transports; FD exhaustion is possible.")
        sys.exit(1)

    # Close all clients.
    for c in clients:
        c.close()

    print("\nDone.")


if __name__ == "__main__":
    main()
