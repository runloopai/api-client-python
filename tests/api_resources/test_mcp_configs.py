# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    McpConfigView,
)
from runloop_api_client.pagination import SyncMcpConfigsCursorIDPage, AsyncMcpConfigsCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMcpConfigs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
            description="description",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.mcp_configs.with_raw_response.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.mcp_configs.with_streaming_response.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.retrieve(
            "id",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.mcp_configs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.mcp_configs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.mcp_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.update(
            id="id",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.update(
            id="id",
            allowed_tools=["string"],
            description="description",
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.mcp_configs.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.mcp_configs.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.mcp_configs.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.list()
        assert_matches_type(SyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.list(
            id="id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.mcp_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = response.parse()
        assert_matches_type(SyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.mcp_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = response.parse()
            assert_matches_type(SyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        mcp_config = client.mcp_configs.delete(
            "id",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.mcp_configs.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.mcp_configs.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.mcp_configs.with_raw_response.delete(
                "",
            )


class TestAsyncMcpConfigs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
            description="description",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.mcp_configs.with_raw_response.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = await response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.mcp_configs.with_streaming_response.create(
            allowed_tools=["string"],
            endpoint="endpoint",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = await response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.retrieve(
            "id",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.mcp_configs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = await response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.mcp_configs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = await response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.mcp_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.update(
            id="id",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.update(
            id="id",
            allowed_tools=["string"],
            description="description",
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.mcp_configs.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = await response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.mcp_configs.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = await response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.mcp_configs.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.list()
        assert_matches_type(AsyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.list(
            id="id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.mcp_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = await response.parse()
        assert_matches_type(AsyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.mcp_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = await response.parse()
            assert_matches_type(AsyncMcpConfigsCursorIDPage[McpConfigView], mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        mcp_config = await async_client.mcp_configs.delete(
            "id",
        )
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.mcp_configs.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_config = await response.parse()
        assert_matches_type(McpConfigView, mcp_config, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.mcp_configs.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_config = await response.parse()
            assert_matches_type(McpConfigView, mcp_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.mcp_configs.with_raw_response.delete(
                "",
            )
