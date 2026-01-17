# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    NetworkPolicyView,
)
from runloop_api_client.pagination import SyncNetworkPoliciesCursorIDPage, AsyncNetworkPoliciesCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNetworkPolicies:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        network_policy = client.network_policies.create(
            name="name",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        network_policy = client.network_policies.create(
            name="name",
            allow_all=True,
            allow_devbox_to_devbox=True,
            allowed_hostnames=["string"],
            description="description",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.network_policies.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.network_policies.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        network_policy = client.network_policies.retrieve(
            "id",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.network_policies.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.network_policies.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.network_policies.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        network_policy = client.network_policies.update(
            id="id",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        network_policy = client.network_policies.update(
            id="id",
            allow_all=True,
            allow_devbox_to_devbox=True,
            allowed_hostnames=["string"],
            description="description",
            name="name",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.network_policies.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.network_policies.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.network_policies.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        network_policy = client.network_policies.list()
        assert_matches_type(SyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        network_policy = client.network_policies.list(
            id="id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.network_policies.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = response.parse()
        assert_matches_type(SyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.network_policies.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = response.parse()
            assert_matches_type(SyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        network_policy = client.network_policies.delete(
            "id",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.network_policies.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.network_policies.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.network_policies.with_raw_response.delete(
                "",
            )


class TestAsyncNetworkPolicies:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.create(
            name="name",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.create(
            name="name",
            allow_all=True,
            allow_devbox_to_devbox=True,
            allowed_hostnames=["string"],
            description="description",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.network_policies.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = await response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.network_policies.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = await response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.retrieve(
            "id",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.network_policies.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = await response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.network_policies.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = await response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.network_policies.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.update(
            id="id",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.update(
            id="id",
            allow_all=True,
            allow_devbox_to_devbox=True,
            allowed_hostnames=["string"],
            description="description",
            name="name",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.network_policies.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = await response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.network_policies.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = await response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.network_policies.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.list()
        assert_matches_type(AsyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.list(
            id="id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.network_policies.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = await response.parse()
        assert_matches_type(AsyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.network_policies.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = await response.parse()
            assert_matches_type(AsyncNetworkPoliciesCursorIDPage[NetworkPolicyView], network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        network_policy = await async_client.network_policies.delete(
            "id",
        )
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.network_policies.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        network_policy = await response.parse()
        assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.network_policies.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            network_policy = await response.parse()
            assert_matches_type(NetworkPolicyView, network_policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.network_policies.with_raw_response.delete(
                "",
            )
