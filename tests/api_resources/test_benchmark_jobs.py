# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    BenchmarkJobView,
    BenchmarkJobListView,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBenchmarkJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        benchmark_job = client.benchmark_jobs.create()
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        benchmark_job = client.benchmark_jobs.create(
            name="name",
            spec={
                "inline_yaml": "inline_yaml",
                "type": "harbor",
            },
        )
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.benchmark_jobs.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark_job = response.parse()
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.benchmark_jobs.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark_job = response.parse()
            assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        benchmark_job = client.benchmark_jobs.retrieve(
            "id",
        )
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.benchmark_jobs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark_job = response.parse()
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.benchmark_jobs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark_job = response.parse()
            assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.benchmark_jobs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        benchmark_job = client.benchmark_jobs.list()
        assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        benchmark_job = client.benchmark_jobs.list(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.benchmark_jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark_job = response.parse()
        assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.benchmark_jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark_job = response.parse()
            assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBenchmarkJobs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        benchmark_job = await async_client.benchmark_jobs.create()
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark_job = await async_client.benchmark_jobs.create(
            name="name",
            spec={
                "inline_yaml": "inline_yaml",
                "type": "harbor",
            },
        )
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmark_jobs.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark_job = await response.parse()
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmark_jobs.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark_job = await response.parse()
            assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        benchmark_job = await async_client.benchmark_jobs.retrieve(
            "id",
        )
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmark_jobs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark_job = await response.parse()
        assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmark_jobs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark_job = await response.parse()
            assert_matches_type(BenchmarkJobView, benchmark_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.benchmark_jobs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        benchmark_job = await async_client.benchmark_jobs.list()
        assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark_job = await async_client.benchmark_jobs.list(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmark_jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark_job = await response.parse()
        assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmark_jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark_job = await response.parse()
            assert_matches_type(BenchmarkJobListView, benchmark_job, path=["response"])

        assert cast(Any, response.is_closed) is True
