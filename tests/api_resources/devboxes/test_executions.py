# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import DevboxExecutionDetailView, DevboxAsyncExecutionDetailView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExecutions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        execution = client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
            last_n="last_n",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.executions.with_raw_response.retrieve(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.executions.with_raw_response.retrieve(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    def test_method_execute_async(self, client: Runloop) -> None:
        execution = client.devboxes.executions.execute_async(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_execute_async_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.execute_async(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_execute_async(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.execute_async(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_execute_async(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.execute_async(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute_async(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.executions.with_raw_response.execute_async(
                id="",
                command="command",
            )

    @parametrize
    def test_method_execute_sync(self, client: Runloop) -> None:
        execution = client.devboxes.executions.execute_sync(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_execute_sync_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.execute_sync(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_execute_sync(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.execute_sync(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_execute_sync(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.execute_sync(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute_sync(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.executions.with_raw_response.execute_sync(
                id="",
                command="command",
            )

    @parametrize
    def test_method_kill(self, client: Runloop) -> None:
        execution = client.devboxes.executions.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_kill(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_kill(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_kill(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.executions.with_raw_response.kill(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.executions.with_raw_response.kill(
                execution_id="",
                devbox_id="devbox_id",
            )


class TestAsyncExecutions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
            last_n="last_n",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.retrieve(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.retrieve(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    async def test_method_execute_async(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.execute_async(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_execute_async_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.execute_async(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_execute_async(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.execute_async(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_execute_async(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.execute_async(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute_async(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.execute_async(
                id="",
                command="command",
            )

    @parametrize
    async def test_method_execute_sync(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.execute_sync(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_execute_sync_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.execute_sync(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.execute_sync(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.execute_sync(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.execute_sync(
                id="",
                command="command",
            )

    @parametrize
    async def test_method_kill(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_kill(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_kill(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_kill(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.kill(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.kill(
                execution_id="",
                devbox_id="devbox_id",
            )
