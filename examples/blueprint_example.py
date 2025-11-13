#!/usr/bin/env -S uv run python
"""
Runloop SDK Example - Blueprint Workflows

This example demonstrates blueprint creation and management:
- Creating blueprints with Dockerfiles
- Creating blueprints with system setup commands
- Using blueprints to create devboxes
- Viewing blueprint build logs
- Blueprint lifecycle management
"""

import os

from runloop_api_client import RunloopSDK
from runloop_api_client.sdk import Blueprint


def create_simple_blueprint(sdk: RunloopSDK):
    """Create a simple blueprint with a Dockerfile."""
    print("=== Creating Simple Blueprint ===")

    dockerfile = """FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    curl \\
    git

WORKDIR /home/user
"""

    blueprint = sdk.blueprint.create(
        name="simple-python-blueprint",
        dockerfile=dockerfile,
    )

    print(f"Created blueprint: {blueprint.id}")

    # Get blueprint info
    info = blueprint.get_info()
    print(f"Blueprint name: {info.name}")
    print(f"Blueprint status: {info.status}")

    return blueprint


def create_blueprint_with_setup(sdk: RunloopSDK):
    """Create a blueprint with system setup commands."""
    print("\n=== Creating Blueprint with System Setup ===")

    dockerfile = """FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip

WORKDIR /home/user
"""

    blueprint = sdk.blueprint.create(
        name="ml-environment-blueprint",
        dockerfile=dockerfile,
        system_setup_commands=[
            "pip3 install numpy pandas scikit-learn",
            "pip3 install matplotlib seaborn",
            "echo 'ML environment ready!'",
        ],
    )

    print(f"Created blueprint: {blueprint.id}")

    # View build logs
    print("\nRetrieving build logs...")
    logs = blueprint.logs()
    if logs.logs:
        print("Build log entries:")
        for i, log_entry in enumerate(logs.logs[:5], 1):
            print(f"  {i}. {log_entry.message[:80]}...")
        if len(logs.logs) > 5:
            print(f"  ... and {len(logs.logs) - 5} more log entries")

    return blueprint


def create_blueprint_from_base(sdk: RunloopSDK):
    """Create a blueprint based on an existing blueprint."""
    print("\n=== Creating Blueprint from Base ===")

    # First create a base blueprint
    base_blueprint = sdk.blueprint.create(
        name="base-nodejs-blueprint",
        dockerfile="""FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \\
    curl \\
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \\
    && apt-get install -y nodejs

WORKDIR /home/user
""",
    )

    print(f"Created base blueprint: {base_blueprint.id}")

    # Create a derived blueprint
    derived_blueprint = sdk.blueprint.create(
        name="nodejs-with-tools-blueprint",
        base_blueprint_id=base_blueprint.id,
        system_setup_commands=[
            "npm install -g typescript ts-node",
            "npm install -g eslint prettier",
            "echo 'Node.js with tools ready!'",
        ],
    )

    print(f"Created derived blueprint: {derived_blueprint.id}")

    return base_blueprint, derived_blueprint


def use_blueprint_to_create_devbox(blueprint: Blueprint):
    """Create and use a devbox from a blueprint."""
    print("\n=== Creating Devbox from Blueprint ===")

    # Create devbox from blueprint
    devbox = blueprint.create_devbox(name="devbox-from-blueprint")

    print(f"Created devbox: {devbox.id}")

    try:
        # Verify the devbox has the expected environment
        result = devbox.cmd.exec("python3 --version")
        print(f"Python version: {result.stdout().strip()}")

        result = devbox.cmd.exec("which pip3")
        print(f"pip3 location: {result.stdout().strip()}")

        # Run a simple Python command
        result = devbox.cmd.exec("python3 -c 'import sys; print(sys.version)'")
        print(f"Python sys.version: {result.stdout().strip()}")
    finally:
        # Cleanup
        devbox.shutdown()
        print("Devbox shutdown")


def list_blueprints(sdk: RunloopSDK):
    """List all available blueprints."""
    print("\n=== Listing Blueprints ===")

    blueprints = sdk.blueprint.list(limit=5)

    print(f"Found {len(blueprints)} blueprints:")
    for bp in blueprints:
        info = bp.get_info()
        print(f"  - {info.name} ({bp.id}): {info.status}")


def cleanup_blueprints(blueprints: list[Blueprint]):
    """Delete blueprints to clean up."""
    print("\n=== Cleaning Up Blueprints ===")

    for blueprint in blueprints:
        try:
            info = blueprint.get_info()
            print(f"Deleting blueprint: {info.name} ({blueprint.id})")
            blueprint.delete()
            print(f"  Deleted: {blueprint.id}")
        except Exception as e:
            print(f"  Error deleting {blueprint.id}: {e}")


def main():
    # Initialize the SDK
    sdk = RunloopSDK()
    print("Initialized Runloop SDK\n")

    created_blueprints: list[Blueprint] = []

    try:
        # Create simple blueprint
        simple_bp = create_simple_blueprint(sdk)
        created_blueprints.append(simple_bp)

        # Create blueprint with setup commands
        ml_bp = create_blueprint_with_setup(sdk)
        created_blueprints.append(ml_bp)

        # Create blueprint from base
        base_bp, derived_bp = create_blueprint_from_base(sdk)
        created_blueprints.extend([base_bp, derived_bp])

        # Use a blueprint to create a devbox
        use_blueprint_to_create_devbox(simple_bp)

        # List all blueprints
        list_blueprints(sdk)

    finally:
        # Cleanup all created blueprints
        if created_blueprints:
            cleanup_blueprints(created_blueprints)

    print("\nBlueprint example completed!")


if __name__ == "__main__":
    # Ensure API key is set
    if not os.getenv("RUNLOOP_API_KEY"):
        print("Error: RUNLOOP_API_KEY environment variable is not set")
        print("Please set it to your Runloop API key:")
        print("  export RUNLOOP_API_KEY=your-api-key")
        exit(1)

    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        raise
