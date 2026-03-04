#!/usr/bin/env -S uv run python
"""
---
title: Devbox Tunnel (HTTP Server Access)
slug: devbox-tunnel
use_case: Create a devbox, start an HTTP server, enable a tunnel, and access the server from the local machine through the tunnel. Uses the async SDK.
workflow:
  - Create a devbox
  - Start an HTTP server inside the devbox
  - Enable a tunnel for external access
  - Make an HTTP request from the local machine through the tunnel
  - Validate the response
  - Shutdown the devbox
tags:
  - devbox
  - tunnel
  - networking
  - http
  - async
prerequisites:
  - RUNLOOP_API_KEY
run: uv run python -m examples.devbox_tunnel
test: uv run pytest -m smoketest tests/smoketests/examples/
---
"""

from __future__ import annotations

import asyncio

import httpx

from runloop_api_client import AsyncRunloopSDK

from ._harness import run_as_cli, wrap_recipe
from .example_types import ExampleCheck, RecipeOutput, RecipeContext

HTTP_SERVER_PORT = 8080
SERVER_STARTUP_DELAY_S = 2


async def recipe(ctx: RecipeContext) -> RecipeOutput:
    """Create a devbox, start an HTTP server, enable a tunnel, and access it from the local machine."""
    cleanup = ctx.cleanup

    sdk = AsyncRunloopSDK()

    devbox = await sdk.devbox.create(
        name="devbox-tunnel-example",
        launch_parameters={
            "resource_size_request": "X_SMALL",
            "keep_alive_time_seconds": 60 * 10,
        },
    )
    cleanup.add(f"devbox:{devbox.id}", devbox.shutdown)

    # Start a simple HTTP server inside the devbox using Python's built-in http.server
    # We use exec_async because the server runs indefinitely until stopped
    server_execution = await devbox.cmd.exec_async(f"python3 -m http.server {HTTP_SERVER_PORT} --directory /tmp")

    # Give the server a moment to start
    await asyncio.sleep(SERVER_STARTUP_DELAY_S)

    # Enable a tunnel to expose the HTTP server
    # For authenticated tunnels, use auth_mode="authenticated" and include the auth_token
    # in your requests via the Authorization header: `Authorization: Bearer {tunnel.auth_token}`
    tunnel = await devbox.net.enable_tunnel(auth_mode="open")

    # Get the tunnel URL for the server port
    tunnel_url = await devbox.get_tunnel_url(HTTP_SERVER_PORT)
    if tunnel_url is None:
        raise RuntimeError("Failed to get tunnel URL after enabling tunnel")

    # Make an HTTP request from the LOCAL MACHINE through the tunnel to the devbox
    # This demonstrates that the tunnel allows external access to the devbox service
    async with httpx.AsyncClient() as client:
        response = await client.get(tunnel_url)
        response_text = response.text

    # Stop the HTTP server
    await server_execution.kill()

    return RecipeOutput(
        resources_created=[f"devbox:{devbox.id}"],
        checks=[
            ExampleCheck(
                name="tunnel was created successfully",
                passed=bool(tunnel.tunnel_key),
                details=f"tunnel_key={tunnel.tunnel_key}",
            ),
            ExampleCheck(
                name="tunnel URL was constructed correctly",
                passed=bool(
                    tunnel.tunnel_key and tunnel.tunnel_key in tunnel_url and str(HTTP_SERVER_PORT) in tunnel_url
                ),
                details=tunnel_url,
            ),
            ExampleCheck(
                name="HTTP request through tunnel succeeded",
                passed=response.is_success,
                details=f"status={response.status_code}",
            ),
            ExampleCheck(
                name="response contains directory listing",
                passed="Directory listing" in response_text,
                details=response_text[:200],
            ),
        ],
    )


run_devbox_tunnel_example = wrap_recipe(recipe)


if __name__ == "__main__":
    run_as_cli(run_devbox_tunnel_example)
