#!/usr/bin/env -S uv run python
"""
---
title: Devbox Snapshots (Suspend, Resume, Restore, Delete)
slug: devbox-snapshots
use_case: Upload a file to a devbox, preserve it across suspend and resume, create a disk snapshot, restore multiple devboxes from that snapshot, mutate each copy independently, and delete the snapshot when finished.
workflow:
  - Create a source devbox
  - Upload a file and mutate it into a shared baseline
  - Suspend and resume the source devbox
  - Create a disk snapshot from the resumed devbox
  - Restore two additional devboxes from the same snapshot baseline
  - Mutate the same file differently in each devbox to prove isolation
  - Shutdown the devboxes and delete the snapshot
tags:
  - devbox
  - snapshot
  - suspend
  - resume
  - files
  - cleanup
prerequisites:
  - RUNLOOP_API_KEY
run: uv run python -m examples.devbox_snapshots
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from runloop_api_client import AsyncRunloopSDK
from runloop_api_client.lib.polling import PollingConfig
from runloop_api_client.sdk.async_devbox import AsyncDevbox
from runloop_api_client.sdk.async_snapshot import AsyncSnapshot

from ._harness import run_as_cli, unique_name, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

FILE_PATH = "/tmp/snapshot-demo.txt"
POLLING_CONFIG = PollingConfig(timeout_seconds=120.0, interval_seconds=5.0)


async def read_file_contents(devbox: AsyncDevbox) -> str:
    """Read the shared demo file from a devbox."""
    return await devbox.file.read(file_path=FILE_PATH)


async def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Demonstrate suspend/resume and shared snapshot restoration with isolated mutations."""
    cleanup = ctx.cleanup
    sdk = AsyncRunloopSDK()

    resources_created: list[str] = []

    source_devbox: AsyncDevbox | None = None
    clone_a: AsyncDevbox | None = None
    clone_b: AsyncDevbox | None = None
    snapshot: AsyncSnapshot | None = None
    local_file_path: Path | None = None

    source_needs_cleanup = False
    clone_a_needs_cleanup = False
    clone_b_needs_cleanup = False
    snapshot_needs_cleanup = False

    async def cleanup_source() -> None:
        if source_needs_cleanup and source_devbox is not None:
            await source_devbox.shutdown()

    async def cleanup_clone_a() -> None:
        if clone_a_needs_cleanup and clone_a is not None:
            await clone_a.shutdown()

    async def cleanup_clone_b() -> None:
        if clone_b_needs_cleanup and clone_b is not None:
            await clone_b.shutdown()

    async def cleanup_snapshot() -> None:
        if snapshot_needs_cleanup and snapshot is not None:
            await snapshot.delete()

    def cleanup_local_file() -> None:
        if local_file_path is not None:
            local_file_path.unlink(missing_ok=True)

    # Cleanup runs in LIFO order, so register these handlers up front in reverse
    # dependency order: clones, then source devbox, then snapshot, then local file.
    cleanup.add("local-file:snapshot-demo", cleanup_local_file)
    cleanup.add("snapshot:baseline", cleanup_snapshot)
    cleanup.add("devbox:source", cleanup_source)
    cleanup.add("devbox:clone-a", cleanup_clone_a)
    cleanup.add("devbox:clone-b", cleanup_clone_b)

    uploaded_contents = "uploaded-from-local-file"
    baseline_contents = "baseline-after-upload-and-mutation"
    source_contents = "source-devbox-after-isolated-mutation"
    clone_a_contents = "clone-a-after-isolated-mutation"
    clone_b_contents = "clone-b-after-isolated-mutation"

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(uploaded_contents)
        local_file_path = Path(tmp_file.name)

    source_devbox = await sdk.devbox.create(
        name=unique_name("snapshot-source"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
        },
    )
    source_needs_cleanup = True
    resources_created.append(f"devbox:{source_devbox.id}")

    await source_devbox.file.upload(path=FILE_PATH, file=local_file_path)
    uploaded_readback = await read_file_contents(source_devbox)

    await source_devbox.file.write(file_path=FILE_PATH, contents=baseline_contents)

    suspend_response = await source_devbox.suspend()
    suspended_info = suspend_response
    if suspended_info.status != "suspended":
        suspended_info = await source_devbox.await_suspended(polling_config=POLLING_CONFIG)

    resumed_info = await source_devbox.resume(polling_config=POLLING_CONFIG)
    resumed_readback = await read_file_contents(source_devbox)

    snapshot = await source_devbox.snapshot_disk(
        name=unique_name("snapshot-baseline"),
        commit_message="Capture the shared baseline after suspend and resume.",
        polling_config=POLLING_CONFIG,
    )
    snapshot_needs_cleanup = True
    resources_created.append(f"snapshot:{snapshot.id}")

    clone_a = await snapshot.create_devbox(
        name=unique_name("snapshot-clone-a"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
        },
    )
    clone_a_needs_cleanup = True
    resources_created.append(f"devbox:{clone_a.id}")

    clone_b = await sdk.devbox.create_from_snapshot(
        snapshot.id,
        name=unique_name("snapshot-clone-b"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
        },
    )
    clone_b_needs_cleanup = True
    resources_created.append(f"devbox:{clone_b.id}")

    clone_a_baseline_readback = await read_file_contents(clone_a)
    clone_b_baseline_readback = await read_file_contents(clone_b)

    await source_devbox.file.write(file_path=FILE_PATH, contents=source_contents)
    await clone_a.file.write(file_path=FILE_PATH, contents=clone_a_contents)
    await clone_b.file.write(file_path=FILE_PATH, contents=clone_b_contents)

    source_isolated_readback = await read_file_contents(source_devbox)
    clone_a_isolated_readback = await read_file_contents(clone_a)
    clone_b_isolated_readback = await read_file_contents(clone_b)

    await clone_b.shutdown()
    clone_b_needs_cleanup = False

    await clone_a.shutdown()
    clone_a_needs_cleanup = False

    await source_devbox.shutdown()
    source_needs_cleanup = False

    await snapshot.delete()
    snapshot_needs_cleanup = False

    return RecipeOutput(
        resources_created=resources_created,
        checks=[
            ExampleCheck(
                name="uploaded file is readable on the source devbox",
                passed=uploaded_readback == uploaded_contents,
                details=uploaded_readback,
            ),
            ExampleCheck(
                name="suspend reaches the suspended state",
                passed=suspended_info.status == "suspended",
                details=f"status={suspended_info.status}",
            ),
            ExampleCheck(
                name="resume preserves the baseline file contents",
                passed=resumed_info.status == "running" and resumed_readback == baseline_contents,
                details=f"status={resumed_info.status}, contents={resumed_readback}",
            ),
            ExampleCheck(
                name="multiple devboxes can use the same snapshot baseline",
                passed=(
                    clone_a_baseline_readback == baseline_contents and clone_b_baseline_readback == baseline_contents
                ),
                details=(f"clone_a={clone_a_baseline_readback}, clone_b={clone_b_baseline_readback}"),
            ),
            ExampleCheck(
                name="devboxes diverge after isolated mutations",
                passed=(
                    source_isolated_readback == source_contents
                    and clone_a_isolated_readback == clone_a_contents
                    and clone_b_isolated_readback == clone_b_contents
                ),
                details=(
                    "source="
                    f"{source_isolated_readback}, "
                    f"clone_a={clone_a_isolated_readback}, "
                    f"clone_b={clone_b_isolated_readback}"
                ),
            ),
            ExampleCheck(
                name="snapshot-backed devboxes stay isolated from one another",
                passed=(
                    len(
                        {
                            source_isolated_readback,
                            clone_a_isolated_readback,
                            clone_b_isolated_readback,
                        }
                    )
                    == 3
                ),
                details=(f"values={[source_isolated_readback, clone_a_isolated_readback, clone_b_isolated_readback]}"),
            ),
            ExampleCheck(
                name="snapshot can be deleted after the demo finishes",
                passed=not snapshot_needs_cleanup,
                details=f"deleted={not snapshot_needs_cleanup}",
            ),
        ],
    )


run_devbox_snapshots_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_snapshots_example)
