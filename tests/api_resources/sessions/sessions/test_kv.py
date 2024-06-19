# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from runloop import Runloop, AsyncRunloop
from tests.utils import assert_matches_type
from runloop.types.sessions.sessions import SessionKv

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKv:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        kv = client.sessions.sessions.kv.list(
            "string",
        )
        assert_matches_type(SessionKv, kv, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        kv = client.sessions.sessions.kv.list(
            "string",
            keys="string",
        )
        assert_matches_type(SessionKv, kv, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.sessions.sessions.kv.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kv = response.parse()
        assert_matches_type(SessionKv, kv, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.sessions.sessions.kv.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kv = response.parse()
            assert_matches_type(SessionKv, kv, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.sessions.kv.with_raw_response.list(
                "",
            )


class TestAsyncKv:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        kv = await async_client.sessions.sessions.kv.list(
            "string",
        )
        assert_matches_type(SessionKv, kv, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        kv = await async_client.sessions.sessions.kv.list(
            "string",
            keys="string",
        )
        assert_matches_type(SessionKv, kv, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.sessions.sessions.kv.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kv = await response.parse()
        assert_matches_type(SessionKv, kv, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.sessions.sessions.kv.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kv = await response.parse()
            assert_matches_type(SessionKv, kv, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.sessions.kv.with_raw_response.list(
                "",
            )
