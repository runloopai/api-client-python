"""Asynchronous SDK smoke tests for AsyncRunloopSDK initialization."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30


class TestAsyncRunloopSDKInitialization:
    """Test AsyncRunloopSDK client initialization and structure."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_sdk_instance_creation(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test that async SDK instance is created successfully with all client properties."""
        assert async_sdk_client is not None
        assert async_sdk_client.devbox is not None
        assert async_sdk_client.blueprint is not None
        assert async_sdk_client.snapshot is not None
        assert async_sdk_client.storage_object is not None

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_legacy_api_access(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test that legacy API client is accessible through sdk.api."""
        assert async_sdk_client.api is not None
        assert async_sdk_client.api.devboxes is not None
        assert async_sdk_client.api.blueprints is not None
        assert async_sdk_client.api.objects is not None
