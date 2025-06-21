# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import DevboxSnapshotView
from runloop_api_client.pagination import SyncDiskSnapshotsCursorIDPage, AsyncDiskSnapshotsCursorIDPage
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
