# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types.functions import (
    FunctionInvocationListView,
    InvocationRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInvocations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        invocation = client.functions.invocations.retrieve(
            "invocationId",
        )
        assert_matches_type(InvocationRetrieveResponse, invocation, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.functions.invocations.with_raw_response.retrieve(
            "invocationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invocation = response.parse()
        assert_matches_type(InvocationRetrieveResponse, invocation, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.functions.invocations.with_streaming_response.retrieve(
            "invocationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invocation = response.parse()
            assert_matches_type(InvocationRetrieveResponse, invocation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `invocation_id` but received ''"):
            client.functions.invocations.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        invocation = client.functions.invocations.list()
        assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        invocation = client.functions.invocations.list(
            limit="limit",
            starting_after="starting_after",
        )
        assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.functions.invocations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invocation = response.parse()
        assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.functions.invocations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invocation = response.parse()
            assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_kill(self, client: Runloop) -> None:
        invocation = client.functions.invocations.kill(
            "invocationId",
        )
        assert_matches_type(object, invocation, path=["response"])

    @parametrize
    def test_raw_response_kill(self, client: Runloop) -> None:
        response = client.functions.invocations.with_raw_response.kill(
            "invocationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invocation = response.parse()
        assert_matches_type(object, invocation, path=["response"])

    @parametrize
    def test_streaming_response_kill(self, client: Runloop) -> None:
        with client.functions.invocations.with_streaming_response.kill(
            "invocationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invocation = response.parse()
            assert_matches_type(object, invocation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_kill(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `invocation_id` but received ''"):
            client.functions.invocations.with_raw_response.kill(
                "",
            )


class TestAsyncInvocations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        invocation = await async_client.functions.invocations.retrieve(
            "invocationId",
        )
        assert_matches_type(InvocationRetrieveResponse, invocation, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.invocations.with_raw_response.retrieve(
            "invocationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invocation = await response.parse()
        assert_matches_type(InvocationRetrieveResponse, invocation, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.invocations.with_streaming_response.retrieve(
            "invocationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invocation = await response.parse()
            assert_matches_type(InvocationRetrieveResponse, invocation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `invocation_id` but received ''"):
            await async_client.functions.invocations.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        invocation = await async_client.functions.invocations.list()
        assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        invocation = await async_client.functions.invocations.list(
            limit="limit",
            starting_after="starting_after",
        )
        assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.invocations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invocation = await response.parse()
        assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.invocations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invocation = await response.parse()
            assert_matches_type(FunctionInvocationListView, invocation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_kill(self, async_client: AsyncRunloop) -> None:
        invocation = await async_client.functions.invocations.kill(
            "invocationId",
        )
        assert_matches_type(object, invocation, path=["response"])

    @parametrize
    async def test_raw_response_kill(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.invocations.with_raw_response.kill(
            "invocationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        invocation = await response.parse()
        assert_matches_type(object, invocation, path=["response"])

    @parametrize
    async def test_streaming_response_kill(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.invocations.with_streaming_response.kill(
            "invocationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            invocation = await response.parse()
            assert_matches_type(object, invocation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_kill(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `invocation_id` but received ''"):
            await async_client.functions.invocations.with_raw_response.kill(
                "",
            )
