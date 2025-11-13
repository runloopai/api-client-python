#!/usr/bin/env -S uv run python
"""
Async Runloop SDK Example - Concurrent Devbox Operations

This example demonstrates the asynchronous capabilities of the Runloop SDK:
- Creating and managing devboxes asynchronously
- Concurrent command execution across multiple devboxes
- Async file operations
- Async command streaming
"""

import os
import asyncio

from runloop_api_client import AsyncRunloopSDK


async def demonstrate_basic_async():
    """Demonstrate basic async devbox operations."""
    print("=== Basic Async Operations ===")

    sdk = AsyncRunloopSDK()

    # Create a devbox with async context manager
    async with sdk.devbox.create(name="async-example-devbox") as devbox:
        print(f"Created devbox: {devbox.id}")

        # Execute command asynchronously
        result = await devbox.cmd.exec("echo 'Hello from async devbox!'")
        output = await result.stdout()
        print(f"Command output: {output.strip()}")

        # File operations
        await devbox.file.write(
            path="/home/user/async_test.txt",
            contents="Hello from async operations!\n",
        )
        content = await devbox.file.read(path="/home/user/async_test.txt")
        print(f"File content: {content.strip()}")

    print("Devbox automatically shutdown\n")


async def demonstrate_concurrent_commands():
    """Execute multiple commands concurrently on the same devbox."""
    print("=== Concurrent Command Execution ===")

    sdk = AsyncRunloopSDK()

    async with sdk.devbox.create(name="concurrent-commands-devbox") as devbox:
        print(f"Created devbox: {devbox.id}")

        # Execute multiple commands concurrently
        async def run_command(cmd: str, label: str):
            print(f"Starting: {label}")
            result = await devbox.cmd.exec(cmd)
            output = await result.stdout()
            print(f"{label} completed: {output.strip()}")
            return output

        # Run multiple commands in parallel
        results = await asyncio.gather(
            run_command("echo 'Task 1' && sleep 1", "Task 1"),
            run_command("echo 'Task 2' && sleep 1", "Task 2"),
            run_command("echo 'Task 3' && sleep 1", "Task 3"),
        )

        print(f"All {len(results)} tasks completed\n")


async def demonstrate_multiple_devboxes():
    """Create and manage multiple devboxes concurrently."""
    print("=== Managing Multiple Devboxes ===")

    sdk = AsyncRunloopSDK()

    async def create_and_use_devbox(name: str, number: int):
        """Create a devbox, run a command, and return the result."""
        async with sdk.devbox.create(name=name) as devbox:
            print(f"Devbox {number} ({devbox.id}): Created")

            # Run a command
            result = await devbox.cmd.exec(f"echo 'Hello from devbox {number}'")
            output = await result.stdout()
            print(f"Devbox {number}: {output.strip()}")

            return output

    # Create and use multiple devboxes concurrently
    results = await asyncio.gather(
        create_and_use_devbox("multi-devbox-1", 1),
        create_and_use_devbox("multi-devbox-2", 2),
        create_and_use_devbox("multi-devbox-3", 3),
    )

    print(f"All {len(results)} devboxes completed and shutdown\n")


async def demonstrate_async_streaming():
    """Demonstrate real-time command output streaming with async callbacks."""
    print("=== Async Command Streaming ===")

    sdk = AsyncRunloopSDK()

    async with sdk.devbox.create(name="streaming-devbox") as devbox:
        print(f"Created devbox: {devbox.id}")

        # Async callback to capture output
        output_lines = []

        async def capture_output(line: str):
            print(f"[STREAM] {line.strip()}")
            output_lines.append(line)

        # Execute command with streaming output
        print("\nStreaming command output:")
        await devbox.cmd.exec(
            'for i in 1 2 3 4 5; do echo "Line $i"; sleep 0.2; done',
            stdout=capture_output,
        )

        print(f"\nCaptured {len(output_lines)} lines of output\n")


async def demonstrate_async_execution():
    """Demonstrate async execution management."""
    print("=== Async Execution Management ===")

    sdk = AsyncRunloopSDK()

    async with sdk.devbox.create(name="async-exec-devbox") as devbox:
        print(f"Created devbox: {devbox.id}")

        # Start an async execution
        execution = await devbox.cmd.exec_async("echo 'Starting...'; sleep 2; echo 'Finished!'")
        print(f"Started execution: {execution.execution_id}")

        # Poll execution state
        state = await execution.get_state()
        print(f"Initial status: {state.status}")

        # Wait for completion
        print("Waiting for completion...")
        result = await execution.result()
        print(f"Exit code: {result.exit_code}")
        output = await result.stdout()
        print(f"Output:\n{output}")

        # Start another execution and kill it
        print("\nStarting long-running process...")
        long_execution = await devbox.cmd.exec_async("sleep 30")
        print(f"Execution ID: {long_execution.execution_id}")

        # Wait a bit then kill it
        await asyncio.sleep(1)
        print("Killing execution...")
        await long_execution.kill()
        print("Execution killed\n")


async def main():
    """Run all async demonstrations."""
    print("Initialized Async Runloop SDK\n")

    # Run demonstrations
    await demonstrate_basic_async()
    await demonstrate_concurrent_commands()
    await demonstrate_multiple_devboxes()
    await demonstrate_async_streaming()
    await demonstrate_async_execution()

    print("All async demonstrations completed!")


if __name__ == "__main__":
    # Ensure API key is set
    if not os.getenv("RUNLOOP_API_KEY"):
        print("Error: RUNLOOP_API_KEY environment variable is not set")
        print("Please set it to your Runloop API key:")
        print("  export RUNLOOP_API_KEY=your-api-key")
        exit(1)

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nError: {e}")
        raise
