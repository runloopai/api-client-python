# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    FunctionListView,
    FunctionInvokeSyncResponse,
    FunctionInvokeAsyncResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFunctions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        function = client.functions.list()
        assert_matches_type(FunctionListView, function, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.functions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(FunctionListView, function, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.functions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(FunctionListView, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_invoke_async(self, client: Runloop) -> None:
        function = client.functions.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
        )
        assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

    @parametrize
    def test_method_invoke_async_with_all_params(self, client: Runloop) -> None:
        function = client.functions.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
            runloop_meta={"session_id": "session_id"},
        )
        assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

    @parametrize
    def test_raw_response_invoke_async(self, client: Runloop) -> None:
        response = client.functions.with_raw_response.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

    @parametrize
    def test_streaming_response_invoke_async(self, client: Runloop) -> None:
        with client.functions.with_streaming_response.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_invoke_async(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_name` but received ''"):
            client.functions.with_raw_response.invoke_async(
                function_name="function_name",
                project_name="",
                request={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_name` but received ''"):
            client.functions.with_raw_response.invoke_async(
                function_name="",
                project_name="project_name",
                request={},
            )

    @parametrize
    def test_method_invoke_sync(self, client: Runloop) -> None:
        function = client.functions.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
        )
        assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

    @parametrize
    def test_method_invoke_sync_with_all_params(self, client: Runloop) -> None:
        function = client.functions.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
            runloop_meta={"session_id": "session_id"},
        )
        assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

    @parametrize
    def test_raw_response_invoke_sync(self, client: Runloop) -> None:
        response = client.functions.with_raw_response.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

    @parametrize
    def test_streaming_response_invoke_sync(self, client: Runloop) -> None:
        with client.functions.with_streaming_response.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_invoke_sync(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_name` but received ''"):
            client.functions.with_raw_response.invoke_sync(
                function_name="function_name",
                project_name="",
                request={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_name` but received ''"):
            client.functions.with_raw_response.invoke_sync(
                function_name="",
                project_name="project_name",
                request={},
            )


class TestAsyncFunctions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        function = await async_client.functions.list()
        assert_matches_type(FunctionListView, function, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(FunctionListView, function, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(FunctionListView, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_invoke_async(self, async_client: AsyncRunloop) -> None:
        function = await async_client.functions.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
        )
        assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

    @parametrize
    async def test_method_invoke_async_with_all_params(self, async_client: AsyncRunloop) -> None:
        function = await async_client.functions.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
            runloop_meta={"session_id": "session_id"},
        )
        assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

    @parametrize
    async def test_raw_response_invoke_async(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.with_raw_response.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

    @parametrize
    async def test_streaming_response_invoke_async(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.with_streaming_response.invoke_async(
            function_name="function_name",
            project_name="project_name",
            request={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(FunctionInvokeAsyncResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_invoke_async(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_name` but received ''"):
            await async_client.functions.with_raw_response.invoke_async(
                function_name="function_name",
                project_name="",
                request={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_name` but received ''"):
            await async_client.functions.with_raw_response.invoke_async(
                function_name="",
                project_name="project_name",
                request={},
            )

    @parametrize
    async def test_method_invoke_sync(self, async_client: AsyncRunloop) -> None:
        function = await async_client.functions.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
        )
        assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

    @parametrize
    async def test_method_invoke_sync_with_all_params(self, async_client: AsyncRunloop) -> None:
        function = await async_client.functions.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
            runloop_meta={"session_id": "session_id"},
        )
        assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

    @parametrize
    async def test_raw_response_invoke_sync(self, async_client: AsyncRunloop) -> None:
        response = await async_client.functions.with_raw_response.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

    @parametrize
    async def test_streaming_response_invoke_sync(self, async_client: AsyncRunloop) -> None:
        async with async_client.functions.with_streaming_response.invoke_sync(
            function_name="function_name",
            project_name="project_name",
            request={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(FunctionInvokeSyncResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_invoke_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_name` but received ''"):
            await async_client.functions.with_raw_response.invoke_sync(
                function_name="function_name",
                project_name="",
                request={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `function_name` but received ''"):
            await async_client.functions.with_raw_response.invoke_sync(
                function_name="",
                project_name="project_name",
                request={},
            )
