"""Shared fixtures and utilities for SDK tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, AsyncMock

import httpx
import pytest

from runloop_api_client import Runloop, AsyncRunloop


def create_mock_httpx_client(methods: dict[str, Any] | None = None) -> AsyncMock:
    """
    Create a mock httpx.AsyncClient with proper context manager setup.

    Args:
        methods: Optional dict of method names to AsyncMock return values.
                 Common keys: 'get', 'put'

    Returns:
        Configured AsyncMock for httpx.AsyncClient
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
def devbox_view() -> SimpleNamespace:
    """Create a mock DevboxView."""
    return SimpleNamespace(
        id="dev_123",
        status="running",
        name="test-devbox",
    )


@pytest.fixture
def execution_view() -> SimpleNamespace:
    """Create a mock DevboxAsyncExecutionDetailView."""
    return SimpleNamespace(
        execution_id="exec_123",
        devbox_id="dev_123",
        status="completed",
        exit_status=0,
        stdout="output",
        stderr="",
    )


@pytest.fixture
def snapshot_view() -> SimpleNamespace:
    """Create a mock DevboxSnapshotView."""
    return SimpleNamespace(
        id="snap_123",
        status="completed",
        name="test-snapshot",
    )


@pytest.fixture
def blueprint_view() -> SimpleNamespace:
    """Create a mock BlueprintView."""
    return SimpleNamespace(
        id="bp_123",
        status="built",
        name="test-blueprint",
    )


@pytest.fixture
def object_view() -> SimpleNamespace:
    """Create a mock ObjectView."""
    return SimpleNamespace(
        id="obj_123",
        upload_url="https://upload.example.com/obj_123",
        name="test-object",
    )


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
    """Create a mock Stream for testing."""
    stream = Mock()
    stream.__iter__ = Mock(return_value=iter([]))
    stream.__enter__ = Mock(return_value=stream)
    stream.__exit__ = Mock(return_value=None)
    stream.close = Mock()
    return stream


@pytest.fixture
def mock_async_stream() -> AsyncMock:
    """Create a mock AsyncStream for testing."""

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
