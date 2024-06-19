# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from runloop import Runloop, AsyncRunloop
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOpenAPI:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        openapi = client.functions.openapi.retrieve()
        assert_matches_type(object, openapi, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.functions.openapi.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        openapi = response.parse()
        assert_matches_type(object, openapi, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.functions.openapi.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            openapi = response.parse()
            assert_matches_type(object, openapi, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOpenAPI:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        openapi = await async_client.functions.openapi.retrieve()
        assert_matches_type(object, openapi, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.openapi.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        openapi = await response.parse()
        assert_matches_type(object, openapi, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.openapi.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            openapi = await response.parse()
            assert_matches_type(object, openapi, path=["response"])

        assert cast(Any, response.is_closed) is True
