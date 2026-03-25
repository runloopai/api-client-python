"""Asynchronous SDK smoke tests for Axon operations."""

from __future__ import annotations

import json

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30


class TestAsyncAxonLifecycle:
    """Test basic async axon lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_axon_create(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating an axon."""
        axon = await async_sdk_client.axon.create()

        try:
            assert axon is not None
            assert axon.id is not None
            assert len(axon.id) > 0

            info = await axon.get_info()
            assert info.id == axon.id
            assert info.created_at_ms > 0
        finally:
            # TODO: Add axon cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_axon_from_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving axon by ID."""
        created = await async_sdk_client.axon.create()

        try:
            retrieved = async_sdk_client.axon.from_id(created.id)
            assert retrieved.id == created.id

            info = await retrieved.get_info()
            assert info.id == created.id
        finally:
            # TODO: Add axon cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_axon_publish(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test publishing events to an axon."""
        axon = await async_sdk_client.axon.create()

        try:
            result = await axon.publish(
                event_type="test_event",
                origin="USER_EVENT",
                payload=json.dumps({"message": "hello"}),
                source="sdk-smoke-test",
            )

            assert result is not None
            assert result.sequence >= 0
            assert result.timestamp_ms > 0
        finally:
            # TODO: Add axon cleanup once delete endpoint is implemented
            pass


class TestAsyncAxonListing:
    """Test axon listing operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_axons(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing axons."""
        axons = await async_sdk_client.axon.list()

        assert isinstance(axons, list)
        assert len(axons) >= 0
