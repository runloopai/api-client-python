# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    ScenarioView,
    ScenarioRunView,
)
from runloop_api_client.pagination import SyncScenariosCursorIDPage, AsyncScenariosCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScenarios:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        scenario = client.scenarios.create(
            input_context={"problem_statement": "problem_statement"},
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                        },
                        "weight": 0,
                    }
                ]
            },
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        scenario = client.scenarios.create(
            input_context={
                "problem_statement": "problem_statement",
                "additional_context": {},
            },
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                            "lang": "lang",
                        },
                        "weight": 0,
                    }
                ]
            },
            environment_parameters={
                "blueprint_id": "blueprint_id",
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
                "snapshot_id": "snapshot_id",
                "working_directory": "working_directory",
            },
            metadata={"foo": "string"},
            reference_output="reference_output",
            required_environment_variables=["string"],
            required_secret_names=["string"],
            validation_type="UNSPECIFIED",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.scenarios.with_raw_response.create(
            input_context={"problem_statement": "problem_statement"},
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                        },
                        "weight": 0,
                    }
                ]
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = response.parse()
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.scenarios.with_streaming_response.create(
            input_context={"problem_statement": "problem_statement"},
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                        },
                        "weight": 0,
                    }
                ]
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = response.parse()
            assert_matches_type(ScenarioView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        scenario = client.scenarios.retrieve(
            "id",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.scenarios.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = response.parse()
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.scenarios.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = response.parse()
            assert_matches_type(ScenarioView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        scenario = client.scenarios.update(
            id="id",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        scenario = client.scenarios.update(
            id="id",
            environment_parameters={
                "blueprint_id": "blueprint_id",
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
                "snapshot_id": "snapshot_id",
                "working_directory": "working_directory",
            },
            input_context={
                "additional_context": {},
                "problem_statement": "problem_statement",
            },
            metadata={"foo": "string"},
            name="name",
            reference_output="reference_output",
            required_environment_variables=["string"],
            required_secret_names=["string"],
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                            "lang": "lang",
                        },
                        "weight": 0,
                    }
                ]
            },
            validation_type="UNSPECIFIED",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.scenarios.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = response.parse()
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.scenarios.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = response.parse()
            assert_matches_type(ScenarioView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        scenario = client.scenarios.list()
        assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        scenario = client.scenarios.list(
            benchmark_id="benchmark_id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.scenarios.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = response.parse()
        assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.scenarios.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = response.parse()
            assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_public(self, client: Runloop) -> None:
        scenario = client.scenarios.list_public()
        assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    def test_method_list_public_with_all_params(self, client: Runloop) -> None:
        scenario = client.scenarios.list_public(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    def test_raw_response_list_public(self, client: Runloop) -> None:
        response = client.scenarios.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = response.parse()
        assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    def test_streaming_response_list_public(self, client: Runloop) -> None:
        with client.scenarios.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = response.parse()
            assert_matches_type(SyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_start_run(self, client: Runloop) -> None:
        scenario = client.scenarios.start_run(
            scenario_id="scenario_id",
        )
        assert_matches_type(ScenarioRunView, scenario, path=["response"])

    @parametrize
    def test_method_start_run_with_all_params(self, client: Runloop) -> None:
        scenario = client.scenarios.start_run(
            scenario_id="scenario_id",
            benchmark_run_id="benchmark_run_id",
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
        assert_matches_type(ScenarioRunView, scenario, path=["response"])

    @parametrize
    def test_raw_response_start_run(self, client: Runloop) -> None:
        response = client.scenarios.with_raw_response.start_run(
            scenario_id="scenario_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = response.parse()
        assert_matches_type(ScenarioRunView, scenario, path=["response"])

    @parametrize
    def test_streaming_response_start_run(self, client: Runloop) -> None:
        with client.scenarios.with_streaming_response.start_run(
            scenario_id="scenario_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = response.parse()
            assert_matches_type(ScenarioRunView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncScenarios:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.create(
            input_context={"problem_statement": "problem_statement"},
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                        },
                        "weight": 0,
                    }
                ]
            },
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.create(
            input_context={
                "problem_statement": "problem_statement",
                "additional_context": {},
            },
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                            "lang": "lang",
                        },
                        "weight": 0,
                    }
                ]
            },
            environment_parameters={
                "blueprint_id": "blueprint_id",
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
                "snapshot_id": "snapshot_id",
                "working_directory": "working_directory",
            },
            metadata={"foo": "string"},
            reference_output="reference_output",
            required_environment_variables=["string"],
            required_secret_names=["string"],
            validation_type="UNSPECIFIED",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.with_raw_response.create(
            input_context={"problem_statement": "problem_statement"},
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                        },
                        "weight": 0,
                    }
                ]
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = await response.parse()
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.with_streaming_response.create(
            input_context={"problem_statement": "problem_statement"},
            name="name",
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                        },
                        "weight": 0,
                    }
                ]
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = await response.parse()
            assert_matches_type(ScenarioView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.retrieve(
            "id",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = await response.parse()
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = await response.parse()
            assert_matches_type(ScenarioView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.update(
            id="id",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.update(
            id="id",
            environment_parameters={
                "blueprint_id": "blueprint_id",
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
                "snapshot_id": "snapshot_id",
                "working_directory": "working_directory",
            },
            input_context={
                "additional_context": {},
                "problem_statement": "problem_statement",
            },
            metadata={"foo": "string"},
            name="name",
            reference_output="reference_output",
            required_environment_variables=["string"],
            required_secret_names=["string"],
            scoring_contract={
                "scoring_function_parameters": [
                    {
                        "name": "name",
                        "scorer": {
                            "pattern": "pattern",
                            "search_directory": "search_directory",
                            "type": "ast_grep_scorer",
                            "lang": "lang",
                        },
                        "weight": 0,
                    }
                ]
            },
            validation_type="UNSPECIFIED",
        )
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = await response.parse()
        assert_matches_type(ScenarioView, scenario, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = await response.parse()
            assert_matches_type(ScenarioView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.list()
        assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.list(
            benchmark_id="benchmark_id",
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = await response.parse()
        assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = await response.parse()
            assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_public(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.list_public()
        assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    async def test_method_list_public_with_all_params(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.list_public(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    async def test_raw_response_list_public(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = await response.parse()
        assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

    @parametrize
    async def test_streaming_response_list_public(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = await response.parse()
            assert_matches_type(AsyncScenariosCursorIDPage[ScenarioView], scenario, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_start_run(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.start_run(
            scenario_id="scenario_id",
        )
        assert_matches_type(ScenarioRunView, scenario, path=["response"])

    @parametrize
    async def test_method_start_run_with_all_params(self, async_client: AsyncRunloop) -> None:
        scenario = await async_client.scenarios.start_run(
            scenario_id="scenario_id",
            benchmark_run_id="benchmark_run_id",
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
        assert_matches_type(ScenarioRunView, scenario, path=["response"])

    @parametrize
    async def test_raw_response_start_run(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.with_raw_response.start_run(
            scenario_id="scenario_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scenario = await response.parse()
        assert_matches_type(ScenarioRunView, scenario, path=["response"])

    @parametrize
    async def test_streaming_response_start_run(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.with_streaming_response.start_run(
            scenario_id="scenario_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scenario = await response.parse()
            assert_matches_type(ScenarioRunView, scenario, path=["response"])

        assert cast(Any, response.is_closed) is True
