#!/usr/bin/env -S uv run python
"""
Basic Runloop SDK Example - Devbox Operations

This example demonstrates the core functionality of the Runloop SDK:
- Creating and managing devboxes
- Executing commands synchronously and asynchronously
- File operations (read, write, upload, download)
- Devbox lifecycle management
"""

import os
from pathlib import Path

from runloop_api_client import RunloopSDK


def main():
    # Initialize the SDK (uses RUNLOOP_API_KEY environment variable by default)
    sdk = RunloopSDK()
    print("Initialized Runloop SDK")

    # Create a devbox with automatic cleanup using context manager
    print("\n=== Creating Devbox ===")
    with sdk.devbox.create(name="basic-example-devbox") as devbox:
        print(f"Created devbox: {devbox.id}")

        # Get devbox information
        info = devbox.get_info()
        print(f"Devbox status: {info.status}")
        print(f"Devbox name: {info.name}")

        # Execute a simple command
        print("\n=== Executing Commands ===")
        result = devbox.cmd.exec("echo 'Hello from Runloop!'")
        print(f"Command output: {result.stdout().strip()}")
        print(f"Exit code: {result.exit_code}")
        print(f"Success: {result.success}")

        # Execute a command that generates output
        result = devbox.cmd.exec("ls -la /home/user")
        print(f"\nDirectory listing:\n{result.stdout()}")

        # Execute a command with error
        result = devbox.cmd.exec("ls /nonexistent")
        if result.failed:
            print(f"\nCommand failed with exit code {result.exit_code}")
            print(f"Error output: {result.stderr()}")

        # File operations
        print("\n=== File Operations ===")

        # Write a file
        file_path = "/home/user/test.txt"
        content = "Hello, Runloop!\nThis is a test file.\n"
        devbox.file.write(path=file_path, contents=content)
        print(f"Wrote file: {file_path}")

        # Read the file back
        read_content = devbox.file.read(path=file_path)
        print(f"Read file content:\n{read_content}")

        # Create a local file to upload
        local_file = Path("temp_upload.txt")
        local_file.write_text("This file will be uploaded to the devbox.\n")

        try:
            # Upload a file
            upload_path = "/home/user/uploaded.txt"
            devbox.file.upload(path=upload_path, file=local_file)
            print(f"\nUploaded file to: {upload_path}")

            # Verify the upload by reading the file
            uploaded_content = devbox.file.read(path=upload_path)
            print(f"Uploaded file content: {uploaded_content.strip()}")

            # Download a file
            download_data = devbox.file.download(path=upload_path)
            local_download = Path("temp_download.txt")
            local_download.write_bytes(download_data)
            print(f"Downloaded file to: {local_download}")
            print(f"Downloaded content: {local_download.read_text().strip()}")
        finally:
            # Cleanup local files
            local_file.unlink(missing_ok=True)
            if Path("temp_download.txt").exists():
                Path("temp_download.txt").unlink()

        # Asynchronous command execution
        print("\n=== Asynchronous Command Execution ===")

        # Start a long-running command asynchronously
        execution = devbox.cmd.exec_async("sleep 3 && echo 'Done sleeping!'")
        print(f"Started async execution: {execution.execution_id}")

        # Check the execution state
        state = execution.get_state()
        print(f"Execution status: {state.status}")

        # Wait for completion and get the result
        print("Waiting for execution to complete...")
        result = execution.result()
        print(f"Execution completed with exit code: {result.exit_code}")
        print(f"Output: {result.stdout().strip()}")

        # Keep devbox alive (extends timeout)
        print("\n=== Devbox Lifecycle ===")
        devbox.keep_alive()
        print("Extended devbox timeout")

    print("\n=== Devbox Cleanup ===")
    print("Devbox automatically shutdown when exiting context manager")


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
