#!/usr/bin/env -S uv run python
"""
---
title: Secrets with Devbox and Agent Gateway
slug: secrets-with-devbox
use_case: Use a normal secret for sensitive app data in the devbox and agent gateway for upstream API credentials that should never be exposed to the agent.
workflow:
  - Create a secret for application data that should be available inside the devbox
  - Create a separate secret for an upstream API credential
  - Create an agent gateway config for an upstream API
  - Launch a devbox with one secret injected directly and the credential wired through agent gateway
  - Verify the devbox can read MAGIC_NUMBER while the upstream API credential is replaced with gateway values
  - Shutdown the devbox and delete the gateway config and both secrets
tags:
  - secrets
  - devbox
  - agent-gateway
  - credentials
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
_EXAMPLE_GATEWAY_ENDPOINT = "https://api.example.com"
_UPSTREAM_CREDENTIAL_VALUE = "example-upstream-api-key"
_MAGIC_NUMBER_VALUE = "42"


def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Demonstrate direct secret injection for app data and agent gateway protection for upstream credentials."""
    cleanup = ctx.cleanup

    sdk = RunloopSDK()
    resources_created: list[str] = []
    checks: list[ExampleCheck] = []

    magic_number_name = unique_name("magic-number-secret")
    upstream_credential_name = unique_name("agent-gateway-secret")

    magic_number_secret = sdk.secret.create(name=magic_number_name, value=_MAGIC_NUMBER_VALUE)
    resources_created.append(f"secret:{magic_number_name}")
    cleanup.add(f"secret:{magic_number_name}", magic_number_secret.delete)

    magic_number_info = magic_number_secret.get_info()
    checks.append(
        ExampleCheck(
            name="magic number secret created successfully",
            passed=(magic_number_secret.name == magic_number_name and magic_number_info.id.startswith("sec_")),
            details=f"name={magic_number_secret.name}, id={magic_number_info.id}",
        )
    )

    upstream_credential_secret = sdk.secret.create(
        name=upstream_credential_name,
        value=_UPSTREAM_CREDENTIAL_VALUE,
    )
    resources_created.append(f"secret:{upstream_credential_name}")
    cleanup.add(f"secret:{upstream_credential_name}", upstream_credential_secret.delete)

    upstream_credential_info = upstream_credential_secret.get_info()
    checks.append(
        ExampleCheck(
            name="upstream credential secret created successfully",
            passed=(
                upstream_credential_secret.name == upstream_credential_name
                and upstream_credential_info.id.startswith("sec_")
            ),
            details=(f"name={upstream_credential_secret.name}, id={upstream_credential_info.id}"),
        )
    )

    # Use direct secret injection when code inside the devbox legitimately needs
    # the secret value at runtime. Use agent gateway for upstream credentials
    # that should never be exposed to the agent.
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
        secrets={
            "MAGIC_NUMBER": magic_number_secret.name,
        },
        gateways={
            "MY_API": {
                "gateway": gateway_config.id,
                "secret": upstream_credential_secret.name,
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

    magic_number_result = devbox.cmd.exec("echo $MAGIC_NUMBER")
    magic_number = magic_number_result.stdout().strip()
    checks.append(
        ExampleCheck(
            name="devbox receives plain secret when app needs the value",
            passed=(magic_number_result.exit_code == 0 and magic_number == _MAGIC_NUMBER_VALUE),
            details=(f"exit_code={magic_number_result.exit_code}, MAGIC_NUMBER={magic_number}"),
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
                and gateway_token != _UPSTREAM_CREDENTIAL_VALUE
            ),
            details=(f"exit_code={token_result.exit_code}, token_prefix={gateway_token[:4] or 'missing'}"),
        )
    )

    return RecipeOutput(resources_created=resources_created, checks=checks)


run_secrets_with_devbox_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_secrets_with_devbox_example)
