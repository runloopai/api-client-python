#!/usr/bin/env -S uv run python
"""
---
title: Devbox Snapshot and Resume
slug: devbox-snapshot-resume
use_case: Create a devbox, snapshot its disk, resume from the snapshot, and demonstrate that changes in the original devbox do not affect the clone. Uses the async SDK.
workflow:
  - Create a devbox
  - Write a file to the devbox
  - Create a disk snapshot
  - Create a new devbox from the snapshot
  - Modify the file on the original devbox
  - Verify the clone has the original content
  - Shutdown both devboxes and delete the snapshot
tags:
  - devbox
  - snapshot
  - resume
  - cleanup
  - async
prerequisites:
  - RUNLOOP_API_KEY
run: uv run python -m examples.devbox_snapshot_resume
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

from runloop_api_client import AsyncRunloopSDK

from ._harness import run_as_cli, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

FILE_PATH = "/home/user/welcome.txt"
ORIGINAL_CONTENT = "hello world!"
MODIFIED_CONTENT = "original devbox has changed the welcome message"


async def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a devbox, snapshot it, resume from snapshot, and verify state isolation."""
    cleanup = ctx.cleanup

    sdk = AsyncRunloopSDK()

    # Create a devbox
    dbx_original = await sdk.devbox.create(
        name="dbx_original",
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    cleanup.add(f"devbox:{dbx_original.id}", dbx_original.shutdown)

    # Write a file to the original devbox
    await dbx_original.file.write(FILE_PATH, ORIGINAL_CONTENT)

    # Read and display the file contents
    cat_original_before = await dbx_original.cmd.exec(f"cat {FILE_PATH}")
    original_content_before = await cat_original_before.stdout()

    # Create a disk snapshot of the original devbox
    snapshot = await dbx_original.snapshot_disk(name="my-snapshot")
    cleanup.add(f"snapshot:{snapshot.id}", snapshot.delete)

    # Create a new devbox from the snapshot
    dbx_clone = await sdk.devbox.create_from_snapshot(
        snapshot.id,
        name="dbx_clone",
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    cleanup.add(f"devbox:{dbx_clone.id}", dbx_clone.shutdown)

    # Modify the file on the original devbox
    await dbx_original.file.write(FILE_PATH, MODIFIED_CONTENT)

    # Read the file contents from both devboxes
    cat_clone = await dbx_clone.cmd.exec(f"cat {FILE_PATH}")
    clone_content = await cat_clone.stdout()

    # now the original devbox has been modified but the clone has the original message
    cat_original_after = await dbx_original.cmd.exec(f"cat {FILE_PATH}")
    original_content_after = await cat_original_after.stdout()

    return RecipeOutput(
        resources_created=[
            f"devbox:{dbx_original.id}",
            f"snapshot:{snapshot.id}",
            f"devbox:{dbx_clone.id}",
        ],
        checks=[
            ExampleCheck(
                name="original devbox file created successfully",
                passed=cat_original_before.exit_code == 0 and original_content_before.strip() == ORIGINAL_CONTENT,
                details=f'content="{original_content_before.strip()}"',
            ),
            ExampleCheck(
                name="snapshot created successfully",
                passed=bool(snapshot.id),
                details=f"snapshotId={snapshot.id}",
            ),
            ExampleCheck(
                name="clone devbox created from snapshot",
                passed=bool(dbx_clone.id),
                details=f"cloneId={dbx_clone.id}",
            ),
            ExampleCheck(
                name="clone has original file content (before modification)",
                passed=cat_clone.exit_code == 0 and clone_content.strip() == ORIGINAL_CONTENT,
                details=f'cloneContent="{clone_content.strip()}"',
            ),
            ExampleCheck(
                name="original devbox has modified content",
                passed=cat_original_after.exit_code == 0 and original_content_after.strip() == MODIFIED_CONTENT,
                details=f'originalContent="{original_content_after.strip()}"',
            ),
            ExampleCheck(
                name="clone and original have divergent state",
                passed=clone_content.strip() != original_content_after.strip(),
                details=f'clone="{clone_content.strip()}" vs original="{original_content_after.strip()}"',
            ),
        ],
    )


run_devbox_snapshot_resume_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_snapshot_resume_example)
