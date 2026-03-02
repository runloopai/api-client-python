#!/usr/bin/env -S uv run python
"""
---
title: Devbox From Blueprint (Run Command, Shutdown)
slug: devbox-from-blueprint-lifecycle
use_case: Create a devbox from a blueprint, run a command, validate output, and cleanly tear everything down.
workflow:
  - Create a blueprint
  - Create a devbox from the blueprint
  - Execute a command in the devbox
  - Validate exit code and stdout
  - Shutdown devbox and delete blueprint
tags:
  - devbox
  - blueprint
  - commands
  - cleanup
prerequisites:
  - RUNLOOP_API_KEY
run: uv run python -m examples.devbox_from_blueprint_lifecycle
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

from runloop_api_client import RunloopSDK
from runloop_api_client.lib.polling import PollingConfig

from ._harness import run_as_cli, unique_name, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

BLUEPRINT_POLL_TIMEOUT_S = 10 * 60


def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a devbox from a blueprint, run a command, and clean up."""
    cleanup = ctx.cleanup

    sdk = RunloopSDK()

    blueprint = sdk.blueprint.create(
        name=unique_name("example-blueprint"),
        dockerfile='FROM ubuntu:22.04\nRUN echo "Hello from your blueprint"',
        polling_config=PollingConfig(timeout_seconds=BLUEPRINT_POLL_TIMEOUT_S),
    )
    cleanup.add(f"blueprint:{blueprint.id}", blueprint.delete)

    devbox = blueprint.create_devbox(
        name=unique_name("example-devbox"),
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

    result = devbox.cmd.exec('echo "Hello from your devbox"')
    stdout = result.stdout()

    return RecipeOutput(
        resources_created=[f"blueprint:{blueprint.id}", f"devbox:{devbox.id}"],
        checks=[
            ExampleCheck(
                name="command exits successfully",
                passed=result.exit_code == 0,
                details=f"exitCode={result.exit_code}",
            ),
            ExampleCheck(
                name="command output contains expected text",
                passed="Hello from your devbox" in stdout,
                details=stdout.strip(),
            ),
        ],
    )


run_devbox_from_blueprint_lifecycle_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_from_blueprint_lifecycle_example)
