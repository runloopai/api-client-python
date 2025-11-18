"""Shared fixtures and utilities for SDK tests."""

from __future__ import annotations

import asyncio
import threading
from typing import Any
from dataclasses import dataclass
from unittest.mock import Mock, AsyncMock

import httpx
import pytest

from runloop_api_client import Runloop, AsyncRunloop

# Test ID constants
TEST_IDS = {
    "devbox": "dev_123",
    "execution": "exec_123",
    "snapshot": "snap_123",
    "blueprint": "bp_123",
    "object": "obj_123",
}

# Test URL constants
TEST_URLS = {
    "upload": "https://upload.example.com/obj_123",
    "download": "https://download.example.com/obj_123",
}

# Timing constants for thread/task synchronization tests
THREAD_STARTUP_DELAY = 0.1  # Time to allow threads/tasks to start
TASK_COMPLETION_SHORT = 0.02  # Brief async operation
TASK_COMPLETION_LONG = 1.0  # Long-running operation for cancellation tests
NUM_CONCURRENT_THREADS = 5  # Number of threads for concurrency tests


# Mock data structures using dataclasses for type safety
@dataclass
class MockDevboxView:
    """Mock DevboxView for testing."""

    id: str = "dev_123"
    status: str = "running"
    name: str = "test-devbox"


@dataclass
class MockExecutionView:
    """Mock DevboxAsyncExecutionDetailView for testing."""

    execution_id: str = "exec_123"
    devbox_id: str = "dev_123"
    status: str = "completed"
    exit_status: int = 0
    stdout: str = "output"
    stderr: str = ""
    stdout_truncated: bool = False
    stderr_truncated: bool = False


@dataclass
class MockSnapshotView:
    """Mock DevboxSnapshotView for testing."""

    id: str = "snap_123"
    status: str = "completed"
    name: str = "test-snapshot"


@dataclass
class MockBlueprintView:
    """Mock BlueprintView for testing."""

    id: str = "bp_123"
    status: str = "built"
    name: str = "test-blueprint"


@dataclass
class MockObjectView:
    """Mock ObjectView for testing."""

    id: str = "obj_123"
    upload_url: str = "https://upload.example.com/obj_123"
    name: str = "test-object"


def create_mock_httpx_client(methods: dict[str, Any] | None = None) -> AsyncMock:
    """
    Create a mock httpx.AsyncClient with proper context manager setup.

    Args:
        methods: Optional dict of method names to AsyncMock return values.
                 Common keys: 'get', 'put'

    Returns:
        Configured AsyncMock for httpx.AsyncClient

    Note: We don't use spec here because we need to manually set context manager
          methods which are not allowed with spec.
    """
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    if methods:
        for method_name, return_value in methods.items():
            setattr(mock_client, method_name, AsyncMock(return_value=return_value))

    return mock_client


def create_mock_httpx_response(**attrs: Any) -> Mock:
    """
    Create a mock httpx.Response with specified attributes.

    Args:
        **attrs: Attributes to set on the mock response.
                 Common: content, text, encoding

    Returns:
        Mock configured with httpx.Response spec and attributes
    """
    mock_response = Mock(spec=httpx.Response)
    for key, value in attrs.items():
        setattr(mock_response, key, value)
    return mock_response


@pytest.fixture
def mock_client() -> Mock:
    """Create a mock Runloop client."""
    return Mock(spec=Runloop)


@pytest.fixture
def mock_async_client() -> AsyncMock:
    """Create a mock AsyncRunloop client."""
    return AsyncMock(spec=AsyncRunloop)


@pytest.fixture
def devbox_view() -> MockDevboxView:
    """Create a mock DevboxView."""
    return MockDevboxView()


@pytest.fixture
def execution_view() -> MockExecutionView:
    """Create a mock DevboxAsyncExecutionDetailView."""
    return MockExecutionView()


@pytest.fixture
def snapshot_view() -> MockSnapshotView:
    """Create a mock DevboxSnapshotView."""
    return MockSnapshotView()


@pytest.fixture
def blueprint_view() -> MockBlueprintView:
    """Create a mock BlueprintView."""
    return MockBlueprintView()


@pytest.fixture
def object_view() -> MockObjectView:
    """Create a mock ObjectView."""
    return MockObjectView()


@pytest.fixture
def mock_httpx_response() -> Mock:
    """Create a mock httpx.Response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.content = b"test content"
    response.text = "test content"
    response.encoding = "utf-8"
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def mock_stream() -> Mock:
    """Create a mock Stream for testing.

    Note: We don't use spec here because we need to manually set context manager
          and iterator methods which are not allowed with spec.
    """
    stream = Mock()
    stream.__iter__ = Mock(return_value=iter([]))
    stream.__enter__ = Mock(return_value=stream)
    stream.__exit__ = Mock(return_value=None)
    stream.close = Mock()
    return stream


@pytest.fixture
def mock_async_stream() -> AsyncMock:
    """Create a mock AsyncStream for testing.

    Note: We don't use spec here because we need to manually set context manager
          and async iterator methods which are not allowed with spec.
    """

    async def async_iter():
        # Empty async iterator
        if False:
            yield

    stream = AsyncMock()
    stream.__aiter__ = Mock(return_value=async_iter())
    stream.__aenter__ = AsyncMock(return_value=stream)
    stream.__aexit__ = AsyncMock(return_value=None)
    stream.close = AsyncMock()
    return stream


@pytest.fixture
async def async_task_cleanup():
    """
    Fixture to ensure async tasks are properly cleaned up after tests.

    Usage:
        async def test_something(async_task_cleanup):
            task = asyncio.create_task(some_coroutine())
            async_task_cleanup.append(task)
            # Task will be automatically cancelled and awaited on teardown

    Yields:
        List to append tasks to for automatic cleanup
    """
    tasks: list[asyncio.Task[Any]] = []
    yield tasks
    # Cleanup: cancel all tasks and wait for them to finish
    for task in tasks:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


@pytest.fixture
def thread_cleanup():
    """
    Fixture to ensure threads are properly cleaned up after tests.

    Usage:
        def test_something(thread_cleanup):
            threads, stop_events = thread_cleanup
            stop_event = threading.Event()
            thread = threading.Thread(target=worker, args=(stop_event,))
            thread.start()
            threads.append(thread)
            stop_events.append(stop_event)
            # Thread will be automatically stopped and joined on teardown

    Yields:
        Tuple of (threads list, stop_events list) for automatic cleanup
    """
    threads: list[threading.Thread] = []
    stop_events: list[threading.Event] = []
    yield threads, stop_events
    # Cleanup: signal all threads to stop and wait for them
    for event in stop_events:
        event.set()
    for thread in threads:
        thread.join(timeout=2.0)
