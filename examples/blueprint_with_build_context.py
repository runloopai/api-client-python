#!/usr/bin/env -S uv run python
"""
---
title: Blueprint with Build Context
slug: blueprint-with-build-context
use_case: Create a blueprint using the object store to provide docker build context files, then verify files are copied into the image. Uses the async SDK.
workflow:
  - Create a temporary directory with sample application files
  - Upload the directory to object storage as build context
  - Create a blueprint with a Dockerfile that copies the context files
  - Create a devbox from the blueprint
  - Verify the files were copied into the image
  - Shutdown devbox and delete blueprint and storage object
tags:
  - blueprint
  - object-store
  - build-context
  - devbox
  - cleanup
  - async
prerequisites:
  - RUNLOOP_API_KEY
run: uv run python -m examples.blueprint_with_build_context
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from datetime import timedelta

from runloop_api_client import AsyncRunloopSDK
from runloop_api_client.lib.polling import PollingConfig

from ._harness import run_as_cli, unique_name, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

# building can take time: make sure to set a long blueprint build timeout
BLUEPRINT_POLL_TIMEOUT_S = 10 * 60
BLUEPRINT_POLL_MAX_ATTEMPTS = 600

# configure object storage ttl for the build context
BUILD_CONTEXT_TTL = timedelta(hours=1)


async def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a blueprint with build context from object storage, then verify files in a devbox."""
    cleanup = ctx.cleanup

    sdk = AsyncRunloopSDK()

    # setup: create a temporary directory with sample application files to use as build context
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        (tmp_path / "app.py").write_text('print("Hello from app")')
        (tmp_path / "config.txt").write_text("key=value")

        # upload the build context to object storage
        storage_obj = await sdk.storage_object.upload_from_dir(
            tmp_path,
            name=unique_name("example-build-context"),
            ttl=BUILD_CONTEXT_TTL,
        )
        cleanup.add(f"storage_object:{storage_obj.id}", storage_obj.delete)

        # create a blueprint with the build context
        blueprint = await sdk.blueprint.create(
            name=unique_name("example-blueprint-context"),
            dockerfile="FROM ubuntu:22.04\nWORKDIR /app\nCOPY . .",
            build_context=storage_obj.as_build_context(),
            polling_config=PollingConfig(
                timeout_seconds=BLUEPRINT_POLL_TIMEOUT_S,
                max_attempts=BLUEPRINT_POLL_MAX_ATTEMPTS,
            ),
        )
        cleanup.add(f"blueprint:{blueprint.id}", blueprint.delete)

        devbox = await blueprint.create_devbox(
            name=unique_name("example-devbox"),
            launch_parameters={
                "resource_size_request": "X_SMALL",
                "keep_alive_time_seconds": 60 * 5,
            },
        )
        cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

        app_result = await devbox.cmd.exec("cat /app/app.py")
        app_stdout = await app_result.stdout()

        config_result = await devbox.cmd.exec("cat /app/config.txt")
        config_stdout = await config_result.stdout()

        return RecipeOutput(
            resources_created=[
                f"storage_object:{storage_obj.id}",
                f"blueprint:{blueprint.id}",
                f"devbox:{devbox.id}",
            ],
            checks=[
                ExampleCheck(
                    name="app.py exists and readable",
                    passed=app_result.exit_code == 0,
                    details=f"exitCode={app_result.exit_code}",
                ),
                ExampleCheck(
                    name="app.py contains expected content",
                    passed='print("Hello from app")' in app_stdout,
                    details=app_stdout.strip(),
                ),
                ExampleCheck(
                    name="config.txt exists and readable",
                    passed=config_result.exit_code == 0,
                    details=f"exitCode={config_result.exit_code}",
                ),
                ExampleCheck(
                    name="config.txt contains expected content",
                    passed="key=value" in config_stdout,
                    details=config_stdout.strip(),
                ),
            ],
        )


run_blueprint_with_build_context_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_blueprint_with_build_context_example)
