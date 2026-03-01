# Runloop Python SDK - LLM Reference Guide

This document provides comprehensive reference information for LLMs to generate code using the Runloop Python SDK. The SDK provides both a high-level object-oriented interface and low-level REST API access for managing cloud development environments (devboxes), blueprints, snapshots, and more.

## Table of Contents

1. [Quick Start](#quick-start)
2. [SDK Architecture](#sdk-architecture)
3. [Core Resources - Devbox](#devbox)
4. [Core Resources - Blueprint](#blueprint)
5. [Core Resources - Snapshot](#snapshot)
6. [Core Resources - StorageObject](#storageobject)
7. [Evaluation Framework](#evaluation-framework)
8. [Network Policies](#network-policies)
9. [REST API Reference](#rest-api-reference)
10. [Common Patterns](#common-patterns)
11. [Type Reference Index](#type-reference-index)

---

## Quick Start

### Installation

```bash
pip install runloop-api-client
```

### Authentication

Set the `RUNLOOP_API_KEY` environment variable, or pass `bearer_token` to the SDK constructor.

### Basic Example (Async - Recommended)

```python
import asyncio
from runloop_api_client.sdk import AsyncRunloopSDK

async def main():
    async with AsyncRunloopSDK() as runloop:
        # Create a devbox and wait for it to be running
        devbox = await runloop.devbox.create(name="my-devbox")

        # Execute a command
        result = await devbox.cmd.exec("echo 'Hello, World!'")
        print(await result.stdout())
        print(f"Exit code: {result.exit_code}")

        # Shutdown
        await devbox.shutdown()

asyncio.run(main())
```

### Sync Example

```python
from runloop_api_client.sdk import RunloopSDK

runloop = RunloopSDK()
with runloop.devbox.create(name="my-devbox") as devbox:
    result = devbox.cmd.exec("echo 'Hello'")
    print(result.stdout())
# Devbox auto-shuts down on context exit
```

---

## SDK Architecture

### Layer Overview

```
┌─────────────────────────────────────────────┐
│  Your Code                                  │
├─────────────────────────────────────────────┤
│  OO SDK Layer (AsyncRunloopSDK/RunloopSDK)  │
│  - AsyncDevboxOps, AsyncBlueprintOps, etc.  │
│  - AsyncDevbox, AsyncBlueprint, etc.        │
├─────────────────────────────────────────────┤
│  REST API Resources (resources/)            │
│  - DevboxesResource, BlueprintsResource     │
├─────────────────────────────────────────────┤
│  Base Client (AsyncRunloop/Runloop)         │
│  - httpx-based HTTP, retries, polling       │
└─────────────────────────────────────────────┘
```

### Entry Points

| Class | Import | Description |
|-------|--------|-------------|
| `AsyncRunloopSDK` | `from runloop_api_client.sdk import AsyncRunloopSDK` | Async OO SDK (recommended) |
| `RunloopSDK` | `from runloop_api_client.sdk import RunloopSDK` | Sync OO SDK |
| `AsyncRunloop` | `from runloop_api_client import AsyncRunloop` | Async REST client |
| `Runloop` | `from runloop_api_client import Runloop` | Sync REST client |

### SDK Constructor Parameters

```python
AsyncRunloopSDK(
    bearer_token: str | None = None,      # API key (default: RUNLOOP_API_KEY env)
    base_url: str | httpx.URL | None = None,
    timeout: float | Timeout | None = not_given,
    max_retries: int = 2,
    default_headers: Mapping[str, str] | None = None,
    http_client: httpx.AsyncClient | None = None,
)
```

### Resource Managers

The SDK provides these high-level managers via properties:

```python
runloop.devbox           # AsyncDevboxOps - create/list devboxes
runloop.blueprint        # AsyncBlueprintOps - create/list blueprints
runloop.snapshot         # AsyncSnapshotOps - list snapshots
runloop.storage_object   # AsyncStorageObjectOps - upload/download objects
runloop.scenario         # AsyncScenarioOps - manage evaluation scenarios
runloop.benchmark        # AsyncBenchmarkOps - manage benchmarks
runloop.agent            # AsyncAgentOps - manage agents
runloop.scorer           # AsyncScorerOps - manage scorers
runloop.network_policy   # AsyncNetworkPolicyOps - manage network policies
runloop.api              # Direct access to REST client (AsyncRunloop)
```

---

## Devbox

A Devbox is an isolated virtual development environment for running code. It's the primary resource you'll interact with.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncDevboxOps)
- `src/runloop_api_client/sdk/async_devbox.py` (AsyncDevbox)
- `src/runloop_api_client/sdk/devbox.py` (sync Devbox)

### Creating Devboxes

#### AsyncDevboxOps Methods

```python
# Create a new devbox (waits until running)
devbox = await runloop.devbox.create(
    name="my-devbox",                    # Optional display name
    blueprint_id="bp_xxx",               # Create from blueprint ID
    blueprint_name="my-blueprint",       # OR create from blueprint name (latest)
    snapshot_id="snap_xxx",              # OR restore from snapshot
    environment_variables={"KEY": "val"},
    launch_parameters={...},             # Resource configuration
    mounts=[...],                        # File/object mounts
    entrypoint="./start.sh",             # Script to run on boot
    metadata={"team": "ml"},             # Custom metadata
)

# Create from specific sources
devbox = await runloop.devbox.create_from_blueprint_id("bp_xxx", name="dev")
devbox = await runloop.devbox.create_from_blueprint_name("my-blueprint")
devbox = await runloop.devbox.create_from_snapshot("snap_xxx")

# Attach to existing devbox (returns immediately, no waiting)
devbox = runloop.devbox.from_id("dbx_xxx")

# List devboxes
devboxes = await runloop.devbox.list(
    limit=20,
    status="running",           # Filter by status
    starting_after="dbx_xxx",   # Pagination cursor
)
```

### Devbox Instance

#### Properties and Lifecycle

```python
devbox.id                        # Unique devbox identifier

# Get current state
info = await devbox.get_info()   # Returns DevboxView
print(info.status)               # "running", "suspended", etc.

# Wait for state transitions
await devbox.await_running()     # Block until running
await devbox.await_suspended()   # Block until suspended

# Lifecycle management
await devbox.shutdown()          # Terminate and release resources
await devbox.suspend()           # Pause, preserving state (waits)
await devbox.resume()            # Wake from suspension (waits)
await devbox.resume_async()      # Wake without waiting
await devbox.keep_alive()        # Extend timeout

# Context manager support (auto-shutdown)
async with await runloop.devbox.create() as devbox:
    await devbox.cmd.exec("make build")
# Automatically shut down here
```

### Command Execution (devbox.cmd)

The `CommandInterface` provides methods to run shell commands.

```python
# Synchronous execution (waits for completion)
result = await devbox.cmd.exec(
    "python train.py",
    shell_name="main",           # Use named shell for state persistence
    working_directory="/app",    # Override CWD
    user="root",                 # Run as specific user

    # Streaming callbacks (receive output in real-time)
    stdout=lambda line: print(f"[OUT] {line}"),
    stderr=lambda line: print(f"[ERR] {line}"),
    output=lambda line: print(line),  # Both stdout and stderr
)

# Check results
print(result.exit_code)          # 0 for success
print(result.success)            # True if exit_code == 0
print(result.failed)             # True if exit_code != 0
print(await result.stdout())     # Get stdout (streams if truncated)
print(await result.stderr())     # Get stderr
print(await result.stdout(50))   # Last 50 lines only

# Async execution (fire-and-forget with management)
execution = await devbox.cmd.exec_async("long_process.sh")
state = await execution.get_state()   # Poll current state
print(state.status)                   # "running", "completed", etc.
await execution.kill()                # Terminate early
result = await execution.result()     # Wait for completion
```

### Named Shells (Stateful Sessions)

Named shells maintain environment variables and CWD across commands.

```python
# Create/attach to a named shell
shell = devbox.shell("my-session")   # Specify name
shell = devbox.shell()               # Auto-generated UUID name

# Commands share state
await shell.exec("cd /app")
await shell.exec("export API_KEY=secret")
result = await shell.exec("echo $API_KEY && pwd")
# Outputs: secret\n/app

# Async execution in named shell
execution = await shell.exec_async("npm install")
```

### File Operations (devbox.file)

```python
# Read file contents
content = await devbox.file.read(file_path="/app/config.json")

# Write file (creates or overwrites)
await devbox.file.write(
    file_path="/app/data.txt",
    contents="Hello, World!",
)

# Download file as bytes
data = await devbox.file.download(file_path="/app/model.bin")

# Upload file from local filesystem
from pathlib import Path
await devbox.file.upload(
    file_path="/app/input.csv",
    file=Path("./local_data.csv"),
)
```

### Network Operations (devbox.net)

```python
# Create SSH key for remote access
ssh_info = await devbox.net.create_ssh_key()
print(ssh_info.url)              # SSH connection URL
print(ssh_info.private_key)      # Private key content

# Create public tunnel to a port
tunnel = await devbox.net.create_tunnel(port=8080)
print(tunnel.url)                # Public URL

# Remove tunnel
await devbox.net.remove_tunnel(port=8080)
```

### Snapshots

```python
# Create snapshot (waits for completion)
snapshot = await devbox.snapshot_disk(name="checkpoint-v1")

# Create snapshot async (returns immediately)
snapshot = await devbox.snapshot_disk_async()
await snapshot.await_completed()  # Wait later
```

### DevboxView (State Object)

When you call `get_info()`, you receive a `DevboxView`:

**Key fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique devbox ID |
| `status` | `Literal[...]` | Current state (see below) |
| `name` | `str \| None` | Display name |
| `blueprint_id` | `str \| None` | Source blueprint ID |
| `snapshot_id` | `str \| None` | Source snapshot ID |
| `create_time_ms` | `int` | Creation timestamp |
| `end_time_ms` | `int \| None` | Termination timestamp |
| `metadata` | `Dict[str, str]` | Custom metadata |
| `launch_parameters` | `LaunchParameters` | Resource configuration |
| `failure_reason` | `Literal[...] \| None` | Why it failed |
| `shutdown_reason` | `Literal[...] \| None` | Why it shut down |

**Status values:**
- `provisioning` - Allocating resources
- `initializing` - Running boot scripts
- `running` - Ready for interaction
- `suspending` - Creating suspension snapshot
- `suspended` - Paused, no compute used
- `resuming` - Restoring from suspension
- `failure` - Boot or execution failed
- `shutdown` - Successfully terminated

**Full type definition:** `src/runloop_api_client/types/devbox_view.py`

### DevboxCreateParams

**Key parameters for devbox creation:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str \| None` | Display name |
| `blueprint_id` | `str \| None` | Create from blueprint |
| `blueprint_name` | `str \| None` | Create from latest blueprint with name |
| `snapshot_id` | `str \| None` | Restore from snapshot |
| `environment_variables` | `Dict[str, str]` | Env vars for the devbox |
| `secrets` | `Dict[str, str]` | Map env var names to secret names |
| `mounts` | `Iterable[Mount]` | Files/objects to mount |
| `entrypoint` | `str \| None` | Script to run (devbox lifecycle bound to it) |
| `launch_parameters` | `LaunchParameters` | Resource sizing and behavior |
| `metadata` | `Dict[str, str]` | Custom key-value metadata |

**Full type definition:** `src/runloop_api_client/types/devbox_create_params.py`

### LaunchParameters

Resource and behavior configuration:

```python
launch_parameters = {
    "resource_size_request": "MEDIUM",   # X_SMALL, SMALL, MEDIUM, LARGE, X_LARGE, XX_LARGE
    # OR custom sizing:
    "custom_cpu_cores": 4,               # 1-16, must be multiple of 2
    "custom_gb_memory": 8,               # 2-64 GiB, multiple of 2
    "custom_disk_size": 20,              # 2-64 GiB, multiple of 2

    "architecture": "x86_64",            # or "arm64"
    "keep_alive_time_seconds": 3600,     # Auto-shutdown after idle (max 172800)
    "launch_commands": ["npm install"],  # Run before entrypoint
    "available_ports": [8080, 3000],     # Ports for tunneling
    "network_policy_id": "np_xxx",       # Network restrictions

    "after_idle": {                      # Idle-based lifecycle
        "idle_time_seconds": 300,
        "on_idle": "suspend",            # or "shutdown"
    },
}
```

**Full type definition:** `src/runloop_api_client/types/shared_params/launch_parameters.py`

### Mount Types

```python
# Object mount - mount a storage object
object_mount = {
    "type": "object_mount",
    "object_id": "obj_xxx",
    "object_path": "/data/input.csv",    # Target path in devbox
}

# File mount - inline file content
file_mount = {
    "type": "file_mount",
    "target": "/app/config.json",
    "content": '{"key": "value"}',
}

# Code mount - clone a git repo
code_mount = {
    "type": "code_mount",
    "repo_owner": "myorg",
    "repo_name": "myrepo",
    "token": "ghp_xxx",                  # Optional auth token
    "install_command": "npm install",    # Optional setup
}

# Agent mount - mount an agent package
agent_mount = {
    "type": "agent_mount",
    "agent_id": "agt_xxx",
    "agent_path": "/app/agent",
}
```

**Full type definition:** `src/runloop_api_client/types/shared_params/mount.py`

---

## Blueprint

A Blueprint is a reusable container image definition for creating devboxes.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncBlueprintOps)
- `src/runloop_api_client/sdk/async_blueprint.py` (AsyncBlueprint)

### Creating Blueprints

```python
# Create from Dockerfile (waits for build to complete)
blueprint = await runloop.blueprint.create(
    name="my-blueprint",
    dockerfile="FROM node:22\nRUN npm install -g typescript",
    system_setup_commands=["apt-get update"],  # Run before Dockerfile
)

# With build context (upload local directory)
from datetime import timedelta

# First upload the context as a storage object
context_obj = await runloop.storage_object.upload_from_dir(
    "./my-app",
    ttl=timedelta(hours=1),
)

blueprint = await runloop.blueprint.create(
    name="my-app-blueprint",
    dockerfile="FROM python:3.12\nCOPY . /app\nWORKDIR /app\nRUN pip install -r requirements.txt",
    build_context=context_obj.as_build_context(),
)

# Get blueprint by ID
blueprint = runloop.blueprint.from_id("bp_xxx")

# List blueprints
blueprints = await runloop.blueprint.list(limit=20)
```

### Blueprint Instance

```python
blueprint.id                     # Unique blueprint ID

# Get current state
info = await blueprint.get_info()
print(info.status)               # "building", "built", "build_failed"

# Get build logs
logs = await blueprint.logs()
for entry in logs.logs:
    print(entry.message)

# Create devbox from this blueprint
devbox = await blueprint.create_devbox(name="dev-instance")

# Delete blueprint
await blueprint.delete()
```

### BlueprintView

**Key fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique blueprint ID |
| `name` | `str` | Display name |
| `status` | `Literal["building", "built", "build_failed"]` | Build state |
| `create_time_ms` | `int` | Creation timestamp |

**Full type definition:** `src/runloop_api_client/types/blueprint_view.py`

### BlueprintCreateParams

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Required display name |
| `dockerfile` | `str` | Dockerfile content |
| `build_context` | `BuildContext` | Optional build context |
| `system_setup_commands` | `list[str]` | Commands before Dockerfile |
| `launch_parameters` | `LaunchParameters` | Default devbox resources |

**Full type definition:** `src/runloop_api_client/types/blueprint_create_params.py`

---

## Snapshot

A Snapshot captures the disk state of a devbox for later restoration.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncSnapshotOps)
- `src/runloop_api_client/sdk/async_snapshot.py` (AsyncSnapshot)

### Working with Snapshots

```python
# List snapshots
snapshots = await runloop.snapshot.list(
    devbox_id="dbx_xxx",         # Filter by source devbox
    limit=20,
)

# Get snapshot by ID
snapshot = runloop.snapshot.from_id("snap_xxx")

# Get snapshot info
info = await snapshot.get_info()
print(info.status)               # "pending", "completed", "failed"

# Wait for snapshot to complete (if created async)
await snapshot.await_completed()

# Create devbox from snapshot
devbox = await snapshot.create_devbox(name="restored-dev")

# Update metadata
await snapshot.update(name="my-checkpoint")

# Delete snapshot
await snapshot.delete()
```

### DevboxSnapshotView

**Key fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique snapshot ID |
| `name` | `str \| None` | Display name |
| `devbox_id` | `str` | Source devbox |
| `status` | `Literal["pending", "completed", "failed"]` | Snapshot state |
| `create_time_ms` | `int` | Creation timestamp |

**Full type definition:** `src/runloop_api_client/types/devbox_snapshot_view.py`

---

## StorageObject

Storage objects provide cloud storage for files that can be mounted in devboxes or used as build contexts.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncStorageObjectOps)
- `src/runloop_api_client/sdk/async_storage_object.py` (AsyncStorageObject)

### Uploading Objects

```python
from pathlib import Path
from datetime import timedelta

# Upload from local file
obj = await runloop.storage_object.upload_from_file(
    Path("./data.csv"),
    name="training-data.csv",            # Optional, defaults to filename
    content_type="csv",                  # Optional MIME type
    metadata={"version": "1"},
    ttl=timedelta(hours=24),             # Auto-delete after TTL
)

# Upload from directory (creates tar.gz)
obj = await runloop.storage_object.upload_from_dir(
    "./my-project",
    name="project-context.tar.gz",
    ttl=timedelta(hours=1),
)

# Upload from text
obj = await runloop.storage_object.upload_from_text(
    "Hello, World!",
    name="greeting.txt",
)

# Upload from bytes
obj = await runloop.storage_object.upload_from_bytes(
    b"binary data",
    name="data.bin",
    content_type="binary",
)

# Manual upload flow (for large files or custom handling)
obj = await runloop.storage_object.create(
    name="large-file.bin",
    content_type="binary",
)
# obj.upload_url contains pre-signed URL
await obj.upload_content(large_bytes)
await obj.complete()  # Mark upload finished
```

### Downloading Objects

```python
# Get object by ID
obj = runloop.storage_object.from_id("obj_xxx")

# Download methods
data = await obj.download_as_bytes()
text = await obj.download_as_text()

# Get download URL (for external use)
url_info = await obj.get_download_url()
print(url_info.download_url)
```

### Using Objects

```python
# Use as build context for blueprints
blueprint = await runloop.blueprint.create(
    name="my-app",
    dockerfile="...",
    build_context=obj.as_build_context(),
)

# Mount in devbox
devbox = await runloop.devbox.create(
    mounts=[{
        "type": "object_mount",
        "object_id": obj.id,
        "object_path": "/data/input.csv",
    }]
)

# List and delete
objects = await runloop.storage_object.list()
await obj.delete()
```

### ObjectView

**Key fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique object ID |
| `name` | `str` | Display name |
| `content_type` | `str` | MIME type |
| `status` | `str` | Upload status |
| `upload_url` | `str \| None` | Pre-signed upload URL |

**Full type definition:** `src/runloop_api_client/types/object_view.py`

---

## Evaluation Framework

The SDK provides tools for evaluating AI agents: Scenarios define individual test cases, Benchmarks group scenarios, and Scorers measure performance.

### Scenarios

A Scenario defines a test environment and scoring criteria for an agent task.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncScenarioOps)
- `src/runloop_api_client/sdk/async_scenario.py` (AsyncScenario)
- `src/runloop_api_client/sdk/async_scenario_builder.py` (AsyncScenarioBuilder)

#### Creating Scenarios with Builder Pattern

```python
# Use the fluent builder API
builder = (
    runloop.scenario.builder("fix-login-bug")
    .from_blueprint(blueprint)                    # or .from_snapshot(snapshot)
    .with_working_directory("/app")
    .with_problem_statement("Fix the authentication bug in auth.py")
    .with_additional_context({"hint": "Check the token validation"})
    .add_test_command_scorer("tests", test_command="pytest tests/")
    .add_bash_script_scorer(
        "linting",
        bash_script="ruff check . && echo 'score=1.0' || echo 'score=0.0'",
        weight=0.3,
    )
    .with_reference_output("diff --git a/auth.py...")  # Gold patch
    .with_metadata({"difficulty": "medium"})
)

# Preview configuration
preview = builder.preview()

# Push to platform
scenario = await builder.push()
```

#### Scorer Types

```python
# Test-based scorer (runs test command, scores by pass rate)
.add_test_command_scorer(
    "unit-tests",
    test_command="pytest --tb=short",
    weight=1.0,
)

# Shell command scorer (exit code 0 = pass)
.add_shell_command_scorer(
    "build-check",
    command="npm run build",
    weight=0.5,
)

# Bash script scorer (outputs "score=X.X")
.add_bash_script_scorer(
    "custom-check",
    bash_script='''
        if grep -q "TODO" *.py; then
            echo "score=0.5"
        else
            echo "score=1.0"
        fi
    ''',
)

# Python script scorer (prints score to stdout)
.add_python_script_scorer(
    "complexity",
    python_script='''
        import ast
        # ... analyze code complexity ...
        print(0.8)
    ''',
)

# AST grep scorer (pattern matching)
.add_ast_grep_scorer(
    "no-eval",
    pattern="eval($$$)",
    search_directory="src/",
    weight=0.2,
)

# Custom registered scorer
.add_custom_scorer(
    "my-scorer",
    custom_scorer_type="my_registered_type",
    scorer_params={"threshold": 0.9},
)
```

#### Running Scenarios

```python
# Get existing scenario
scenario = runloop.scenario.from_id("scn_xxx")

# Start a run (waits for devbox to be ready)
run = await scenario.run(run_name="test-v1")

# Access the devbox
devbox = run.devbox
await devbox.cmd.exec("cat problem.txt")  # Read problem statement

# Let agent work...
await devbox.cmd.exec("git apply solution.patch")

# Score the result
scores = await run.score()
print(scores.aggregate_score)
for fn in scores.scoring_function_results:
    print(f"{fn.name}: {fn.score}")

# Complete the run
await run.complete()
```

### Benchmarks

A Benchmark groups multiple scenarios for aggregate evaluation.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncBenchmarkOps)
- `src/runloop_api_client/sdk/async_benchmark.py` (AsyncBenchmark)

```python
# Create benchmark
benchmark = await runloop.benchmark.create(
    name="code-fix-benchmark",
    scenario_ids=["scn_1", "scn_2", "scn_3"],
)

# Add/remove scenarios
await benchmark.add_scenarios(["scn_4", "scn_5"])
await benchmark.remove_scenarios(["scn_1"])

# Start a benchmark run
bench_run = await benchmark.start_run(run_name="evaluation-v1")

# Run each scenario
info = await benchmark.get_info()
for scenario_id in info.scenario_ids:
    scenario = runloop.scenario.from_id(scenario_id)
    scenario_run = await scenario.run(
        benchmark_run_id=bench_run.id,
        run_name="evaluation-v1",
    )
    # Let agent work on each scenario...
    await scenario_run.score()
    await scenario_run.complete()

# Get results
runs = await bench_run.list_scenario_runs()
```

### Agents

Register agent packages for use in evaluations.

```python
# Create agent from NPM package
agent = await runloop.agent.create_from_npm(
    name="my-agent",
    package_name="@myorg/coding-agent",
    agent_setup=["npm run build"],
)

# From pip package
agent = await runloop.agent.create_from_pip(
    name="python-agent",
    package_name="my-coding-agent",
)

# From git repository
agent = await runloop.agent.create_from_git(
    name="git-agent",
    repository="https://github.com/myorg/agent",
    ref="main",
    agent_setup=["pip install -e ."],
)

# From storage object (uploaded tar.gz)
agent = await runloop.agent.create_from_object(
    name="custom-agent",
    object_id=obj.id,
)

# List agents
agents = await runloop.agent.list()
```

### Scorers

Create reusable custom scorers.

```python
# Create scorer
scorer = await runloop.scorer.create(
    type="code_quality",
    bash_script='''
        pylint src/ --score=y | grep "rated at" | grep -oP "\\d+\\.\\d+" | head -1
    ''',
)

# List scorers
scorers = await runloop.scorer.list()
```

---

## Network Policies

Network policies restrict outbound network access from devboxes.

**Source files:**
- `src/runloop_api_client/sdk/async_.py` (AsyncNetworkPolicyOps)
- `src/runloop_api_client/sdk/async_network_policy.py` (AsyncNetworkPolicy)

```python
# Create policy with allowed hostnames
policy = await runloop.network_policy.create(
    name="github-only",
    allowed_hostnames=[
        "github.com",
        "*.githubusercontent.com",
        "api.github.com",
    ],
)

# Use in devbox
devbox = await runloop.devbox.create(
    launch_parameters={
        "network_policy_id": policy.id,
    }
)

# Or in blueprint (inherited by devboxes)
blueprint = await runloop.blueprint.create(
    name="restricted-blueprint",
    dockerfile="FROM python:3.12",
    launch_parameters={
        "network_policy_id": policy.id,
    },
)

# Manage policies
info = await policy.get_info()
await policy.update(allowed_hostnames=["pypi.org", "*.python.org"])
await policy.delete()

# List all policies
policies = await runloop.network_policy.list()
```

---

## REST API Reference

For advanced use cases, access the REST API directly via `runloop.api`.

### Resource Classes

```python
# Access REST resources
runloop.api.devboxes              # DevboxesResource
runloop.api.blueprints            # BlueprintsResource
runloop.api.objects               # ObjectsResource
runloop.api.scenarios             # ScenariosResource
runloop.api.benchmarks            # BenchmarksResource
runloop.api.benchmark_runs        # BenchmarkRunsResource
runloop.api.agents                # AgentsResource
runloop.api.network_policies      # NetworkPoliciesResource
runloop.api.secrets               # SecretsResource
runloop.api.repositories          # RepositoriesResource

# Nested resources
runloop.api.devboxes.executions   # Manage async executions
runloop.api.devboxes.disk_snapshots
runloop.api.devboxes.browsers     # Browser automation
runloop.api.devboxes.computers    # Computer use APIs
runloop.api.scenarios.scorers     # Scorer management
```

### Common REST Patterns

```python
# Standard CRUD operations
view = await runloop.api.devboxes.create(**params)
view = await runloop.api.devboxes.retrieve(devbox_id)
view = await runloop.api.devboxes.update(devbox_id, **params)
await runloop.api.devboxes.delete(devbox_id)

# Pagination
page = await runloop.api.devboxes.list(limit=20)
for devbox in page.devboxes:
    print(devbox.id)
# Or iterate automatically
async for devbox in runloop.api.devboxes.list():
    print(devbox.id)

# Raw response access
response = await runloop.api.devboxes.with_raw_response.retrieve(devbox_id)
print(response.headers)
view = response.parse()

# Polling helpers (built into REST client)
view = await runloop.api.devboxes.create_and_await_running(**params)
view = await runloop.api.devboxes.await_running(devbox_id, polling_config=PollingConfig(...))
```

### Execution Resource

```python
# Start async execution
exec_view = await runloop.api.devboxes.execute_async(
    devbox_id,
    command="python train.py",
)

# Poll execution state
state = await runloop.api.devboxes.executions.retrieve(
    exec_view.execution_id,
    devbox_id=devbox_id,
)

# Wait for completion
final = await runloop.api.devboxes.executions.await_completed(
    exec_view.execution_id,
    devbox_id=devbox_id,
)

# Stream output
async for chunk in runloop.api.devboxes.executions.stream_stdout_updates(
    execution_id,
    devbox_id=devbox_id,
):
    print(chunk.output, end="")

# Kill execution
await runloop.api.devboxes.executions.kill(execution_id, devbox_id=devbox_id)
```

**REST resource files:** `src/runloop_api_client/resources/`

---

## Common Patterns

### Streaming Command Output

```python
# Real-time output with callbacks
async def log_handler(line: str):
    print(f"[{time.time():.2f}] {line}")

result = await devbox.cmd.exec(
    "npm install && npm run build",
    stdout=log_handler,
    stderr=log_handler,
)
```

### Long-Running Commands

```python
# Start process in background
execution = await devbox.cmd.exec_async("python long_training.py")

# Do other work...
await asyncio.sleep(10)

# Check status periodically
state = await execution.get_state()
if state.status == "running":
    print("Still running...")

# Wait for completion when ready
result = await execution.result()
```

### Error Handling

```python
from runloop_api_client import APIError, APIStatusError, RateLimitError

try:
    devbox = await runloop.devbox.create()
except RateLimitError:
    await asyncio.sleep(60)
    devbox = await runloop.devbox.create()
except APIStatusError as e:
    print(f"HTTP {e.status_code}: {e.message}")
except APIError as e:
    print(f"API error: {e}")
```

### Polling Configuration

```python
from runloop_api_client.lib.polling import PollingConfig, PollingTimeout

config = PollingConfig(
    interval_seconds=2.0,      # Poll every 2 seconds
    max_attempts=60,           # Max 60 attempts
    timeout_seconds=120.0,     # Total timeout
)

try:
    await devbox.await_running(polling_config=config)
except PollingTimeout as e:
    print(f"Timed out. Last state: {e.last_value}")
```

### Cleanup Patterns

```python
# Context manager (recommended)
async with AsyncRunloopSDK() as runloop:
    async with await runloop.devbox.create() as devbox:
        await devbox.cmd.exec("make test")
    # Devbox auto-shutdown
# SDK connection closed

# Manual cleanup
runloop = AsyncRunloopSDK()
devbox = await runloop.devbox.create()
try:
    await devbox.cmd.exec("make test")
finally:
    await devbox.shutdown()
    await runloop.aclose()
```

### Build Context from Directory

```python
from runloop_api_client.lib.context_loader import build_docker_context_tar

# Create tar respecting .dockerignore
tar_bytes = build_docker_context_tar(Path("./my-project"))

# Upload and use as build context
obj = await runloop.storage_object.upload_from_bytes(
    tar_bytes,
    name="context.tar.gz",
    content_type="tgz",
)

blueprint = await runloop.blueprint.create(
    name="my-app",
    dockerfile=Path("./my-project/Dockerfile").read_text(),
    build_context=obj.as_build_context(),
)
```

---

## Type Reference Index

### Core Types

| Type | Location | Description |
|------|----------|-------------|
| `DevboxView` | `types/devbox_view.py` | Devbox state snapshot |
| `DevboxCreateParams` | `types/devbox_create_params.py` | Devbox creation parameters |
| `BlueprintView` | `types/blueprint_view.py` | Blueprint state |
| `BlueprintCreateParams` | `types/blueprint_create_params.py` | Blueprint creation parameters |
| `DevboxSnapshotView` | `types/devbox_snapshot_view.py` | Snapshot state |
| `ObjectView` | `types/object_view.py` | Storage object state |
| `ScenarioView` | `types/scenario_view.py` | Scenario configuration |
| `BenchmarkView` | `types/benchmark_view.py` | Benchmark configuration |
| `AgentView` | `types/agent_view.py` | Agent configuration |
| `NetworkPolicyView` | `types/network_policy_view.py` | Network policy state |

### Execution Types

| Type | Location | Description |
|------|----------|-------------|
| `DevboxAsyncExecutionDetailView` | `types/devbox_async_execution_detail_view.py` | Async execution state |
| `DevboxExecutionDetailView` | `types/devbox_execution_detail_view.py` | Sync execution state |
| `ExecutionResult` | `sdk/execution_result.py` | Completed execution wrapper |
| `Execution` | `sdk/execution.py` | Running execution handle |

### Shared Parameter Types

| Type | Location | Description |
|------|----------|-------------|
| `LaunchParameters` | `types/shared_params/launch_parameters.py` | Resource/lifecycle config |
| `Mount` | `types/shared_params/mount.py` | Mount configuration union |
| `ObjectMount` | `types/shared_params/object_mount.py` | Object mount config |
| `CodeMountParameters` | `types/shared_params/code_mount_parameters.py` | Git repo mount config |
| `AgentSource` | `types/shared_params/agent_source.py` | Agent package source |

### SDK Request Option Types

| Type | Location | Description |
|------|----------|-------------|
| `BaseRequestOptions` | `sdk/_types.py` | Basic request options |
| `LongRequestOptions` | `sdk/_types.py` | Options with idempotency key |
| `PollingRequestOptions` | `sdk/_types.py` | Options with polling config |
| `ExecuteStreamingCallbacks` | `sdk/_types.py` | Stdout/stderr callbacks |

### Polling Types

| Type | Location | Description |
|------|----------|-------------|
| `PollingConfig` | `lib/polling.py` | Polling behavior configuration |
| `PollingTimeout` | `lib/polling.py` | Polling timeout exception |

---

## Additional Resources

- **Full type definitions:** `src/runloop_api_client/types/`
- **SDK source:** `src/runloop_api_client/sdk/`
- **REST resources:** `src/runloop_api_client/resources/`
- **Context loader utilities:** `src/runloop_api_client/lib/context_loader.py`
