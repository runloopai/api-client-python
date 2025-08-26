# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    BenchmarkView,
    BenchmarkRunView,
    ScenarioDefinitionListView,
)
from runloop_api_client.pagination import SyncBenchmarksCursorIDPage, AsyncBenchmarksCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBenchmarks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        benchmark = client.benchmarks.create(
            name="name",
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        benchmark = client.benchmarks.create(
            name="name",
            attribution="attribution",
            description="description",
            metadata={"foo": "string"},
            required_environment_variables=["string"],
            required_secret_names=["string"],
            scenario_ids=["string"],
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(BenchmarkView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        benchmark = client.benchmarks.retrieve(
            "id",
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(BenchmarkView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.benchmarks.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        benchmark = client.benchmarks.update(
            id="id",
            name="name",
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        benchmark = client.benchmarks.update(
            id="id",
            name="name",
            attribution="attribution",
            description="description",
            metadata={"foo": "string"},
            required_environment_variables=["string"],
            required_secret_names=["string"],
            scenario_ids=["string"],
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.update(
            id="id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.update(
            id="id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(BenchmarkView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.benchmarks.with_raw_response.update(
                id="",
                name="name",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        benchmark = client.benchmarks.list()
        assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        benchmark = client.benchmarks.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_definitions(self, client: Runloop) -> None:
        benchmark = client.benchmarks.definitions(
            id="id",
        )
        assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

    @parametrize
    def test_method_definitions_with_all_params(self, client: Runloop) -> None:
        benchmark = client.benchmarks.definitions(
            id="id",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

    @parametrize
    def test_raw_response_definitions(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.definitions(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

    @parametrize
    def test_streaming_response_definitions(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.definitions(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_definitions(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.benchmarks.with_raw_response.definitions(
                id="",
            )

    @parametrize
    def test_method_list_public(self, client: Runloop) -> None:
        benchmark = client.benchmarks.list_public()
        assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    def test_method_list_public_with_all_params(self, client: Runloop) -> None:
        benchmark = client.benchmarks.list_public(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    def test_raw_response_list_public(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    def test_streaming_response_list_public(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(SyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_start_run(self, client: Runloop) -> None:
        benchmark = client.benchmarks.start_run(
            benchmark_id="benchmark_id",
        )
        assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

    @parametrize
    def test_method_start_run_with_all_params(self, client: Runloop) -> None:
        benchmark = client.benchmarks.start_run(
            benchmark_id="benchmark_id",
            metadata={"foo": "string"},
            run_name="run_name",
            run_profile={
                "env_vars": {"foo": "string"},
                "launch_parameters": {
                    "after_idle": {
                        "idle_time_seconds": 0,
                        "on_idle": "shutdown",
                    },
                    "architecture": "x86_64",
                    "available_ports": [0],
                    "custom_cpu_cores": 0,
                    "custom_disk_size": 0,
                    "custom_gb_memory": 0,
                    "keep_alive_time_seconds": 0,
                    "launch_commands": ["string"],
                    "required_services": ["string"],
                    "resource_size_request": "X_SMALL",
                    "user_parameters": {
                        "uid": 0,
                        "username": "username",
                    },
                },
                "purpose": "purpose",
                "secrets": {"foo": "string"},
            },
        )
        assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

    @parametrize
    def test_raw_response_start_run(self, client: Runloop) -> None:
        response = client.benchmarks.with_raw_response.start_run(
            benchmark_id="benchmark_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = response.parse()
        assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

    @parametrize
    def test_streaming_response_start_run(self, client: Runloop) -> None:
        with client.benchmarks.with_streaming_response.start_run(
            benchmark_id="benchmark_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = response.parse()
            assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBenchmarks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.create(
            name="name",
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.create(
            name="name",
            attribution="attribution",
            description="description",
            metadata={"foo": "string"},
            required_environment_variables=["string"],
            required_secret_names=["string"],
            scenario_ids=["string"],
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(BenchmarkView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.retrieve(
            "id",
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(BenchmarkView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.benchmarks.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.update(
            id="id",
            name="name",
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.update(
            id="id",
            name="name",
            attribution="attribution",
            description="description",
            metadata={"foo": "string"},
            required_environment_variables=["string"],
            required_secret_names=["string"],
            scenario_ids=["string"],
        )
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.update(
            id="id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(BenchmarkView, benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.update(
            id="id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(BenchmarkView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.benchmarks.with_raw_response.update(
                id="",
                name="name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.list()
        assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_definitions(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.definitions(
            id="id",
        )
        assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

    @parametrize
    async def test_method_definitions_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.definitions(
            id="id",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

    @parametrize
    async def test_raw_response_definitions(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.definitions(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_definitions(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.definitions(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(ScenarioDefinitionListView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_definitions(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.benchmarks.with_raw_response.definitions(
                id="",
            )

    @parametrize
    async def test_method_list_public(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.list_public()
        assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    async def test_method_list_public_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.list_public(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    async def test_raw_response_list_public(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_list_public(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(AsyncBenchmarksCursorIDPage[BenchmarkView], benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_start_run(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.start_run(
            benchmark_id="benchmark_id",
        )
        assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

    @parametrize
    async def test_method_start_run_with_all_params(self, async_client: AsyncRunloop) -> None:
        benchmark = await async_client.benchmarks.start_run(
            benchmark_id="benchmark_id",
            metadata={"foo": "string"},
            run_name="run_name",
            run_profile={
                "env_vars": {"foo": "string"},
                "launch_parameters": {
                    "after_idle": {
                        "idle_time_seconds": 0,
                        "on_idle": "shutdown",
                    },
                    "architecture": "x86_64",
                    "available_ports": [0],
                    "custom_cpu_cores": 0,
                    "custom_disk_size": 0,
                    "custom_gb_memory": 0,
                    "keep_alive_time_seconds": 0,
                    "launch_commands": ["string"],
                    "required_services": ["string"],
                    "resource_size_request": "X_SMALL",
                    "user_parameters": {
                        "uid": 0,
                        "username": "username",
                    },
                },
                "purpose": "purpose",
                "secrets": {"foo": "string"},
            },
        )
        assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

    @parametrize
    async def test_raw_response_start_run(self, async_client: AsyncRunloop) -> None:
        response = await async_client.benchmarks.with_raw_response.start_run(
            benchmark_id="benchmark_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        benchmark = await response.parse()
        assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

    @parametrize
    async def test_streaming_response_start_run(self, async_client: AsyncRunloop) -> None:
        async with async_client.benchmarks.with_streaming_response.start_run(
            benchmark_id="benchmark_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            benchmark = await response.parse()
            assert_matches_type(BenchmarkRunView, benchmark, path=["response"])

        assert cast(Any, response.is_closed) is True
