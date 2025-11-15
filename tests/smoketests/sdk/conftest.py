"""Pytest fixtures for SDK end-to-end smoke tests."""

from __future__ import annotations

import os
from typing import Iterator, AsyncIterator

import pytest

from runloop_api_client.sdk import RunloopSDK, AsyncRunloopSDK


@pytest.fixture(scope="module")
def sdk_client() -> Iterator[RunloopSDK]:
    """Provide a synchronous RunloopSDK client for tests.

    Reads configuration from environment variables:
    - RUNLOOP_API_KEY: Required API key
    - RUNLOOP_BASE_URL: Optional API base URL
    """
    base_url = os.getenv("RUNLOOP_BASE_URL")
    bearer_token = os.getenv("RUNLOOP_API_KEY")

    if not bearer_token:
        pytest.skip("RUNLOOP_API_KEY environment variable not set")

    client = RunloopSDK(
        bearer_token=bearer_token,
        base_url=base_url,
    )

    try:
        yield client
    finally:
        try:
            client.close()
        except Exception:
            pass


@pytest.fixture(scope="module")
async def async_sdk_client() -> AsyncIterator[AsyncRunloopSDK]:
    """Provide an asynchronous AsyncRunloopSDK client for tests.

    Reads configuration from environment variables:
    - RUNLOOP_API_KEY: Required API key
    - RUNLOOP_BASE_URL: Optional API base URL
    """
    base_url = os.getenv("RUNLOOP_BASE_URL")
    bearer_token = os.getenv("RUNLOOP_API_KEY")

    if not bearer_token:
        pytest.skip("RUNLOOP_API_KEY environment variable not set")

    client = AsyncRunloopSDK(
        bearer_token=bearer_token,
        base_url=base_url,
    )

    try:
        async with client:
            yield client
    except Exception:
        # If context manager fails, try manual cleanup
        try:
            await client.aclose()
        except Exception:
            pass
