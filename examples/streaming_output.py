#!/usr/bin/env -S uv run python
"""
Runloop SDK Example - Real-time Command Output Streaming

This example demonstrates streaming command output in real-time:
- Streaming stdout
- Streaming stderr
- Streaming combined output
- Processing output line-by-line
- Async streaming callbacks
"""

import os
import asyncio
from datetime import datetime

from runloop_api_client import RunloopSDK, AsyncRunloopSDK


def demonstrate_basic_streaming(sdk: RunloopSDK):
    """Demonstrate basic stdout streaming."""
    print("=== Basic Stdout Streaming ===")

    with sdk.devbox.create(name="streaming-basic-devbox") as devbox:
        print(f"Created devbox: {devbox.id}\n")

        # Simple callback to print output
        def print_output(line: str):
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {line.rstrip()}")

        # Execute command with streaming
        print("Streaming command output:")
        result = devbox.cmd.exec(
            'for i in 1 2 3 4 5; do echo "Processing item $i"; sleep 0.5; done',
            stdout=print_output,
        )

        print(f"\nCommand completed with exit code: {result.exit_code}")


def demonstrate_stderr_streaming(sdk: RunloopSDK):
    """Demonstrate stderr streaming separately."""
    print("\n=== Separate Stdout and Stderr Streaming ===")

    with sdk.devbox.create(name="streaming-stderr-devbox") as devbox:
        print(f"Created devbox: {devbox.id}\n")

        def handle_stdout(line: str):
            print(f"[STDOUT] {line.rstrip()}")

        def handle_stderr(line: str):
            print(f"[STDERR] {line.rstrip()}")

        # Command that writes to both stdout and stderr
        print("Streaming stdout and stderr separately:")
        result = devbox.cmd.exec(
            """
            echo "This goes to stdout"
            echo "This goes to stderr" >&2
            echo "Back to stdout"
            echo "More stderr" >&2
            """,
            stdout=handle_stdout,
            stderr=handle_stderr,
        )

        print(f"\nCommand completed with exit code: {result.exit_code}")


def demonstrate_combined_streaming(sdk: RunloopSDK):
    """Demonstrate combined output streaming."""
    print("\n=== Combined Output Streaming ===")

    with sdk.devbox.create(name="streaming-combined-devbox") as devbox:
        print(f"Created devbox: {devbox.id}\n")

        # Track all output
        all_output = []

        def capture_all(line: str):
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            all_output.append((timestamp, line.rstrip()))
            print(f"[{timestamp}] {line.rstrip()}")

        # Use the 'output' parameter to capture both stdout and stderr
        print("Streaming combined output:")
        result = devbox.cmd.exec(
            """
            echo "Line 1"
            echo "Error 1" >&2
            echo "Line 2"
            echo "Error 2" >&2
            echo "Line 3"
            """,
            output=capture_all,
        )

        print(f"\nCommand completed with exit code: {result.exit_code}")
        print(f"Captured {len(all_output)} lines of output")


def demonstrate_output_processing(sdk: RunloopSDK):
    """Demonstrate processing streaming output."""
    print("\n=== Processing Streaming Output ===")

    with sdk.devbox.create(name="streaming-processing-devbox") as devbox:
        print(f"Created devbox: {devbox.id}\n")

        # Process and analyze output
        stats = {
            "total_lines": 0,
            "error_lines": 0,
            "warning_lines": 0,
            "info_lines": 0,
        }

        def analyze_output(line: str):
            stats["total_lines"] += 1
            line_lower = line.lower()

            if "error" in line_lower:
                stats["error_lines"] += 1
                print(f"❌ ERROR: {line.rstrip()}")
            elif "warning" in line_lower:
                stats["warning_lines"] += 1
                print(f"⚠️  WARNING: {line.rstrip()}")
            else:
                stats["info_lines"] += 1
                print(f"ℹ️  INFO: {line.rstrip()}")

        # Execute a script that produces different types of output
        print("Analyzing output in real-time:")
        result = devbox.cmd.exec(
            """
            echo "Starting process..."
            echo "Warning: Low memory"
            echo "Processing data..."
            echo "Error: Connection timeout"
            echo "Retrying..."
            echo "Warning: Slow response"
            echo "Success: Operation complete"
            """,
            stdout=analyze_output,
        )

        print(f"\nCommand completed with exit code: {result.exit_code}")
        print(f"\nOutput Statistics:")
        print(f"  Total lines: {stats['total_lines']}")
        print(f"  Errors: {stats['error_lines']}")
        print(f"  Warnings: {stats['warning_lines']}")
        print(f"  Info: {stats['info_lines']}")


