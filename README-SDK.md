# Runloop SDK – Python Object-Oriented Client

The `RunloopSDK` builds on top of the generated REST client and provides a Pythonic, object-oriented API for managing devboxes, blueprints, snapshots, and storage objects. The SDK exposes synchronous and asynchronous variants to match your runtime requirements.

> **Installation**  
> The SDK ships with the `runloop_api_client` package—no extra dependencies are required.

```bash
pip install runloop_api_client
```

## Quickstart (synchronous)

```python
from runloop_api_client import RunloopSDK

sdk = RunloopSDK()

# Create a ready-to-use devbox
with sdk.devbox.create(name="my-devbox") as devbox:
    result = devbox.cmd.exec("echo 'Hello from Runloop!'")
    print(result.stdout())

    # Stream stdout in real time
    devbox.cmd.exec(
        "ls -la",
        stdout=lambda line: print("stdout:", line),
        output=lambda line: print("combined:", line),
    )

# Blueprints
blueprint = sdk.blueprint.create(
    name="my-blueprint",
    dockerfile="FROM ubuntu:22.04\nRUN echo 'Hello' > /hello.txt\n",
)
devbox = blueprint.create_devbox(name="dev-from-blueprint")

# Storage objects
obj = sdk.storage_object.upload_from_text("Hello world!", name="greeting.txt")
print(obj.download_as_text())
```

## Quickstart (asynchronous)

```python
import asyncio
from runloop_api_client import AsyncRunloopSDK

async def main():
    sdk = AsyncRunloopSDK()
    async with sdk.devbox.create(name="async-devbox") as devbox:
        result = await devbox.cmd.exec("pwd")
        print(await result.stdout())

        async def capture(line: str) -> None:
            print(">>", line)

        await devbox.cmd.exec("ls", stdout=capture)

asyncio.run(main())
```

## Available Resources

- **Devbox / AsyncDevbox**
  - Creation helpers (`create`, `create_from_blueprint_id`, `create_from_snapshot`, `from_id`)
  - Lifecycle management (`await_running`, `suspend`, `resume`, `keep_alive`, `shutdown`)
  - Command execution (`cmd.exec`, `cmd.exec_async`) with optional streaming callbacks
  - File operations (`read`, `write`, `upload`, `download`)
  - Network helpers (`net.create_ssh_key`, `net.create_tunnel`, `net.remove_tunnel`)

- **Blueprint / AsyncBlueprint**
  - Build orchestration (`create`)
  - Fetch metadata & logs (`get_info`, `logs`)
  - Spawn devboxes from existing blueprints (`create_devbox`)

- **Snapshot / AsyncSnapshot**
  - List and inspect snapshots (`list`, `get_info`, `await_completed`)
  - Metadata updates (`update`), deletion (`delete`)
  - Provision new devboxes from snapshots (`create_devbox`)

- **StorageObject / AsyncStorageObject**
  - Object creation (`create`, `from_id`, `list`)
  - Convenience uploads (`upload_from_file`, `upload_from_text`, `upload_from_bytes`)
  - Manual uploads via presigned URLs (`upload_content`, `complete`)
  - Downloads (`download_as_text`, `download_as_bytes`)

All objects expose the low-level REST ID through the `id` property, making it easy to cross-reference with existing tooling.

## Streaming Command Output

Pass callbacks into `cmd.exec` / `cmd.exec_async` to process logs in real time. Synchronous callbacks receive strings; asynchronous callbacks may return either `None` or `Awaitable[None]`.

```python
def handle_output(line: str) -> None:
    print("LOG:", line)

result = devbox.cmd.exec(
    "python train.py",
    stdout=handle_output,
    stderr=lambda line: print("ERR:", line),
    output=lambda line: print("ANY:", line),
)
print("exit code:", result.exit_code)
```

Async example:

```python
async def capture(line: str) -> None:
    await log_queue.put(line)

await devbox.cmd.exec(
    "tail -f /var/log/app.log",
    stdout=capture,
)
```

## Storage Object Upload Helpers

The storage helpers manage the multi-step upload flow (create → PUT to presigned URL → complete):

```python
from pathlib import Path

# Upload local file with content-type detection
obj = sdk.storage_object.upload_from_file(Path("./report.csv"))

# Manual control
obj = sdk.storage_object.create("data.bin", content_type="binary")
obj.upload_content(b"\xDE\xAD\xBE\xEF")
obj.complete()
```

## Accessing the Generated REST Client

The SDK always exposes the underlying generated client through the `.api` attribute:

```python
sdk = RunloopSDK()
raw_devbox = sdk.api.devboxes.create()
```

This makes it straightforward to mix high-level helpers with low-level calls whenever you need advanced control.

## Feedback

The object-oriented SDK is new for Python—feedback and ideas are welcome! Please open an issue or pull request on GitHub if you spot gaps, bugs, or ergonomic improvements.

