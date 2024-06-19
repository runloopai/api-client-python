# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from runloop import Runloop, AsyncRunloop
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLatches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_fulfill(self, client: Runloop) -> None:
        latch = client.latches.fulfill(
            "string",
            result={},
        )
        assert_matches_type(object, latch, path=["response"])

    @parametrize
    def test_raw_response_fulfill(self, client: Runloop) -> None:
        response = client.latches.with_raw_response.fulfill(
            "string",
            result={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        latch = response.parse()
        assert_matches_type(object, latch, path=["response"])

    @parametrize
    def test_streaming_response_fulfill(self, client: Runloop) -> None:
        with client.latches.with_streaming_response.fulfill(
            "string",
            result={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            latch = response.parse()
            assert_matches_type(object, latch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_fulfill(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `latch_id` but received ''"):
            client.latches.with_raw_response.fulfill(
                "",
                result={},
            )


class TestAsyncLatches:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_fulfill(self, async_client: AsyncRunloop) -> None:
        latch = await async_client.latches.fulfill(
            "string",
            result={},
        )
        assert_matches_type(object, latch, path=["response"])

    @parametrize
    async def test_raw_response_fulfill(self, async_client: AsyncRunloop) -> None:
        response = await async_client.latches.with_raw_response.fulfill(
            "string",
            result={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        latch = await response.parse()
        assert_matches_type(object, latch, path=["response"])

    @parametrize
    async def test_streaming_response_fulfill(self, async_client: AsyncRunloop) -> None:
        async with async_client.latches.with_streaming_response.fulfill(
            "string",
            result={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            latch = await response.parse()
            assert_matches_type(object, latch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_fulfill(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `latch_id` but received ''"):
            await async_client.latches.with_raw_response.fulfill(
                "",
                result={},
            )
