#!/usr/bin/env -S uv run python
"""
---
title: Devbox From Blueprint (Run Command, Shutdown)
slug: devbox-from-blueprint-lifecycle
use_case: Create a devbox from a blueprint, run a command, fetch logs, validate output, and cleanly tear everything down.
workflow:
  - Create a blueprint
  - Fetch blueprint build logs
  - Create a devbox from the blueprint
  - Execute a command in the devbox
  - Fetch devbox logs
  - Validate exit code, stdout, and logs
  - Shutdown devbox and delete blueprint
tags:
  - devbox
  - blueprint
  - commands
  - logs
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
    """Create a devbox from a blueprint, run a command, fetch logs, and clean up."""
    cleanup = ctx.cleanup

    sdk = RunloopSDK()

    blueprint = sdk.blueprint.create(
        name=unique_name("example-blueprint"),
        dockerfile='FROM ubuntu:22.04\nRUN echo "Hello from your blueprint"',
        polling_config=PollingConfig(timeout_seconds=BLUEPRINT_POLL_TIMEOUT_S),
    )
    cleanup.add(f"blueprint:{blueprint.id}", blueprint.delete)

    # Fetch blueprint build logs
    blueprint_logs = blueprint.logs()

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

    # Fetch devbox logs
    devbox_logs = devbox.logs()

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
            ExampleCheck(
                name="blueprint build logs are retrievable",
                passed=blueprint_logs is not None and hasattr(blueprint_logs, "logs"),
                details=f"blueprint_log_count={len(blueprint_logs.logs)}",
            ),
            ExampleCheck(
                name="devbox logs are retrievable",
                passed=devbox_logs is not None and hasattr(devbox_logs, "logs"),
                details=f"devbox_log_count={len(devbox_logs.logs)}",
            ),
        ],
    )


run_devbox_from_blueprint_lifecycle_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_from_blueprint_lifecycle_example)
