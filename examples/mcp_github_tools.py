#!/usr/bin/env -S uv run python
"""
---
title: MCP Hub + Claude Code + GitHub
slug: mcp-github-tools
use_case: Connect Claude Code running in a devbox to GitHub tools through MCP Hub without exposing raw GitHub credentials to the devbox.
workflow:
  - Create an MCP config for GitHub
  - Store GitHub token as a Runloop secret
  - Launch a devbox with MCP Hub wiring
  - Install Claude Code and register MCP endpoint
  - Run a Claude prompt through MCP tools
  - Shutdown devbox and clean up cloud resources
tags:
  - mcp
  - devbox
  - github
  - commands
  - cleanup
prerequisites:
  - RUNLOOP_API_KEY
  - GITHUB_TOKEN (GitHub PAT with repo scope)
  - ANTHROPIC_API_KEY
run: GITHUB_TOKEN=ghp_xxx ANTHROPIC_API_KEY=sk-ant-xxx uv run python -m examples.mcp_github_tools
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from runloop_api_client import RunloopSDK

from ._harness import run_as_cli, unique_name, wrap_recipe_with_options
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

GITHUB_MCP_ENDPOINT = "https://api.githubcopilot.com/mcp/"


@dataclass
class McpExampleOptions:
    """Options for the MCP GitHub tools example."""

    skip_if_missing_credentials: bool = False


def recipe(ctx: RecipeContext, options: McpExampleOptions) -> RecipeOutput:  # noqa: ARG001
    """Connect Claude Code to GitHub tools via MCP Hub."""
    cleanup = ctx.cleanup

    sdk = RunloopSDK()
    resources_created: list[str] = []
    checks: list[ExampleCheck] = []

    github_token = os.environ.get("GITHUB_TOKEN")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if not github_token:
        raise RuntimeError("Set GITHUB_TOKEN to a GitHub PAT with repo scope.")
    if not anthropic_key:
        raise RuntimeError("Set ANTHROPIC_API_KEY for Claude Code.")

    # Register GitHub's MCP server with Runloop
    mcp_config = sdk.api.mcp_configs.create(
        name=unique_name("github-example"),
        endpoint=GITHUB_MCP_ENDPOINT,
        allowed_tools=[
            "get_me",
            "search_pull_requests",
            "get_pull_request",
            "get_repository",
            "get_file_contents",
        ],
        description="GitHub MCP server - example",
    )
    resources_created.append(f"mcp_config:{mcp_config.id}")
    cleanup.add(f"mcp_config:{mcp_config.id}", lambda: sdk.api.mcp_configs.delete(mcp_config.id))

    # Store the GitHub PAT as a Runloop secret
    secret_name = unique_name("example-github-mcp")
    secret = sdk.secret.create(name=secret_name, value=github_token)
    resources_created.append(f"secret:{secret_name}")
    cleanup.add(f"secret:{secret_name}", secret.delete)

    # Launch a devbox with MCP Hub wiring
    devbox = sdk.devbox.create(
        name=unique_name("mcp-claude-code"),
        launch_parameters={
            "resource_size_request": "SMALL",
            "keep_alive_time_seconds": 300,
        },
        mcp={
            "MCP_SECRET": {
                "mcp_config": mcp_config.id,
                "secret": secret_name,
            },
        },
    )
    resources_created.append(f"devbox:{devbox.id}")
    cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

    # Install Claude Code
    install_result = devbox.cmd.exec("npm install -g @anthropic-ai/claude-code")
    checks.append(
        ExampleCheck(
            name="install Claude Code",
            passed=install_result.exit_code == 0,
            details="installed" if install_result.exit_code == 0 else install_result.stderr(),
        )
    )
    if install_result.exit_code != 0:
        return RecipeOutput(resources_created=resources_created, checks=checks)

    # Register MCP Hub endpoint with Claude Code
    add_mcp_result = devbox.cmd.exec(
        'claude mcp add runloop-mcp --transport http "$RL_MCP_URL" --header "Authorization: Bearer $RL_MCP_TOKEN"',
    )
    checks.append(
        ExampleCheck(
            name="register MCP Hub in Claude",
            passed=add_mcp_result.exit_code == 0,
            details="registered" if add_mcp_result.exit_code == 0 else add_mcp_result.stderr(),
        )
    )
    if add_mcp_result.exit_code != 0:
        return RecipeOutput(resources_created=resources_created, checks=checks)

    # Ask Claude to summarize latest PR via MCP tools
    prompt = (
        "Use the MCP tools to get my last pr and describe what it does in 2-3 sentences. "
        "Also detail how you collected this information"
    )
    claude_result = devbox.cmd.exec(
        f'ANTHROPIC_API_KEY={anthropic_key} claude -p "{prompt}" --dangerously-skip-permissions',
    )
    claude_stdout = claude_result.stdout().strip()
    checks.append(
        ExampleCheck(
            name="Claude prompt through MCP succeeds",
            passed=claude_result.exit_code == 0 and len(claude_stdout) > 0,
            details="non-empty response received" if claude_result.exit_code == 0 else claude_result.stderr(),
        )
    )

    return RecipeOutput(resources_created=resources_created, checks=checks)


def validate_env(options: McpExampleOptions) -> tuple[bool, list[ExampleCheck]]:
    """Validate required environment variables."""
    checks: list[ExampleCheck] = []
    skip_if_missing = options.skip_if_missing_credentials

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token and skip_if_missing:
        checks.append(
            ExampleCheck(
                name="GITHUB_TOKEN provided",
                passed=False,
                details="Skipped: missing GITHUB_TOKEN",
            )
        )
        return True, checks

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key and skip_if_missing:
        checks.append(
            ExampleCheck(
                name="ANTHROPIC_API_KEY provided",
                passed=False,
                details="Skipped: missing ANTHROPIC_API_KEY",
            )
        )
        return True, checks

    return False, checks


run_mcp_github_tools_example = wrap_recipe_with_options(recipe, validate_env)


if __name__ == "__main__":
    run_as_cli(lambda: run_mcp_github_tools_example(McpExampleOptions()))
