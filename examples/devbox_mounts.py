#!/usr/bin/env -S uv run python
"""
---
title: Devbox Mounts (Agent, Code, Object)
slug: devbox-mounts
use_case: Launch a devbox that combines an agent mount for Claude Code, a code mount for the Runloop CLI repo, and an object mount for startup files while routing Anthropic credentials through agent gateway.
workflow:
  - Create or reuse a Claude Code agent by name
  - Store ANTHROPIC_API_KEY as a Runloop secret for gateway-backed access
  - Upload a temporary bootstrap directory as a storage object with a TTL
  - Launch a devbox with agent, code, and object mounts together
  - Verify the gateway token and URL are present instead of the raw Anthropic key
  - Run Claude Code through the Anthropic agent gateway
  - Verify the code mount and extracted object mount contents are present
  - Shutdown the devbox and delete the temporary secret and storage object
tags:
  - devbox
  - mounts
  - agent
  - code
  - object
  - claude-code
  - agent-gateway
  - ttl
  - async
prerequisites:
  - RUNLOOP_API_KEY
  - ANTHROPIC_API_KEY
run: ANTHROPIC_API_KEY=sk-ant-xxx uv run python -m examples.devbox_mounts
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

import os
import shlex
import shutil
import asyncio
import tempfile
from pathlib import Path
from datetime import timedelta

from runloop_api_client import AsyncRunloopSDK
from runloop_api_client.sdk.async_devbox import AsyncDevbox
from runloop_api_client.sdk.async_storage_object import AsyncStorageObject
from runloop_api_client.sdk.async_execution_result import AsyncExecutionResult

from ._harness import run_as_cli, unique_name, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

CLAUDE_CODE_AGENT_NAME = "example-claude-code-agent"
CLAUDE_CODE_AGENT_VERSION = "1.0.0"
CLAUDE_CODE_PACKAGE = "@anthropic-ai/claude-code"
CLAUDE_MODEL = "claude-opus-4-5"
GATEWAY_ENV_PREFIX = "ANTHROPIC"
OBJECT_MOUNT_DIR = "/home/user/bootstrap-assets"
COPIED_EXAMPLE_FILE_NAME = "devbox-mounts-source.py"
OBJECT_TTL = timedelta(hours=1)
CLAUDE_PROMPT = "Reply with the exact text mounted-through-agent-gateway and nothing else."


async def ensure_claude_code_agent(sdk: AsyncRunloopSDK) -> tuple[str, bool]:
    """Return a reusable Claude Code agent, creating it if needed."""
    existing_agents = await sdk.agent.list(name=CLAUDE_CODE_AGENT_NAME, limit=20)
    existing_infos = await asyncio.gather(*(agent.get_info() for agent in existing_agents))

    matching_agents = sorted(
        (
            info
            for info in existing_infos
            if info.name == CLAUDE_CODE_AGENT_NAME
            and info.version == CLAUDE_CODE_AGENT_VERSION
            and info.source is not None
            and info.source.type == "npm"
            and info.source.npm is not None
            and info.source.npm.package_name == CLAUDE_CODE_PACKAGE
        ),
        key=lambda info: info.create_time_ms,
        reverse=True,
    )
    if matching_agents:
        return matching_agents[0].id, True

    agent = await sdk.agent.create_from_npm(
        name=CLAUDE_CODE_AGENT_NAME,
        version=CLAUDE_CODE_AGENT_VERSION,
        package_name=CLAUDE_CODE_PACKAGE,
    )
    return agent.id, False


def create_bootstrap_dir() -> Path:
    """Create local files that will be uploaded and extracted via object mount."""
    temp_dir = Path(tempfile.mkdtemp(prefix="runloop-devbox-mounts-"))
    copied_example_path = temp_dir / COPIED_EXAMPLE_FILE_NAME
    copied_example_path.write_text(Path(__file__).read_text())
    (temp_dir / "README.txt").write_text(
        "This directory was uploaded with upload_from_dir(), stored as a tgz object, "
        "and extracted onto the devbox via an object mount.\n"
    )
    return temp_dir


async def discover_code_mount_path(devbox: AsyncDevbox) -> str:
    """Find the repository path created by the code mount."""
    result: AsyncExecutionResult = await devbox.cmd.exec(
        "if [ -d /home/user/rl-cli ]; then printf /home/user/rl-cli; "
        "elif [ -d /home/user/rl-clis ]; then printf /home/user/rl-clis; "
        "else exit 1; fi"
    )
    return (await result.stdout()).strip() if result.exit_code == 0 else ""


def build_claude_gateway_command() -> str:
    """Build a shell-safe Claude invocation that uses gateway-provided credentials."""
    return (
        f'ANTHROPIC_BASE_URL="${GATEWAY_ENV_PREFIX}_URL" '
        f'ANTHROPIC_API_KEY="${GATEWAY_ENV_PREFIX}" '
        f"claude --model {shlex.quote(CLAUDE_MODEL)} "
        f"-p {shlex.quote(CLAUDE_PROMPT)} "
        "--dangerously-skip-permissions"
    )


async def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a devbox with agent, code, and object mounts plus agent gateway."""
    cleanup = ctx.cleanup
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise RuntimeError("Set ANTHROPIC_API_KEY to run the Claude Code mount example.")

    sdk = AsyncRunloopSDK()
    resources_created: list[str] = []

    agent_id, reused_agent = await ensure_claude_code_agent(sdk)
    resources_created.append(f"agent:{agent_id}:reused" if reused_agent else f"agent:{agent_id}")

    secret = await sdk.secret.create(
        name=unique_name("example-anthropic-gateway").upper().replace("-", "_"),
        value=anthropic_api_key,
    )
    resources_created.append(f"secret:{secret.name}")
    cleanup.add(f"secret:{secret.name}", secret.delete)

    bootstrap_dir = create_bootstrap_dir()
    cleanup.add(f"temp_dir:{bootstrap_dir}", lambda: shutil.rmtree(bootstrap_dir, ignore_errors=True))

    archive: AsyncStorageObject = await sdk.storage_object.upload_from_dir(
        bootstrap_dir,
        name=unique_name("example-devbox-mounts"),
        ttl=OBJECT_TTL,
        metadata={"example": "devbox-mounts"},
    )
    resources_created.append(f"storage_object:{archive.id}")
    cleanup.add(f"storage_object:{archive.id}", archive.delete)

    devbox = await sdk.devbox.create(
        name=unique_name("devbox-mounts-example"),
        launch_parameters={
            "resource_size_request": "SMALL",
            "keep_alive_time_seconds": 60 * 5,
        },
        mounts=[
            {
                "type": "agent_mount",
                "agent_id": None,
                "agent_name": CLAUDE_CODE_AGENT_NAME,
            },
            {
                "type": "code_mount",
                "repo_owner": "runloopai",
                "repo_name": "rl-cli",
            },
            {
                "type": "object_mount",
                "object_id": archive.id,
                "object_path": OBJECT_MOUNT_DIR,
            },
        ],
        gateways={
            GATEWAY_ENV_PREFIX: {
                "gateway": "anthropic",
                "secret": secret.name,
            }
        },
    )
    resources_created.append(f"devbox:{devbox.id}")
    cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

    devbox_info = await devbox.get_info()
    archive_info = await archive.refresh()

    gateway_url_result = await devbox.cmd.exec(f"echo ${GATEWAY_ENV_PREFIX}_URL")
    gateway_url = (await gateway_url_result.stdout()).strip()

    gateway_token_result = await devbox.cmd.exec(f"echo ${GATEWAY_ENV_PREFIX}")
    gateway_token = (await gateway_token_result.stdout()).strip()

    claude_version_result = await devbox.cmd.exec("claude --version")
    claude_version = (await claude_version_result.stdout()).strip()

    claude_gateway_command = build_claude_gateway_command()
    # This is the command you would run to send Claude traffic through the agent gateway.
    # We intentionally do not execute it here so repeated example test runs do not incur model costs.
    # claude_prompt_result = await devbox.cmd.exec(claude_gateway_command)

    repo_mount_path = await discover_code_mount_path(devbox)
    repo_package_json = await devbox.file.read(file_path=f"{repo_mount_path}/package.json") if repo_mount_path else ""

    mounted_example_path = f"{OBJECT_MOUNT_DIR}/{COPIED_EXAMPLE_FILE_NAME}"
    mounted_example_contents = await devbox.file.read(file_path=mounted_example_path)
    mounted_readme_path = f"{OBJECT_MOUNT_DIR}/README.txt"
    mounted_readme_contents = await devbox.file.read(file_path=mounted_readme_path)

    return RecipeOutput(
        resources_created=resources_created,
        checks=[
            ExampleCheck(
                name="Claude Code agent exists and is callable on the devbox",
                passed=claude_version_result.exit_code == 0 and bool(claude_version),
                details=claude_version or f"exit_code={claude_version_result.exit_code}",
            ),
            ExampleCheck(
                name="Anthropic access is routed through agent gateway",
                passed=(
                    devbox_info.gateway_specs is not None
                    and devbox_info.gateway_specs.get(GATEWAY_ENV_PREFIX) is not None
                    and gateway_url_result.exit_code == 0
                    and gateway_url.startswith("http")
                    and gateway_token_result.exit_code == 0
                    and gateway_token.startswith("gws_")
                    and gateway_token != anthropic_api_key
                ),
                details=f"gateway_url={gateway_url}, token_prefix={gateway_token[:4] or 'missing'}",
            ),
            ExampleCheck(
                name="Claude Code gateway invocation is documented without executing it",
                passed=(
                    "ANTHROPIC_BASE_URL" in claude_gateway_command
                    and "ANTHROPIC_API_KEY" in claude_gateway_command
                    and "claude --model" in claude_gateway_command
                ),
                details=claude_gateway_command,
            ),
            ExampleCheck(
                name="rl-cli repository is available through the code mount",
                passed=bool(repo_mount_path) and '"name": "@runloop/rl-cli"' in repo_package_json,
                details=repo_mount_path or "repo mount not found",
            ),
            ExampleCheck(
                name="object mount extracted the uploaded example file onto the devbox",
                passed=(
                    "title: Devbox Mounts (Agent, Code, Object)" in mounted_example_contents
                    and mounted_example_contents.startswith("#!/usr/bin/env -S uv run python")
                ),
                details=mounted_example_path,
            ),
            ExampleCheck(
                name="uploaded object shows TTL and compression details",
                passed=(
                    archive_info.content_type == "tgz"
                    and archive_info.delete_after_time_ms is not None
                    and archive_info.delete_after_time_ms > archive_info.create_time_ms
                ),
                details=(
                    f"content_type={archive_info.content_type}, "
                    f"delete_after_time_ms={archive_info.delete_after_time_ms}"
                ),
            ),
            ExampleCheck(
                name="object mount preserved the bootstrap README content",
                passed="uploaded with upload_from_dir()" in mounted_readme_contents,
                details=mounted_readme_path,
            ),
        ],
    )


run_devbox_mounts_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_mounts_example)
