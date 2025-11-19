# SDK End-to-End Smoke Tests

Comprehensive end-to-end tests for the object-oriented Python SDK (`runloop_api_client.sdk`). These tests run against the real Runloop API to validate critical workflows including devboxes, blueprints, snapshots, and storage objects.

## Overview

The Python SDK provides both synchronous and asynchronous interfaces:
- **Synchronous SDK**: `RunloopSDK` with `Devbox`, `Blueprint`, `Snapshot`, `StorageObject`
- **Asynchronous SDK**: `AsyncRunloopSDK` with `AsyncDevbox`, `AsyncBlueprint`, `AsyncSnapshot`, `AsyncStorageObject`

These tests ensure both interfaces work correctly in real-world scenarios.

## Test Files

### Infrastructure
- `conftest.py` - Pytest fixtures for SDK client instances

### Devbox Tests
- `test_devbox.py` - Synchronous devbox operations
- `test_async_devbox.py` - Asynchronous devbox operations

**Test Coverage:**
- Devbox lifecycle (create, get_info, shutdown)
- Command execution (exec, exec_async) with streaming callbacks
- File operations (read, write, upload, download)
- State management (suspend, resume, await_running, await_suspended, keep_alive)
- Networking (SSH keys, tunnels)
- Creation from blueprints and snapshots
- Snapshot creation
- Context manager support

### Blueprint Tests
- `test_blueprint.py` - Synchronous blueprint operations
- `test_async_blueprint.py` - Asynchronous blueprint operations

**Test Coverage:**
- Blueprint creation with dockerfiles and system setup commands
- Blueprint listing and retrieval
- Creating devboxes from blueprints
- Blueprint deletion

### Snapshot Tests
- `test_snapshot.py` - Synchronous snapshot operations
- `test_async_snapshot.py` - Asynchronous snapshot operations

**Test Coverage:**
- Snapshot creation from devboxes
- Snapshot info and status tracking
- Waiting for snapshot completion
- Creating devboxes from snapshots
- Snapshot listing and deletion

### Storage Object Tests
- `test_storage_object.py` - Synchronous storage object operations
- `test_async_storage_object.py` - Asynchronous storage object operations

**Test Coverage:**
- Storage object lifecycle (create, upload, complete, delete)
- Static upload methods (upload_from_text, upload_from_bytes, upload_from_file)
- Download methods (download_as_text, download_as_bytes, get_download_url)
- Storage object listing and retrieval
- Mounting storage objects to devboxes

## Running the Tests

### Prerequisites

Set required environment variables:
```bash
export RUNLOOP_API_KEY=your_api_key_here
# Optional: override the API base URL
# export RUNLOOP_BASE_URL=https://api.runloop.ai
```

### Run All SDK Smoke Tests
```bash
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest tests/smoketests/sdk/
```

### Run Specific Test File
```bash
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest tests/smoketests/sdk/test_devbox.py
```

### Run Specific Test
```bash
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest -k "test_devbox_lifecycle" tests/smoketests/sdk/
```

### Run Only Sync or Async Tests
```bash
# Sync tests only (files without 'async' prefix)
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest tests/smoketests/sdk/test_devbox.py tests/smoketests/sdk/test_blueprint.py tests/smoketests/sdk/test_snapshot.py tests/smoketests/sdk/test_storage_object.py

# Async tests only (files with 'async' prefix)
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest tests/smoketests/sdk/test_async_*.py
```

## Test Patterns

### Resource Management
All tests include proper cleanup using try/finally blocks or pytest fixtures to ensure resources (devboxes, blueprints, etc.) are deleted after testing, even if tests fail.

### Timeouts
Tests use appropriate timeouts based on operation types:
- **30 seconds**: Quick operations (create, retrieve, delete)
- **2+ minutes**: Long-running operations (devbox creation, blueprint builds)

### Sequential Tests
Some tests within a file may be dependent on each other to save time and resources. Tests are designed to be run sequentially within each file.

### Naming Convention
Tests use the `unique_name()` utility to generate unique resource names with timestamps, preventing conflicts between test runs.

## Differences from TypeScript SDK

The Python SDK includes both synchronous and asynchronous implementations, whereas the TypeScript SDK is async-only. This necessitates separate test files for each variant to ensure both work correctly.

Key differences:
- Python uses `async`/`await` syntax for async operations
- Python has separate classes: `Devbox` vs `AsyncDevbox`, etc.
- Python uses context managers (`with` statement) for resource cleanup
- Python async tests require `pytest.mark.asyncio` decorator

## CI Integration

These tests can be integrated into CI workflows similar to other smoketests. Set the `RUNLOOP_API_KEY` secret in your CI environment and run with the `RUN_SMOKETESTS=1` environment variable.

Example GitHub Actions workflow step:
```yaml
- name: Run SDK Smoke Tests
  env:
    RUNLOOP_API_KEY: ${{ secrets.RUNLOOP_SMOKETEST_API_KEY }}
    RUN_SMOKETESTS: 1
  run: |
    uv run pytest -q -vv -m smoketest tests/smoketests/sdk/
```

