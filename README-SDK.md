# Runloop SDK – Python Object-Oriented Client

The `RunloopSDK` builds on top of the underlying REST client and provides a Pythonic, object-oriented API for managing devboxes, blueprints, snapshots, and storage objects. The SDK exposes synchronous and asynchronous variants to match your runtime requirements.

## Table of Contents

- [Installation](#installation)
- [Quickstart (synchronous)](#quickstart-synchronous)
- [Quickstart (asynchronous)](#quickstart-asynchronous)
- [Core Concepts](#core-concepts)
- [Devbox](#devbox)
- [Blueprint](#blueprint)
- [Snapshot](#snapshot)
- [StorageObject](#storageobject)
- [Mounting Storage Objects to Devboxes](#mounting-storage-objects-to-devboxes)
- [Accessing the Underlying REST Client](#accessing-the-underlying-rest-client)
- [Error Handling](#error-handling)
- [Advanced Configuration](#advanced-configuration)
- [Async Usage](#async-usage)
- [Polling Configuration](#polling-configuration)
- [Complete API Reference](#complete-api-reference)
- [Feedback](#feedback)

## Installation

The SDK ships with the `runloop_api_client` package—no extra dependencies are required.

```bash
pip install runloop_api_client
```

## Quickstart (synchronous)

```python
from runloop_api_client import RunloopSDK

runloop = RunloopSDK()

# Create a ready-to-use devbox
with runloop.devbox.create(name="my-devbox") as devbox:
    result = devbox.cmd.exec(command="echo 'Hello from Runloop!'")
    print(result.stdout())

    # Stream stdout in real time
    devbox.cmd.exec(
        command="ls -la",
        stdout=lambda line: print("stdout:", line),
    )

# Blueprints
blueprint = runloop.blueprint.create(
    name="my-blueprint",
    dockerfile="FROM ubuntu:22.04\nRUN echo 'Hello' > /hello.txt\n",
)
devbox = blueprint.create_devbox(name="dev-from-blueprint")

# Storage objects
obj = runloop.storage_object.upload_from_text("Hello world!", name="greeting.txt")
print(obj.download_as_text())
```

## Quickstart (asynchronous)

```python
import asyncio
from runloop_api_client import AsyncRunloopSDK

async def main():
    runloop = AsyncRunloopSDK()
    async with await runloop.devbox.create(name="async-devbox") as devbox:
        result = await devbox.cmd.exec(command="pwd")
        print(await result.stdout())

        def capture(line: str) -> None:
            print(">>", line)

        await devbox.cmd.exec(command="ls", stdout=capture)

asyncio.run(main())
```

## Core Concepts

### RunloopSDK

The main SDK class that provides access to all Runloop functionality:

```python
from runloop_api_client import RunloopSDK

runloop = RunloopSDK(
    bearer_token="your-api-key",  # defaults to RUNLOOP_API_KEY env var
    # ... other options
)
```

### Available Resources

The SDK provides object-oriented interfaces for all major Runloop resources:

- **`runloop.devbox`** - Devbox management (create, list, execute commands, file operations)
- **`runloop.blueprint`** - Blueprint management (create, list, build blueprints)
- **`runloop.snapshot`** - Snapshot management (list disk snapshots)
- **`runloop.storage_object`** - Storage object management (upload, download, list objects)
- **`runloop.api`** - Direct access to the underlying REST API client

### Devbox

Object-oriented interface for working with devboxes. Created via `runloop.devbox.create()`, `runloop.devbox.create_from_blueprint_id()`, `runloop.devbox.create_from_blueprint_name()`, `runloop.devbox.create_from_snapshot()`, or `runloop.devbox.from_id()`:

```python
# Create a new devbox
devbox = runloop.devbox.create(name="my-devbox")

# Create a devbox from a blueprint ID
devbox_from_blueprint = runloop.devbox.create_from_blueprint_id(
    blueprint_id="bpt_123",
    name="my-devbox-from-blueprint",
)

# Create a devbox from a blueprint name
devbox_from_name = runloop.devbox.create_from_blueprint_name(
    blueprint_name="my-blueprint-name",
    name="my-devbox-from-blueprint",
)

# Create a devbox from a snapshot
devbox_from_snapshot = runloop.devbox.create_from_snapshot(
    snapshot_id="snp_123",
    name="my-devbox-from-snapshot",
)

# Or get an existing one (waits for it to be running)
existing_devbox = runloop.devbox.from_id(devbox_id="dbx_123")

# List all devboxes
devboxes = runloop.devbox.list(limit=10)

# Get devbox information
info = devbox.get_info()
print(f"Devbox {info.name} is {info.status}")
```

#### Command Execution

Execute commands synchronously or asynchronously:

```python
# Synchronous command execution (waits for completion)
result = devbox.cmd.exec(command="ls -la")
print("Output:", result.stdout())
print("Exit code:", result.exit_code)
print("Success:", result.success)

# Asynchronous command execution (returns immediately)
execution = devbox.cmd.exec_async(command="npm run dev")

# Check execution status
state = execution.get_state()
print("Status:", state.status)

# Wait for completion and get result
result = execution.result()
print("Final output:", result.stdout())

# Kill the process
execution.kill()
```

#### Execution Management

The `Execution` object provides fine-grained control over asynchronous command execution:

```python
# Start a long-running process
execution = devbox.cmd.exec_async(command="python train_model.py")

# Get the execution ID
print("Execution ID:", execution.execution_id)
print("Devbox ID:", execution.devbox_id)

# Poll for current state
state = execution.get_state()
print("Status:", state.status)  # "running", "completed", etc.
print("Exit code:", state.exit_status) # only set when execution has completed

# Wait for completion and get results
result = execution.result()
print("Exit code:", result.exit_code)
print("Output:", result.stdout())
print("Errors:", result.stderr())

# Or kill the process early
execution.kill()
```

**Key methods:**

- `execution.get_state()` - Get current execution state (status, exit_code, etc.)
- `execution.result()` - Wait for completion and return `ExecutionResult`
- `execution.kill()` - Terminate the running process
- `execution.execution_id` - Get the execution ID (property)
- `execution.devbox_id` - Get the devbox ID (property)

#### Execution Results

The `ExecutionResult` object contains the output and exit status of a completed command:

```python
# From synchronous execution
result = devbox.cmd.exec(command="ls -la /tmp")

# Or from asynchronous execution
execution = devbox.cmd.exec_async(command="echo 'test'")
result = execution.result()

# Access execution results
print("Exit code:", result.exit_code)
print("Success:", result.success)  # True if exit code is 0
print("Failed:", result.failed)    # True if exit code is non-zero

# Get output streams
stdout = result.stdout()
stderr = result.stderr()
print("Standard output:", stdout)
print("Standard error:", stderr)

# Access raw result data
raw_result = result.raw
print("Raw result:", raw_result)
```

**Key methods and properties:**

- `result.exit_code` - The process exit code (property)
- `result.success` - Boolean indicating success (exit code 0) (property)
- `result.failed` - Boolean indicating failure (non-zero exit code) (property)
- `result.stdout()` - Get standard output as string
- `result.stderr()` - Get standard error as string
- `result.raw` - Get the raw result data (property)

#### Streaming Command Output

> **Callback requirement:** All callbacks (`stdout`, `stderr`, `output`) must be synchronous functions. Even when using `AsyncDevbox`, callbacks cannot be async. Use thread-safe queues or other coordination primitives if you need to bridge into async code.

Pass callbacks into `cmd.exec` / `cmd.exec_async` to process logs in real time:

```python
def handle_output(line: str) -> None:
    print("LOG:", line)

result = devbox.cmd.exec(
    command="python train.py",
    stdout=handle_output,
    stderr=lambda line: print("ERR:", line),
    output=lambda line: print("ANY:", line),
)
print("exit code:", result.exit_code)
```

Async example (note that the callback itself is still synchronous):

```python
def capture(line: str) -> None:
    # Callbacks must be synchronous
    # Use thread-safe data structures if needed
    log_queue.put_nowait(line)

await devbox.cmd.exec(
    command="tail -f /var/log/app.log",
    stdout=capture,
)
```

#### File Operations

```python
# Write files
devbox.file.write(
    path="/home/user/app.js",
    contents='console.log("Hello from devbox!");',
)

# Read files
content = devbox.file.read(path="/home/user/app.js")
print(content)

# Upload files
from pathlib import Path
devbox.file.upload(
    path="/home/user/upload.txt",
    file=Path("local_file.txt"),
)

# Download files
data = devbox.file.download(path="/home/user/download.txt")
with open("local_download.txt", "wb") as f:
    f.write(data)
```

#### Network Operations

```python
# Create SSH key for remote access
ssh_key = devbox.net.create_ssh_key()
print("SSH URL:", ssh_key.url)

# Create tunnel to expose port
tunnel = devbox.net.create_tunnel(port=8080)
print("Public URL:", tunnel.url)

# Remove tunnel when done
devbox.net.remove_tunnel(port=8080)
```

#### Snapshot Operations

```python
# Create a snapshot (waits for completion)
snapshot = devbox.snapshot_disk(
    name="my-snapshot",
    commit_message="Added new features",
)

# Create a snapshot asynchronously (returns immediately)
snapshot = devbox.snapshot_disk_async(
    name="my-snapshot",
    commit_message="Added new features",
)
# Wait for it to complete later
snapshot.await_completed()

# Create new devbox from snapshot
new_devbox = snapshot.create_devbox(name="devbox-from-snapshot")
```

#### Devbox Lifecycle Management

```python
# Suspend devbox (pause without losing state)
devbox.suspend()

# Resume suspended devbox
devbox.resume()

# Keep devbox alive (extend timeout)
devbox.keep_alive()

# Wait for devbox to reach running state
devbox.await_running()

# Wait for devbox to be suspended
devbox.await_suspended()

# Shutdown devbox
devbox.shutdown()
```

#### Context Manager Support

Devboxes support context managers for automatic cleanup:

```python
# Synchronous
with runloop.devbox.create(name="temp-devbox") as devbox:
    result = devbox.cmd.exec(command="echo 'Hello'")
    print(result.stdout())
# devbox is automatically shutdown when exiting the context

# Asynchronous
async with await runloop.devbox.create(name="temp-devbox") as devbox:
    result = await devbox.cmd.exec(command="echo 'Hello'")
    print(await result.stdout())
# devbox is automatically shutdown when exiting the context
```

**Key methods:**

- `devbox.get_info()` - Get devbox details and status
- `devbox.cmd.exec()` - Execute commands synchronously
- `devbox.cmd.exec_async()` - Execute commands asynchronously
- `devbox.file.read()` - Read file contents
- `devbox.file.write()` - Write file contents
- `devbox.file.upload()` - Upload files
- `devbox.file.download()` - Download files
- `devbox.net.create_ssh_key()` - Create SSH key for remote access
- `devbox.net.create_tunnel()` - Create network tunnel
- `devbox.net.remove_tunnel()` - Remove network tunnel
- `devbox.snapshot_disk()` - Create disk snapshot (waits for completion)
- `devbox.snapshot_disk_async()` - Create disk snapshot (async)
- `devbox.suspend()` - Suspend devbox
- `devbox.resume()` - Resume suspended devbox
- `devbox.keep_alive()` - Extend devbox timeout
- `devbox.await_running()` - Wait for devbox to be running
- `devbox.await_suspended()` - Wait for devbox to be suspended
- `devbox.shutdown()` - Shutdown the devbox

### Blueprint

Object-oriented interface for working with blueprints. Created via `runloop.blueprint.create()` or `runloop.blueprint.from_id()`:

```python
# Create a new blueprint
blueprint = runloop.blueprint.create(
    name="my-blueprint",
    dockerfile="FROM ubuntu:22.04\nRUN apt-get update && apt-get install -y python3\n",
    system_setup_commands=["pip install numpy pandas"],
)

# Or get an existing one
blueprint = runloop.blueprint.from_id(blueprint_id="bpt_123")

# List all blueprints
blueprints = runloop.blueprint.list()

# Get blueprint details and build logs
info = blueprint.get_info()
logs = blueprint.logs()

# Create a devbox from this blueprint
devbox = blueprint.create_devbox(name="devbox-from-blueprint")

# Delete the blueprint when done
blueprint.delete()
```

**Key methods:**

- `blueprint.get_info()` - Get blueprint details
- `blueprint.logs()` - Get build logs for the blueprint
- `blueprint.delete()` - Delete the blueprint
- `blueprint.create_devbox()` - Create a devbox from this blueprint

### Snapshot

Object-oriented interface for working with disk snapshots. Created via `runloop.snapshot.from_id()`:

```python
# Get an existing snapshot
snapshot = runloop.snapshot.from_id(snapshot_id="snp_123")

# List all snapshots
snapshots = runloop.snapshot.list()

# List snapshots for a specific devbox
devbox_snapshots = runloop.snapshot.list(devbox_id="dbx_123")

# Get snapshot details and check status
info = snapshot.get_info()
print(f"Snapshot status: {info.status}")

# Update snapshot metadata
snapshot.update(
    name="updated-snapshot-name",
    metadata={"version": "v2.0"},
)

# Wait for async snapshot to complete
snapshot.await_completed()

# Create a devbox from this snapshot
devbox = snapshot.create_devbox(name="devbox-from-snapshot")

# Delete the snapshot when done
snapshot.delete()
```

**Key methods:**

- `snapshot.get_info()` - Get snapshot details and status
- `snapshot.update()` - Update snapshot name and metadata
- `snapshot.delete()` - Delete the snapshot
- `snapshot.await_completed()` - Wait for snapshot completion
- `snapshot.create_devbox()` - Create a devbox from this snapshot

### StorageObject

Object-oriented interface for working with storage objects. Created via `runloop.storage_object.create()` or `runloop.storage_object.from_id()`:

```python
# Create a new storage object
storage_object = runloop.storage_object.create(
    name="my-file.txt",
    content_type="text",
    metadata={"project": "demo"},
)

# Upload content to the object
storage_object.upload_content("Hello, World!")
storage_object.complete()

# Upload from file
from pathlib import Path
uploaded = runloop.storage_object.upload_from_file(
    Path("/path/to/file.txt"),
    name="my-file.txt",
)

# Upload text content directly
uploaded = runloop.storage_object.upload_from_text(
    "Hello, World!",
    name="my-text.txt",
    metadata={"source": "text"},
)

# Upload from bytes
uploaded = runloop.storage_object.upload_from_bytes(
    b"binary content",
    name="my-file.bin",
    content_type="binary",
)

# Get object details and download
info = storage_object.refresh()
download_url = storage_object.get_download_url(duration_seconds=3600)

# Download content
text_content = storage_object.download_as_text()
binary_content = storage_object.download_as_bytes()

# List all storage objects
objects = runloop.storage_object.list()

# Delete when done
storage_object.delete()
```

#### Storage Object Upload Helpers

The storage helpers manage the multi-step upload flow (create → PUT to presigned URL → complete):

```python
from pathlib import Path

# Upload local file with content-type detection
obj = runloop.storage_object.upload_from_file(file_path=Path("./report.csv"))

# Manual control
obj = runloop.storage_object.create(
    name="data.bin",
    content_type="binary",
)
obj.upload_content(b"\xDE\xAD\xBE\xEF")
obj.complete()
```

**Key methods:**

- `storage_object.refresh()` - Get updated object details
- `storage_object.upload_content()` - Upload content to the object
- `storage_object.complete()` - Mark upload as complete
- `storage_object.get_download_url()` - Get presigned download URL
- `storage_object.download_as_text()` - Download content as text
- `storage_object.download_as_bytes()` - Download content as bytes
- `storage_object.delete()` - Delete the object

**Static upload methods:**

- `runloop.storage_object.upload_from_file()` - Upload from filesystem
- `runloop.storage_object.upload_from_text()` - Upload text content directly
- `runloop.storage_object.upload_from_bytes()` - Upload from bytes

### Mounting Storage Objects to Devboxes

You can mount storage objects to devboxes to access their contents:

```python
# Create a storage object first
storage_object = runloop.storage_object.upload_from_text(
    "Hello, World!",
    name="my-data.txt",
)

# Create a devbox and mount the storage object
devbox = runloop.devbox.create(
    name="my-devbox",
    mounts=[
        {
            "type": "object_mount",
            "object_id": storage_object.id,
            "object_path": "/home/user/data.txt",
        },
    ],
)

# The storage object is now accessible at /home/user/data.txt in the devbox
result = devbox.cmd.exec(command="cat /home/user/data.txt")
print(result.stdout())  # "Hello, World!"

# Mount archived objects (tar, tgz, gzip) - they get extracted to a directory
archive_object = runloop.storage_object.upload_from_file(
    Path("./project.tar.gz"),
    name="project.tar.gz",
)

devbox_with_archive = runloop.devbox.create(
    name="archive-devbox",
    mounts=[
        {
            "type": "object_mount",
            "object_id": archive_object.id,
            "object_path": "/home/user/project",  # Archive gets extracted here
        },
    ],
)

# Access extracted archive contents
result = devbox_with_archive.cmd.exec(command="ls -la /home/user/project/")
print(result.stdout())
```

## Accessing the Underlying REST Client

The SDK always exposes the underlying client through the `.api` attribute:

```python
runloop = RunloopSDK()
raw_devbox = runloop.api.devboxes.create()
```

This makes it straightforward to mix high-level helpers with low-level calls whenever you need advanced control.

## Error Handling

The SDK provides comprehensive error handling with typed exceptions:

```python
from runloop_api_client import RunloopSDK
import runloop_api_client

runloop = RunloopSDK()

try:
    devbox = runloop.devbox.create(name="example-devbox")
    result = devbox.cmd.exec(command="invalid-command")
except runloop_api_client.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except runloop_api_client.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except runloop_api_client.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as follows:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

## Advanced Configuration

```python
import httpx
from runloop_api_client import RunloopSDK, DefaultHttpxClient

runloop = RunloopSDK(
    bearer_token="your-api-key",  # defaults to RUNLOOP_API_KEY env var
    base_url="https://api.runloop.ai",  # or use RUNLOOP_BASE_URL env var
    timeout=60.0,  # 60 second timeout (default is 30)
    max_retries=3,  # Retry failed requests (default is 5)
    default_headers={
        "X-Custom-Header": "value",
    },
    # Custom HTTP client with proxy
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Async Usage

The async SDK has the same interface as the synchronous version, but all I/O operations are async:

```python
import asyncio
from runloop_api_client import AsyncRunloopSDK

async def main():
    runloop = AsyncRunloopSDK()
    
    # All the same operations, but with await
    async with await runloop.devbox.create(name="async-devbox") as devbox:
        result = await devbox.cmd.exec(command="pwd")
        print(await result.stdout())
        
        # Streaming (note: callbacks must be synchronous)
        def capture(line: str) -> None:
            print(">>", line)
        
        await devbox.cmd.exec(command="ls", stdout=capture)
        
        # Async file operations
        await devbox.file.write(path="/tmp/test.txt", contents="Hello")
        content = await devbox.file.read(path="/tmp/test.txt")
        
        # Async network operations
        tunnel = await devbox.net.create_tunnel(port=8080)
        print("Tunnel URL:", tunnel.url)

asyncio.run(main())
```

## Polling Configuration

Many operations that wait for state changes accept a `polling_config` parameter:

```python
from runloop_api_client.lib.polling import PollingConfig

# Create devbox with custom polling
devbox = runloop.devbox.create(
    name="my-devbox",
    polling_config=PollingConfig(
        timeout_seconds=300.0,  # Wait up to 5 minutes
        interval_seconds=2.0,   # Poll every 2 seconds
    ),
)

# Wait for snapshot completion with custom polling
snapshot.await_completed(
    polling_config=PollingConfig(
        timeout_seconds=600.0,  # Wait up to 10 minutes
        interval_seconds=5.0,   # Poll every 5 seconds
    ),
)
```

## Complete API Reference

For the full REST API documentation and all available parameters, see:

- **[api.md](api.md)** - Complete REST API documentation
- **[README.md](README.md)** - Advanced topics (retries, timeouts, error handling, pagination)

## Feedback

The object-oriented SDK is new for Python—feedback and ideas are welcome! Please open an issue or pull request on GitHub if you spot gaps, bugs, or ergonomic improvements.