def demonstrate_long_running_stream(sdk: RunloopSDK):
    """Demonstrate streaming output from a long-running command."""
    print("\n=== Long-running Command Streaming ===")

    with sdk.devbox.create(name="streaming-longrun-devbox") as devbox:
        print(f"Created devbox: {devbox.id}\n")

        progress_items = []

        def track_progress(line: str):
            line = line.rstrip()
            if "Progress:" in line:
                progress_items.append(line)
                # Extract percentage if present
                print(f"📊 {line}")
            else:
                print(f"   {line}")

        print("Streaming output from long-running task:")
        result = devbox.cmd.exec(
            """
            echo "Starting long-running task..."
            for i in 1 2 3 4 5 6 7 8 9 10; do
                echo "Progress: $((i * 10))% complete"
                sleep 0.3
            done
            echo "Task completed successfully!"
            """,
            stdout=track_progress,
        )

        print(f"\nCommand completed with exit code: {result.exit_code}")
        print(f"Tracked {len(progress_items)} progress updates")


async def demonstrate_async_streaming():
    """Demonstrate async streaming with async callbacks."""
    print("\n=== Async Streaming ===")

    sdk = AsyncRunloopSDK()

    async with sdk.devbox.create(name="async-streaming-devbox") as devbox:
        print(f"Created devbox: {devbox.id}\n")

        # Async callback with async operations
        output_queue = asyncio.Queue()

        async def async_capture(line: str):
            # Simulate async processing (e.g., writing to a database)
            await asyncio.sleep(0.01)
            await output_queue.put(line.rstrip())
            print(f"[ASYNC] {line.rstrip()}")

        # Start processing task
        async def process_queue():
            processed = []
            while True:
                try:
                    line = await asyncio.wait_for(output_queue.get(), timeout=2.0)
                    processed.append(line)
                except asyncio.TimeoutError:
                    break
            return processed

        processor = asyncio.create_task(process_queue())

        # Execute with async streaming
        print("Streaming with async callbacks:")
        await devbox.cmd.exec(
            'for i in 1 2 3 4 5; do echo "Async line $i"; sleep 0.2; done',
            stdout=async_capture,
        )

        # Wait for queue processing
        processed = await processor
        print(f"\nProcessed {len(processed)} lines asynchronously")


def main():
    # Initialize the SDK
    sdk = RunloopSDK()
    print("Initialized Runloop SDK\n")

    # Run synchronous streaming demonstrations
    demonstrate_basic_streaming(sdk)
    demonstrate_stderr_streaming(sdk)
    demonstrate_combined_streaming(sdk)
    demonstrate_output_processing(sdk)
    demonstrate_long_running_stream(sdk)

    print("\nSynchronous streaming examples completed!")


async def async_main():
    """Run async streaming demonstrations."""
    print("\n" + "=" * 60)
    print("Running Async Examples")
    print("=" * 60 + "\n")

    await demonstrate_async_streaming()

    print("\nAsync streaming examples completed!")


if __name__ == "__main__":
    # Ensure API key is set
    if not os.getenv("RUNLOOP_API_KEY"):
        print("Error: RUNLOOP_API_KEY environment variable is not set")
        print("Please set it to your Runloop API key:")
        print("  export RUNLOOP_API_KEY=your-api-key")
        exit(1)

    try:
        # Run synchronous examples
        main()

        # Run async examples
        asyncio.run(async_main())

        print("\n" + "=" * 60)
        print("All streaming examples completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\nError: {e}")
        raise
