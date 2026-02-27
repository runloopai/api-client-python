#!/usr/bin/env python3
"""MCP Hub + Claude Code + GitHub

Launches a devbox with GitHub's MCP server attached via MCP Hub,
installs Claude Code, registers the MCP endpoint, and asks Claude
to list repositories in a GitHub org — all without the devbox ever
seeing your real GitHub credentials.

Prerequisites:
    RUNLOOP_API_KEY   — your Runloop API key
    GITHUB_TOKEN      — a GitHub PAT with repo scope
    ANTHROPIC_API_KEY — your Anthropic API key (for Claude Code)

Usage:
    GITHUB_TOKEN=ghp_xxx ANTHROPIC_API_KEY=sk-ant-xxx \
        python examples/mcp_github_claude_code.py
"""

from __future__ import annotations

import os
import sys
import time

from runloop_api_client import RunloopSDK

GITHUB_MCP_ENDPOINT = "https://api.githubcopilot.com/mcp/"
SECRET_NAME = f"example-github-mcp-{int(time.time())}"


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

    # ── 1. Register GitHub's MCP server with Runloop ───────────────────
    print("[1/6] Creating MCP config…")
    mcp_config = sdk.mcp_config.create(
        name=f"github-example-{int(time.time())}",
        endpoint=GITHUB_MCP_ENDPOINT,
        allowed_tools=[
            "get_me",
            "search_pull_requests",
            "get_pull_request",
            "get_repository",
            "get_file_contents",
        ],
        description="GitHub MCP server — example",
    )
    print(f"      Config: {mcp_config.id}")

    # ── 2. Store the GitHub PAT as a Runloop secret ────────────────────
    #    Runloop holds the token server-side; the devbox never sees it.
    print("[2/6] Storing GitHub token as secret…")
    sdk.api.secrets.create(name=SECRET_NAME, value=github_token)
    print(f"      Secret: {SECRET_NAME}")

    devbox = None
    try:
        # ── 3. Launch a devbox with MCP Hub ──────────────────────────────
        #    The devbox gets $RL_MCP_URL and $RL_MCP_TOKEN — a proxy
        #    endpoint, not the raw GitHub token.
        print("[3/6] Creating devbox…")
        devbox = sdk.devbox.create(
            name=f"mcp-claude-code-{int(time.time())}",
            launch_parameters={
                "resource_size_request": "SMALL",
                "keep_alive_time_seconds": 300,
            },
            mcp=[{"mcp_config": mcp_config.id, "secret": SECRET_NAME}],
        )
        print(f"      Devbox: {devbox.id}")

        # ── 4. Install Claude Code ───────────────────────────────────────
        print("[4/6] Installing Claude Code…")
        install_result = devbox.cmd.exec("npm install -g @anthropic-ai/claude-code")
        if install_result.exit_code != 0:
            print("Failed to install Claude Code:", install_result.stderr(), file=sys.stderr)
            return
        print("      Installed.")

        # ── 5. Point Claude Code at MCP Hub ──────────────────────────────
        #    Claude Code  ──>  MCP Hub (Runloop)  ──>  GitHub MCP Server
        #                      injects secret
        print("[5/6] Registering MCP Hub with Claude Code…")
        add_result = devbox.cmd.exec(
            'claude mcp add runloop-mcp --transport http "$RL_MCP_URL" '
            '--header "Authorization: Bearer $RL_MCP_TOKEN"'
        )
        if add_result.exit_code != 0:
            print("Failed to add MCP server:", add_result.stderr(), file=sys.stderr)
            return
        print("      Registered.")

        prompt = (
            "Use the MCP tools to get my last pr and describe what it does "
            "in 2-3 sentences. Also detail how you collected this information"
        )
        # ── 6. Ask Claude Code to list repos via MCP ─────────────────────
        print(f"[6/6] Asking Claude Code to: \n{prompt}\n")
        claude_result = devbox.cmd.exec(
            f'ANTHROPIC_API_KEY={anthropic_key} claude -p "{prompt}" '
            "--dangerously-skip-permissions"
        )
        print(claude_result.stdout().strip())

    finally:
        if devbox:
            devbox.shutdown()
        mcp_config.delete()
        sdk.api.secrets.delete(SECRET_NAME)
        print("Done.")


if __name__ == "__main__":
    main()
