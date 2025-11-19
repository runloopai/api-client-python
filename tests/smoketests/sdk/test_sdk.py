"""Synchronous SDK smoke tests for RunloopSDK initialization."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30


class TestRunloopSDKInitialization:
    """Test RunloopSDK client initialization and structure."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_sdk_instance_creation(self, sdk_client: RunloopSDK) -> None:
        """Test that SDK instance is created successfully with all client properties."""
        assert sdk_client is not None
        assert sdk_client.devbox is not None
        assert sdk_client.blueprint is not None
        assert sdk_client.snapshot is not None
        assert sdk_client.storage_object is not None

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_legacy_api_access(self, sdk_client: RunloopSDK) -> None:
        """Test that legacy API client is accessible through sdk.api."""
        assert sdk_client.api is not None
        assert sdk_client.api.devboxes is not None
        assert sdk_client.api.blueprints is not None
        assert sdk_client.api.objects is not None
