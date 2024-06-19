# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from runloop import Runloop, AsyncRunloop
from tests.utils import assert_matches_type
from runloop.types import CodeHandle, CodeHandleList

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCodeHandles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        code_handle = client.code_handles.create()
        assert_matches_type(CodeHandle, code_handle, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        code_handle = client.code_handles.create(
            auth_token="string",
            branch="string",
            name="string",
            owner="string",
        )
        assert_matches_type(CodeHandle, code_handle, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.code_handles.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        code_handle = response.parse()
        assert_matches_type(CodeHandle, code_handle, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.code_handles.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            code_handle = response.parse()
            assert_matches_type(CodeHandle, code_handle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        code_handle = client.code_handles.list()
        assert_matches_type(CodeHandleList, code_handle, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        code_handle = client.code_handles.list(
            owner="string",
            repo_name="string",
        )
        assert_matches_type(CodeHandleList, code_handle, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.code_handles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        code_handle = response.parse()
        assert_matches_type(CodeHandleList, code_handle, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.code_handles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            code_handle = response.parse()
            assert_matches_type(CodeHandleList, code_handle, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCodeHandles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        code_handle = await async_client.code_handles.create()
        assert_matches_type(CodeHandle, code_handle, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        code_handle = await async_client.code_handles.create(
            auth_token="string",
            branch="string",
            name="string",
            owner="string",
        )
        assert_matches_type(CodeHandle, code_handle, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.code_handles.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        code_handle = await response.parse()
        assert_matches_type(CodeHandle, code_handle, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.code_handles.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            code_handle = await response.parse()
            assert_matches_type(CodeHandle, code_handle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        code_handle = await async_client.code_handles.list()
        assert_matches_type(CodeHandleList, code_handle, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        code_handle = await async_client.code_handles.list(
            owner="string",
            repo_name="string",
        )
        assert_matches_type(CodeHandleList, code_handle, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.code_handles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        code_handle = await response.parse()
        assert_matches_type(CodeHandleList, code_handle, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.code_handles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            code_handle = await response.parse()
            assert_matches_type(CodeHandleList, code_handle, path=["response"])

        assert cast(Any, response.is_closed) is True
