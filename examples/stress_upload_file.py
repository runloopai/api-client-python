#!/usr/bin/env -S uv run python
"""Stress test for AsyncRunloop.devboxes.upload_file.

Reproduces the 408 "Request timed out waiting for request data" pattern seen
in production when many upload_file calls run concurrently through a single
SDK client (shared httpx connection pool).

Usage:

    export RUNLOOP_API_KEY=...

    # Repro path: create a devbox, fire 200 uploads with 50 in flight at once.
    ./examples/stress_upload_file.py --concurrency 50 --total 200

    # Reuse an existing devbox instead of creating one:
    ./examples/stress_upload_file.py --devbox-id dbx_abc... --total 200

    # Tune file size and SDK retry behavior:
    ./examples/stress_upload_file.py --file-size-kb 256 --max-retries 0
"""

from __future__ import annotations

import os
import sys
import time
import asyncio
import argparse
import tempfile
import statistics
from pathlib import Path
from dataclasses import dataclass

import httpx

from runloop_api_client import AsyncRunloop
from runloop_api_client._exceptions import APIStatusError


@dataclass
class UploadResult:
    index: int
    started_at: float
    finished_at: float
    status: str  # "ok", "408", "other_error"
    detail: str = ""

    @property
    def duration_ms(self) -> float:
        return (self.finished_at - self.started_at) * 1000.0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--devbox-id", default=os.environ.get("RUNLOOP_DEVBOX_ID"),
                   help="Reuse an existing devbox (default: create a new one)")
    p.add_argument("--base-url", default=os.environ.get("RUNLOOP_BASE_URL"),
                   help="Override Runloop API base URL")
    p.add_argument("--concurrency", type=int, default=50,
                   help="Number of upload_file calls in flight at once (default: 50)")
    p.add_argument("--total", type=int, default=200,
                   help="Total number of uploads to perform (default: 200)")
    p.add_argument("--file-size-kb", type=int, default=64,
                   help="Size of each uploaded file in KB (default: 64)")
    p.add_argument("--max-retries", type=int, default=None,
                   help="Override SDK max_retries (default: SDK default of 5)")
    p.add_argument("--max-connections", type=int, default=None,
                   help="Override SDK max_connections via connection_limits (default: SDK default of 100)")
    p.add_argument("--max-keepalive", type=int, default=None,
                   help="Override max_keepalive_connections (only meaningful with --max-connections)")
    p.add_argument("--shutdown", action="store_true",
                   help="Shut down the devbox after the run (only if we created it)")
    p.add_argument("--blueprint-name", default=None,
                   help="Blueprint to launch from when creating a devbox")
    return p.parse_args()


async def ensure_devbox(client: AsyncRunloop, args: argparse.Namespace) -> tuple[str, bool]:
    """Return (devbox_id, created_by_us)."""
    if args.devbox_id:
        print(f"[setup] reusing devbox {args.devbox_id}")
        return args.devbox_id, False

    print("[setup] creating a new devbox for the stress run...")
    kwargs: dict[str, object] = {}
    if args.blueprint_name:
        kwargs["blueprint_name"] = args.blueprint_name
    devbox = await client.devboxes.create_and_await_running(**kwargs)  # type: ignore[arg-type]
    print(f"[setup] devbox {devbox.id} is running")
    return devbox.id, True


async def one_upload(
    client: AsyncRunloop,
    devbox_id: str,
    src_path: Path,
    index: int,
    sem: asyncio.Semaphore,
) -> UploadResult:
    async with sem:
        started = time.monotonic()
        try:
            await client.devboxes.upload_file(
                devbox_id,
                path=f"/tmp/stress_{index}.bin",
                file=src_path,
            )
            return UploadResult(index=index, started_at=started, finished_at=time.monotonic(), status="ok")
        except APIStatusError as exc:
            if exc.status_code == 408:
                status = "408"
            else:
                status = f"http_{exc.status_code}"
            return UploadResult(
                index=index,
                started_at=started,
                finished_at=time.monotonic(),
                status=status,
                detail=str(exc)[:200],
            )
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            return UploadResult(
                index=index,
                started_at=started,
                finished_at=time.monotonic(),
                status=f"transport_{type(exc).__name__}",
                detail=str(exc)[:200],
            )


def summarize(results: list[UploadResult], wall_seconds: float) -> int:
    by_status: dict[str, list[UploadResult]] = {}
    for r in results:
        by_status.setdefault(r.status, []).append(r)

    print()
    print("=" * 72)
    print(f"Total uploads:       {len(results)}")
    print(f"Wall time:           {wall_seconds:.1f}s")
    print(f"Effective throughput:{len(results) / wall_seconds:.2f} uploads/s")
    print()
    print("Outcome breakdown:")
    for status in sorted(by_status):
        bucket = by_status[status]
        durations = sorted(r.duration_ms for r in bucket)
        p50 = statistics.median(durations)
        p95 = durations[int(0.95 * (len(durations) - 1))]
        p99 = durations[int(0.99 * (len(durations) - 1))]
        print(f"  {status:>20}  count={len(bucket):>5}  p50={p50:>8.0f}ms  p95={p95:>8.0f}ms  p99={p99:>8.0f}ms")

    sample_408 = by_status.get("408", [])[:3]
    if sample_408:
        print()
        print("Sample 408 errors:")
        for r in sample_408:
            print(f"  #{r.index} duration={r.duration_ms:.0f}ms detail={r.detail}")

    success = len(by_status.get("ok", []))
    return 0 if success == len(results) else 1


async def run() -> int:
    args = parse_args()

    if "RUNLOOP_API_KEY" not in os.environ:
        print("error: RUNLOOP_API_KEY is required", file=sys.stderr)
        return 2

    client_kwargs: dict[str, object] = {}
    if args.base_url:
        client_kwargs["base_url"] = args.base_url
    if args.max_retries is not None:
        client_kwargs["max_retries"] = args.max_retries
    if args.max_connections is not None:
        limits_kwargs: dict[str, int] = {"max_connections": args.max_connections}
        if args.max_keepalive is not None:
            limits_kwargs["max_keepalive_connections"] = args.max_keepalive
        client_kwargs["connection_limits"] = httpx.Limits(**limits_kwargs)

    payload = os.urandom(args.file_size_kb * 1024)
    with tempfile.NamedTemporaryFile(prefix="rl-stress-", suffix=".bin", delete=False) as f:
        f.write(payload)
        src_path = Path(f.name)
    print(f"[setup] payload: {src_path} ({len(payload)} bytes)")

    try:
        async with AsyncRunloop(**client_kwargs) as client:  # type: ignore[arg-type]
            devbox_id, created = await ensure_devbox(client, args)

            print(
                f"[run] firing {args.total} upload_file calls "
                f"(concurrency={args.concurrency}) to {devbox_id}"
            )
            sem = asyncio.Semaphore(args.concurrency)
            t0 = time.monotonic()
            results = await asyncio.gather(
                *(one_upload(client, devbox_id, src_path, i, sem) for i in range(args.total))
            )
            wall = time.monotonic() - t0

            exit_code = summarize(results, wall)

            if created and args.shutdown:
                print(f"[teardown] shutting down devbox {devbox_id}")
                await client.devboxes.shutdown(devbox_id)
    finally:
        try:
            src_path.unlink()
        except OSError:
            pass

    return exit_code


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
