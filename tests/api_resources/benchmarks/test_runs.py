# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import BenchmarkRunView, BenchmarkRunListView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        run = client.benchmarks.runs.retrieve(
            "id",
        )
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.benchmarks.runs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.benchmarks.runs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(BenchmarkRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.benchmarks.runs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        run = client.benchmarks.runs.list()
        assert_matches_type(BenchmarkRunListView, run, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        run = client.benchmarks.runs.list(
            benchmark_id="benchmark_id",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(BenchmarkRunListView, run, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.benchmarks.runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(BenchmarkRunListView, run, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.benchmarks.runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(BenchmarkRunListView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_complete(self, client: Runloop) -> None:
        run = client.benchmarks.runs.complete(
            "id",
        )
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    def test_raw_response_complete(self, client: Runloop) -> None:
        response = client.benchmarks.runs.with_raw_response.complete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    def test_streaming_response_complete(self, client: Runloop) -> None:
        with client.benchmarks.runs.with_streaming_response.complete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(BenchmarkRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_complete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.benchmarks.runs.with_raw_response.complete(
                "",
            )


class TestAsyncRuns:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        run = await async_client.benchmarks.runs.retrieve(
            "id",
        )
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.runs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.runs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(BenchmarkRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.benchmarks.runs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        run = await async_client.benchmarks.runs.list()
        assert_matches_type(BenchmarkRunListView, run, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        run = await async_client.benchmarks.runs.list(
            benchmark_id="benchmark_id",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(BenchmarkRunListView, run, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(BenchmarkRunListView, run, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(BenchmarkRunListView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_complete(self, async_client: AsyncRunloop) -> None:
        run = await async_client.benchmarks.runs.complete(
            "id",
        )
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    async def test_raw_response_complete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.runs.with_raw_response.complete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(BenchmarkRunView, run, path=["response"])

    @parametrize
    async def test_streaming_response_complete(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.runs.with_streaming_response.complete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(BenchmarkRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_complete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.benchmarks.runs.with_raw_response.complete(
                "",
            )
