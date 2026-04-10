# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import RestrictedKeyCreatedView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRestrictedKeys:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        restricted_key = client.restricted_keys.create()
        assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        restricted_key = client.restricted_keys.create(
            expires_at_ms=0,
            name="name",
            scopes=[
                {
                    "access_level": "ACCESS_LEVEL_NONE",
                    "resource_type": "RESOURCE_TYPE_DEVBOXES",
                }
            ],
        )
        assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.restricted_keys.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        restricted_key = response.parse()
        assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.restricted_keys.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            restricted_key = response.parse()
            assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRestrictedKeys:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        restricted_key = await async_client.restricted_keys.create()
        assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        restricted_key = await async_client.restricted_keys.create(
            expires_at_ms=0,
            name="name",
            scopes=[
                {
                    "access_level": "ACCESS_LEVEL_NONE",
                    "resource_type": "RESOURCE_TYPE_DEVBOXES",
                }
            ],
        )
        assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.restricted_keys.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        restricted_key = await response.parse()
        assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.restricted_keys.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            restricted_key = await response.parse()
            assert_matches_type(RestrictedKeyCreatedView, restricted_key, path=["response"])

        assert cast(Any, response.is_closed) is True
