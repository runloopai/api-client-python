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

from ._harness import run_as_cli, unique_name, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

FILE_PATH = "/tmp/snapshot-demo.txt"
POLLING_CONFIG = PollingConfig(timeout_seconds=120.0, interval_seconds=5.0)


async def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Demonstrate suspend/resume and shared snapshot restoration with isolated mutations."""
    cleanup = ctx.cleanup
    sdk = AsyncRunloopSDK()

    resources_created: list[str] = []

    uploaded_contents = "uploaded-from-local-file"
    baseline_contents = "baseline-after-upload-and-mutation"
    source_contents = "source-devbox-after-isolated-mutation"
    clone_a_contents = "clone-a-after-isolated-mutation"
    clone_b_contents = "clone-b-after-isolated-mutation"

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(uploaded_contents)
        local_file_path = Path(tmp_file.name)
    cleanup.add("local-file:snapshot-demo", lambda: local_file_path.unlink(missing_ok=True))

    source_devbox = await sdk.devbox.create(
        name=unique_name("snapshot-source"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    cleanup.add(f"devbox:{source_devbox.id}", source_devbox.shutdown)
    resources_created.append(f"devbox:{source_devbox.id}")

    await source_devbox.file.upload(path=FILE_PATH, file=local_file_path)
    uploaded_readback = await source_devbox.file.read(file_path=FILE_PATH)

    await source_devbox.file.write(file_path=FILE_PATH, contents=baseline_contents)

    await source_devbox.suspend()
    suspended_info = await source_devbox.await_suspended(polling_config=POLLING_CONFIG)

    resumed_info = await source_devbox.resume(polling_config=POLLING_CONFIG)
    resumed_readback = await source_devbox.file.read(file_path=FILE_PATH)

    snapshot = await source_devbox.snapshot_disk(
        name=unique_name("snapshot-baseline"),
        commit_message="Capture the shared baseline after suspend and resume.",
        polling_config=POLLING_CONFIG,
    )
    cleanup.add(f"snapshot:{snapshot.id}", snapshot.delete)
    resources_created.append(f"snapshot:{snapshot.id}")

    clone_a = await snapshot.create_devbox(
        name=unique_name("snapshot-clone-a"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    cleanup.add(f"devbox:{clone_a.id}", clone_a.shutdown)
    resources_created.append(f"devbox:{clone_a.id}")

    # clone_a used snapshot.create_devbox(); clone_b uses sdk.devbox.create_from_snapshot()
    # to demonstrate both entry points for restoring a devbox from a snapshot.
    clone_b = await sdk.devbox.create_from_snapshot(
        snapshot.id,
        name=unique_name("snapshot-clone-b"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    cleanup.add(f"devbox:{clone_b.id}", clone_b.shutdown)
    resources_created.append(f"devbox:{clone_b.id}")

    clone_a_baseline_readback = await clone_a.file.read(file_path=FILE_PATH)
    clone_b_baseline_readback = await clone_b.file.read(file_path=FILE_PATH)

    await source_devbox.file.write(file_path=FILE_PATH, contents=source_contents)
    await clone_a.file.write(file_path=FILE_PATH, contents=clone_a_contents)
    await clone_b.file.write(file_path=FILE_PATH, contents=clone_b_contents)

    source_isolated_readback = await source_devbox.file.read(file_path=FILE_PATH)
    clone_a_isolated_readback = await clone_a.file.read(file_path=FILE_PATH)
    clone_b_isolated_readback = await clone_b.file.read(file_path=FILE_PATH)

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
        ],
    )


run_devbox_snapshots_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_snapshots_example)
