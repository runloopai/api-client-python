# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast
from unittest.mock import patch

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import DevboxSnapshotView
from runloop_api_client.pagination import SyncDiskSnapshotsCursorIDPage, AsyncDiskSnapshotsCursorIDPage
from runloop_api_client._exceptions import RunloopError
from runloop_api_client.lib.polling import PollingConfig, PollingTimeout
from runloop_api_client.types.devboxes import (
    DevboxSnapshotAsyncStatusView,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDiskSnapshots:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        disk_snapshot = client.devboxes.disk_snapshots.update(
            id="id",
        )
        assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        disk_snapshot = client.devboxes.disk_snapshots.update(
            id="id",
            commit_message="commit_message",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.devboxes.disk_snapshots.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = response.parse()
        assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.devboxes.disk_snapshots.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = response.parse()
            assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.disk_snapshots.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        disk_snapshot = client.devboxes.disk_snapshots.list()
        assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        disk_snapshot = client.devboxes.disk_snapshots.list(
            devbox_id="devbox_id",
            limit=0,
            metadata_key="metadata[key]",
            metadata_key_in="metadata[key][in]",
            source_blueprint_id="source_blueprint_id",
            starting_after="starting_after",
        )
        assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.devboxes.disk_snapshots.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = response.parse()
        assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.devboxes.disk_snapshots.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = response.parse()
            assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        disk_snapshot = client.devboxes.disk_snapshots.delete(
            "id",
        )
        assert_matches_type(object, disk_snapshot, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.devboxes.disk_snapshots.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = response.parse()
        assert_matches_type(object, disk_snapshot, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.devboxes.disk_snapshots.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = response.parse()
            assert_matches_type(object, disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.disk_snapshots.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_query_status(self, client: Runloop) -> None:
        disk_snapshot = client.devboxes.disk_snapshots.query_status(
            "id",
        )
        assert_matches_type(DevboxSnapshotAsyncStatusView, disk_snapshot, path=["response"])

    @parametrize
    def test_raw_response_query_status(self, client: Runloop) -> None:
        response = client.devboxes.disk_snapshots.with_raw_response.query_status(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = response.parse()
        assert_matches_type(DevboxSnapshotAsyncStatusView, disk_snapshot, path=["response"])

    @parametrize
    def test_streaming_response_query_status(self, client: Runloop) -> None:
        with client.devboxes.disk_snapshots.with_streaming_response.query_status(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = response.parse()
            assert_matches_type(DevboxSnapshotAsyncStatusView, disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query_status(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.disk_snapshots.with_raw_response.query_status(
                "",
            )

    # Polling method tests
    @parametrize
    def test_method_await_completed_success(self, client: Runloop) -> None:
        """Test await_completed with successful polling to complete state"""

        # Mock the query_status calls - first returns in_progress, then complete
        mock_status_in_progress = DevboxSnapshotAsyncStatusView(
            status="in_progress",
            error_message=None,
        )

        mock_status_complete = DevboxSnapshotAsyncStatusView(
            status="complete",
            error_message=None,
        )

        with patch.object(client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.side_effect = [mock_status_in_progress, mock_status_complete]

            result = client.devboxes.disk_snapshots.await_completed("test_id")

            assert result.status == "complete"
            assert mock_query.call_count == 2

    @parametrize
    def test_method_await_completed_immediate_success(self, client: Runloop) -> None:
        """Test await_completed when snapshot is already complete"""

        mock_status_complete = DevboxSnapshotAsyncStatusView(
            status="complete",
            error_message=None,
        )

        with patch.object(client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_complete

            result = client.devboxes.disk_snapshots.await_completed("test_id")

            assert result.status == "complete"
            assert mock_query.call_count == 1

    @parametrize
    def test_method_await_completed_error_state(self, client: Runloop) -> None:
        """Test await_completed when snapshot status becomes error"""

        mock_status_error = DevboxSnapshotAsyncStatusView(
            status="error",
            error_message="Snapshot creation failed",
        )

        with patch.object(client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_error

            with pytest.raises(RunloopError, match="Snapshot test_id failed: Snapshot creation failed"):
                client.devboxes.disk_snapshots.await_completed("test_id")

    @parametrize
    def test_method_await_completed_error_state_no_message(self, client: Runloop) -> None:
        """Test await_completed when snapshot status becomes error without error message"""

        mock_status_error = DevboxSnapshotAsyncStatusView(
            status="error",
            error_message=None,
        )

        with patch.object(client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_error

            with pytest.raises(RunloopError, match="Snapshot test_id failed: Unknown error"):
                client.devboxes.disk_snapshots.await_completed("test_id")

    @parametrize
    def test_method_await_completed_with_config(self, client: Runloop) -> None:
        """Test await_completed with custom polling configuration"""

        mock_status_complete = DevboxSnapshotAsyncStatusView(
            status="complete",
            error_message=None,
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_complete

            result = client.devboxes.disk_snapshots.await_completed("test_id", polling_config=config)

            assert result.status == "complete"

    @parametrize
    def test_method_await_completed_polling_timeout(self, client: Runloop) -> None:
        """Test await_completed raises PollingTimeout when max attempts exceeded"""

        mock_status_in_progress = DevboxSnapshotAsyncStatusView(
            status="in_progress",
            error_message=None,
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_in_progress

            with pytest.raises(PollingTimeout):
                client.devboxes.disk_snapshots.await_completed("test_id", polling_config=config)


class TestAsyncDiskSnapshots:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        disk_snapshot = await async_client.devboxes.disk_snapshots.update(
            id="id",
        )
        assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        disk_snapshot = await async_client.devboxes.disk_snapshots.update(
            id="id",
            commit_message="commit_message",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.disk_snapshots.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = await response.parse()
        assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.disk_snapshots.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = await response.parse()
            assert_matches_type(DevboxSnapshotView, disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.disk_snapshots.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        disk_snapshot = await async_client.devboxes.disk_snapshots.list()
        assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        disk_snapshot = await async_client.devboxes.disk_snapshots.list(
            devbox_id="devbox_id",
            limit=0,
            metadata_key="metadata[key]",
            metadata_key_in="metadata[key][in]",
            source_blueprint_id="source_blueprint_id",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.disk_snapshots.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = await response.parse()
        assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.disk_snapshots.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = await response.parse()
            assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        disk_snapshot = await async_client.devboxes.disk_snapshots.delete(
            "id",
        )
        assert_matches_type(object, disk_snapshot, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.disk_snapshots.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = await response.parse()
        assert_matches_type(object, disk_snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.disk_snapshots.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = await response.parse()
            assert_matches_type(object, disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.disk_snapshots.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_query_status(self, async_client: AsyncRunloop) -> None:
        disk_snapshot = await async_client.devboxes.disk_snapshots.query_status(
            "id",
        )
        assert_matches_type(DevboxSnapshotAsyncStatusView, disk_snapshot, path=["response"])

    @parametrize
    async def test_raw_response_query_status(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.disk_snapshots.with_raw_response.query_status(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        disk_snapshot = await response.parse()
        assert_matches_type(DevboxSnapshotAsyncStatusView, disk_snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_query_status(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.disk_snapshots.with_streaming_response.query_status(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            disk_snapshot = await response.parse()
            assert_matches_type(DevboxSnapshotAsyncStatusView, disk_snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query_status(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.disk_snapshots.with_raw_response.query_status(
                "",
            )

    # Polling method tests
    @parametrize
    async def test_method_await_completed_success(self, async_client: AsyncRunloop) -> None:
        """Test await_completed with successful polling to complete state"""

        # Mock the query_status calls - first returns in_progress, then complete
        mock_status_in_progress = DevboxSnapshotAsyncStatusView(
            status="in_progress",
            error_message=None,
        )

        mock_status_complete = DevboxSnapshotAsyncStatusView(
            status="complete",
            error_message=None,
        )

        with patch.object(async_client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.side_effect = [mock_status_in_progress, mock_status_complete]

            result = await async_client.devboxes.disk_snapshots.await_completed("test_id")

            assert result.status == "complete"
            assert mock_query.call_count == 2

    @parametrize
    async def test_method_await_completed_immediate_success(self, async_client: AsyncRunloop) -> None:
        """Test await_completed when snapshot is already complete"""

        mock_status_complete = DevboxSnapshotAsyncStatusView(
            status="complete",
            error_message=None,
        )

        with patch.object(async_client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_complete

            result = await async_client.devboxes.disk_snapshots.await_completed("test_id")

            assert result.status == "complete"
            assert mock_query.call_count == 1

    @parametrize
    async def test_method_await_completed_error_state(self, async_client: AsyncRunloop) -> None:
        """Test await_completed when snapshot status becomes error"""

        mock_status_error = DevboxSnapshotAsyncStatusView(
            status="error",
            error_message="Snapshot creation failed",
        )

        with patch.object(async_client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_error

            with pytest.raises(RunloopError, match="Snapshot test_id failed: Snapshot creation failed"):
                await async_client.devboxes.disk_snapshots.await_completed("test_id")

    @parametrize
    async def test_method_await_completed_error_state_no_message(self, async_client: AsyncRunloop) -> None:
        """Test await_completed when snapshot status becomes error without error message"""

        mock_status_error = DevboxSnapshotAsyncStatusView(
            status="error",
            error_message=None,
        )

        with patch.object(async_client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_error

            with pytest.raises(RunloopError, match="Snapshot test_id failed: Unknown error"):
                await async_client.devboxes.disk_snapshots.await_completed("test_id")

    @parametrize
    async def test_method_await_completed_with_config(self, async_client: AsyncRunloop) -> None:
        """Test await_completed with custom polling configuration"""

        mock_status_complete = DevboxSnapshotAsyncStatusView(
            status="complete",
            error_message=None,
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(async_client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_complete

            result = await async_client.devboxes.disk_snapshots.await_completed("test_id", polling_config=config)

            assert result.status == "complete"

    @parametrize
    async def test_method_await_completed_polling_timeout(self, async_client: AsyncRunloop) -> None:
        """Test await_completed raises PollingTimeout when max attempts exceeded"""

        mock_status_in_progress = DevboxSnapshotAsyncStatusView(
            status="in_progress",
            error_message=None,
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(async_client.devboxes.disk_snapshots, "query_status") as mock_query:
            mock_query.return_value = mock_status_in_progress

            with pytest.raises(PollingTimeout):
                await async_client.devboxes.disk_snapshots.await_completed("test_id", polling_config=config)
