#!/usr/bin/env python3
"""MCP Hub + Claude Code + GitHub

Launches a devbox with GitHub's MCP server attached via MCP Hub,
installs Claude Code, registers the MCP endpoint, and asks Claude
to list repositories — all without the devbox seeing your real
GitHub credentials.

Prerequisites:
    RUNLOOP_API_KEY   — your Runloop API key
    GITHUB_TOKEN      — a GitHub PAT with repo scope
    ANTHROPIC_API_KEY — your Anthropic API key (for Claude Code)

Usage:
    GITHUB_TOKEN=ghp_xxx ANTHROPIC_API_KEY=sk-ant-xxx python examples/mcp_github_claude_code.py
"""

from __future__ import annotations

import os
import sys
import time

from runloop_api_client import RunloopSDK

GITHUB_MCP_ENDPOINT = "https://api.githubcopilot.com/mcp/"


def main() -> None:
    github_token = os.environ.get("GITHUB_TOKEN")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if not github_token:
        print("Set GITHUB_TOKEN to a GitHub PAT with repo scope.", file=sys.stderr)
        sys.exit(1)
    if not anthropic_key:
        print("Set ANTHROPIC_API_KEY for Claude Code.", file=sys.stderr)
        sys.exit(1)

    sdk = RunloopSDK()
    secret_name = f"example-github-mcp-{int(time.time())}"

    # 1. Create an MCP config for the GitHub MCP server
    print("Creating MCP config…")
    mcp_config = sdk.mcp_config.create(
        name=f"github-example-{int(time.time())}",
        endpoint=GITHUB_MCP_ENDPOINT,
        allowed_tools=["*"],
        description="GitHub MCP server — example",
    )
    print(f"  MCP config: {mcp_config.id}")

    # 2. Store the GitHub PAT as a Runloop secret
    print("Storing GitHub token as a secret…")
    sdk.api.secrets.create(name=secret_name, value=github_token)

    devbox = None
    try:
        # 3. Launch a devbox with MCP Hub enabled
        print("Creating devbox with MCP Hub…")
        devbox = sdk.devbox.create(
            name=f"mcp-claude-code-{int(time.time())}",
            launch_parameters={
                "resource_size_request": "SMALL",
                "keep_alive_time_seconds": 300,
            },
            mcp=[{"mcp_config": mcp_config.id, "secret": secret_name}],
        )
        print(f"  Devbox ready: {devbox.id}")

        # 4. Install Claude Code
        print("\nInstalling Claude Code…")
        install_result = devbox.cmd.exec("npm install -g @anthropic-ai/claude-code")
        if install_result.exit_code != 0:
            print("Failed to install Claude Code:", install_result.stderr(), file=sys.stderr)
            return
        print("  Installed.")

        # 5. Register MCP Hub with Claude Code
        print("Registering MCP Hub endpoint with Claude Code…")
        add_result = devbox.cmd.exec(
            'claude mcp add runloop-mcp --transport http "$RL_MCP_URL" '
            '--header "Authorization: Bearer $RL_MCP_TOKEN"'
        )
        if add_result.exit_code != 0:
            print("Failed to add MCP server:", add_result.stderr(), file=sys.stderr)
            return
        print("  MCP server registered.")

        # 6. Ask Claude Code to list repos
        print("\nAsking Claude Code to list runloopai repos…\n")
        claude_result = devbox.cmd.exec(
            f"ANTHROPIC_API_KEY={anthropic_key} claude -p "
            '"Use the MCP tools to list all repositories in the runloopai GitHub org. '
            'Just output the repo names, one per line." '
            "--dangerously-skip-permissions"
        )

        output = claude_result.stdout().strip()
        print("── Claude Code output ──────────────────────────────")
        print(output)
        print("────────────────────────────────────────────────────")

    finally:
        print("\nCleaning up…")
        if devbox:
            try:
                devbox.shutdown()
            except Exception:
                pass
        try:
            mcp_config.delete()
        except Exception:
            pass
        try:
            sdk.api.secrets.delete(secret_name)
        except Exception:
            pass
        print("Done.")


if __name__ == "__main__":
    main()
