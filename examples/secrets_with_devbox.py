#!/usr/bin/env -S uv run python
"""
---
title: Secrets with Devbox via Agent Gateway
slug: secrets-with-devbox
use_case: Create a secret, proxy it into a devbox through agent gateway, verify the devbox only gets gateway credentials, and clean up.
workflow:
  - Create a secret with a test credential
  - Create an agent gateway config for an upstream API
  - Launch a devbox with the gateway wired to the secret
  - Verify the devbox receives a gateway URL and token instead of the raw secret
  - Shutdown the devbox and delete the gateway config and secret
tags:
  - secrets
  - devbox
  - agent-gateway
  - credentials
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
_EXAMPLE_GATEWAY_ENDPOINT = "https://api.example.com"
_EXAMPLE_SECRET_VALUE = "example-upstream-api-key"


def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a secret, proxy it through an agent gateway, and verify the devbox only gets gateway credentials."""
    cleanup = ctx.cleanup

    sdk = RunloopSDK()
    resources_created: list[str] = []
    checks: list[ExampleCheck] = []

    secret_name = unique_name("agent-gateway-secret")

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

    # Hide upstream credentials from the devbox by routing requests through an
    # agent gateway config. This prevents direct secret exfiltration.
    gateway_config = sdk.gateway_config.create(
        name=unique_name("agent-gateway-config"),
        endpoint=_EXAMPLE_GATEWAY_ENDPOINT,
        auth_mechanism={"type": "bearer"},
        description="Example gateway that keeps upstream credentials off the devbox",
    )
    resources_created.append(f"gateway_config:{gateway_config.id}")
    cleanup.add(f"gateway_config:{gateway_config.id}", gateway_config.delete)

    gateway_info = gateway_config.get_info()
    checks.append(
        ExampleCheck(
            name="gateway config created successfully",
            passed=(gateway_info.id.startswith("gwc_") and gateway_info.endpoint == _EXAMPLE_GATEWAY_ENDPOINT),
            details=f"id={gateway_info.id}, endpoint={gateway_info.endpoint}",
        )
    )

    devbox = sdk.devbox.create(
        name=unique_name("agent-gateway-devbox"),
        gateways={
            "MY_API": {
                "gateway": gateway_config.id,
                "secret": secret.name,
            }
        },
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
    )
    resources_created.append(f"devbox:{devbox.id}")
    cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

    devbox_info = devbox.get_info()
    checks.append(
        ExampleCheck(
            name="devbox records gateway wiring",
            passed=(
                devbox_info.gateway_specs is not None
                and devbox_info.gateway_specs.get("MY_API") is not None
                and devbox_info.gateway_specs["MY_API"].gateway_config_id == gateway_config.id
            ),
            details=(
                f"gateway_config_id={devbox_info.gateway_specs['MY_API'].gateway_config_id}"
                if devbox_info.gateway_specs is not None and devbox_info.gateway_specs.get("MY_API") is not None
                else "gateway spec missing"
            ),
        )
    )

    url_result = devbox.cmd.exec("echo $MY_API_URL")
    gateway_url = url_result.stdout().strip()
    checks.append(
        ExampleCheck(
            name="devbox receives gateway URL",
            passed=url_result.exit_code == 0 and gateway_url.startswith("http"),
            details=f"exit_code={url_result.exit_code}, url={gateway_url}",
        )
    )

    token_result = devbox.cmd.exec("echo $MY_API")
    gateway_token = token_result.stdout().strip()
    checks.append(
        ExampleCheck(
            name="devbox receives gateway token instead of raw secret",
            passed=(
                token_result.exit_code == 0
                and gateway_token.startswith("gws_")
                and gateway_token != _EXAMPLE_SECRET_VALUE
            ),
            details=(f"exit_code={token_result.exit_code}, token_prefix={gateway_token[:4] or 'missing'}"),
        )
    )

    return RecipeOutput(resources_created=resources_created, checks=checks)


run_secrets_with_devbox_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_secrets_with_devbox_example)
