#!/usr/bin/env -S uv run python
"""
---
title: Secrets with Devbox (Create, Inject, Verify, Delete)
slug: secrets-with-devbox
use_case: Create a secret, inject it into a devbox as an environment variable, verify access, and clean up.
workflow:
  - Create a secret with a test value
  - Create a devbox with the secret mapped to an env var
  - Execute a command that reads the secret from the environment
  - Verify the value matches
  - Update the secret and verify
  - List secrets and verify the secret appears
  - Shutdown devbox and delete secret
tags:
  - secrets
  - devbox
  - environment-variables
  - cleanup
prerequisites:
  - RUNLOOP_API_KEY
run: uv run python -m examples.secrets_with_devbox
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

from runloop_api_client import RunloopSDK

from ._harness import run_as_cli, unique_name, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

# Note: do NOT hardcode secret values in your code!
# This is example code only; use environment variables instead!
_EXAMPLE_SECRET_VALUE = "my-secret-value"
_UPDATED_SECRET_VALUE = "updated-secret-value"


def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a secret, inject it into a devbox, and verify it is accessible."""
    cleanup = ctx.cleanup

    sdk = RunloopSDK()
    resources_created: list[str] = []
    checks: list[ExampleCheck] = []

    secret_name = unique_name("RUNLOOP_SDK_EXAMPLE").upper().replace("-", "_")

    secret = sdk.secret.create(name=secret_name, value=_EXAMPLE_SECRET_VALUE)
    resources_created.append(f"secret:{secret_name}")
    cleanup.add(f"secret:{secret_name}", lambda: secret.delete())

    secret_info = secret.get_info()
    checks.append(
        ExampleCheck(
            name="secret created successfully",
            passed=secret.name == secret_name and secret_info.id.startswith("sec_"),
            details=f"name={secret.name}, id={secret_info.id}",
        )
    )

    devbox = sdk.devbox.create(
        name=unique_name("secrets-example-devbox"),
        secrets={
            "MY_SECRET_ENV": secret.name,
        },
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    resources_created.append(f"devbox:{devbox.id}")
    cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

    result = devbox.cmd.exec("echo $MY_SECRET_ENV")
    stdout = result.stdout().strip()
    checks.append(
        ExampleCheck(
            name="devbox can read secret as env var",
            passed=result.exit_code == 0 and stdout == _EXAMPLE_SECRET_VALUE,
            details=f'exit_code={result.exit_code}, stdout="{stdout}"',
        )
    )

    updated_info = sdk.secret.update(secret, _UPDATED_SECRET_VALUE).get_info()
    checks.append(
        ExampleCheck(
            name="secret updated successfully",
            passed=updated_info.name == secret_name,
            details=f"update_time_ms={updated_info.update_time_ms}",
        )
    )

    secrets = sdk.secret.list()
    found = next((s for s in secrets if s.name == secret_name), None)
    checks.append(
        ExampleCheck(
            name="secret appears in list",
            passed=found is not None,
            details=f"found name={found.name}" if found else "not found",
        )
    )

    return RecipeOutput(resources_created=resources_created, checks=checks)


run_secrets_with_devbox_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_secrets_with_devbox_example)
