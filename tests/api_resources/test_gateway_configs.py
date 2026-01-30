# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    GatewayConfigView,
)
from runloop_api_client.pagination import SyncGatewayConfigsCursorIDPage, AsyncGatewayConfigsCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGatewayConfigs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.create(
            auth_mechanism={"type": "type"},
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.create(
            auth_mechanism={
                "type": "type",
                "key": "key",
            },
            endpoint="endpoint",
            name="name",
            description="description",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.gateway_configs.with_raw_response.create(
            auth_mechanism={"type": "type"},
            endpoint="endpoint",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.gateway_configs.with_streaming_response.create(
            auth_mechanism={"type": "type"},
            endpoint="endpoint",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.retrieve(
            "id",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.gateway_configs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.gateway_configs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.gateway_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.update(
            id="id",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.update(
            id="id",
            auth_mechanism={
                "type": "type",
                "key": "key",
            },
            description="description",
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.gateway_configs.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.gateway_configs.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.gateway_configs.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.list()
        assert_matches_type(SyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.list(
            id="id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.gateway_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = response.parse()
        assert_matches_type(SyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.gateway_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = response.parse()
            assert_matches_type(SyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        gateway_config = client.gateway_configs.delete(
            "id",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.gateway_configs.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.gateway_configs.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.gateway_configs.with_raw_response.delete(
                "",
            )


class TestAsyncGatewayConfigs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.create(
            auth_mechanism={"type": "type"},
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.create(
            auth_mechanism={
                "type": "type",
                "key": "key",
            },
            endpoint="endpoint",
            name="name",
            description="description",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.gateway_configs.with_raw_response.create(
            auth_mechanism={"type": "type"},
            endpoint="endpoint",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = await response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.gateway_configs.with_streaming_response.create(
            auth_mechanism={"type": "type"},
            endpoint="endpoint",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = await response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.retrieve(
            "id",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.gateway_configs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = await response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.gateway_configs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = await response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.gateway_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.update(
            id="id",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.update(
            id="id",
            auth_mechanism={
                "type": "type",
                "key": "key",
            },
            description="description",
            endpoint="endpoint",
            name="name",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.gateway_configs.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = await response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.gateway_configs.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = await response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.gateway_configs.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.list()
        assert_matches_type(AsyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.list(
            id="id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.gateway_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = await response.parse()
        assert_matches_type(AsyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.gateway_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = await response.parse()
            assert_matches_type(AsyncGatewayConfigsCursorIDPage[GatewayConfigView], gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        gateway_config = await async_client.gateway_configs.delete(
            "id",
        )
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.gateway_configs.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        gateway_config = await response.parse()
        assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.gateway_configs.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            gateway_config = await response.parse()
            assert_matches_type(GatewayConfigView, gateway_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.gateway_configs.with_raw_response.delete(
                "",
            )
