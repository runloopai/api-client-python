# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    ObjectView,
    ObjectDownloadURLView,
)
from runloop_api_client.pagination import SyncObjectsCursorIDPage, AsyncObjectsCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestObjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        object_ = client.objects.create(
            content_type="unspecified",
            name="name",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        object_ = client.objects.create(
            content_type="unspecified",
            name="name",
            metadata={"foo": "string"},
            ttl_ms=0,
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.create(
            content_type="unspecified",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.create(
            content_type="unspecified",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        object_ = client.objects.retrieve(
            "id",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.objects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        object_ = client.objects.list()
        assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        object_ = client.objects.list(
            content_type="unspecified",
            limit=0,
            name="name",
            search="search",
            starting_after="starting_after",
            state="UPLOADING",
        )
        assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        object_ = client.objects.delete(
            "id",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.objects.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_complete(self, client: Runloop) -> None:
        object_ = client.objects.complete(
            "id",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_raw_response_complete(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.complete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    def test_streaming_response_complete(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.complete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_complete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.objects.with_raw_response.complete(
                "",
            )

    @parametrize
    def test_method_download(self, client: Runloop) -> None:
        object_ = client.objects.download(
            id="id",
        )
        assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

    @parametrize
    def test_method_download_with_all_params(self, client: Runloop) -> None:
        object_ = client.objects.download(
            id="id",
            duration_seconds=0,
        )
        assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

    @parametrize
    def test_raw_response_download(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.download(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

    @parametrize
    def test_streaming_response_download(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.download(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_download(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.objects.with_raw_response.download(
                id="",
            )

    @parametrize
    def test_method_list_public(self, client: Runloop) -> None:
        object_ = client.objects.list_public()
        assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    def test_method_list_public_with_all_params(self, client: Runloop) -> None:
        object_ = client.objects.list_public(
            content_type="unspecified",
            limit=0,
            name="name",
            search="search",
            starting_after="starting_after",
            state="UPLOADING",
        )
        assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    def test_raw_response_list_public(self, client: Runloop) -> None:
        response = client.objects.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    def test_streaming_response_list_public(self, client: Runloop) -> None:
        with client.objects.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(SyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncObjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.create(
            content_type="unspecified",
            name="name",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.create(
            content_type="unspecified",
            name="name",
            metadata={"foo": "string"},
            ttl_ms=0,
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.create(
            content_type="unspecified",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.create(
            content_type="unspecified",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.retrieve(
            "id",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.objects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.list()
        assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.list(
            content_type="unspecified",
            limit=0,
            name="name",
            search="search",
            starting_after="starting_after",
            state="UPLOADING",
        )
        assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.delete(
            "id",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.objects.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_complete(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.complete(
            "id",
        )
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_raw_response_complete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.complete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectView, object_, path=["response"])

    @parametrize
    async def test_streaming_response_complete(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.complete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_complete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.objects.with_raw_response.complete(
                "",
            )

    @parametrize
    async def test_method_download(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.download(
            id="id",
        )
        assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

    @parametrize
    async def test_method_download_with_all_params(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.download(
            id="id",
            duration_seconds=0,
        )
        assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

    @parametrize
    async def test_raw_response_download(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.download(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

    @parametrize
    async def test_streaming_response_download(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.download(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectDownloadURLView, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_download(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.objects.with_raw_response.download(
                id="",
            )

    @parametrize
    async def test_method_list_public(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.list_public()
        assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    async def test_method_list_public_with_all_params(self, async_client: AsyncRunloop) -> None:
        object_ = await async_client.objects.list_public(
            content_type="unspecified",
            limit=0,
            name="name",
            search="search",
            starting_after="starting_after",
            state="UPLOADING",
        )
        assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    async def test_raw_response_list_public(self, async_client: AsyncRunloop) -> None:
        response = await async_client.objects.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

    @parametrize
    async def test_streaming_response_list_public(self, async_client: AsyncRunloop) -> None:
        async with async_client.objects.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(AsyncObjectsCursorIDPage[ObjectView], object_, path=["response"])

        assert cast(Any, response.is_closed) is True
