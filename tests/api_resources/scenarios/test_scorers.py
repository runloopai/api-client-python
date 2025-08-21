# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.pagination import SyncScenarioScorersCursorIDPage, AsyncScenarioScorersCursorIDPage
from runloop_api_client.types.scenarios import (
    ScorerListResponse,
    ScorerCreateResponse,
    ScorerUpdateResponse,
    ScorerRetrieveResponse,
    ScorerValidateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScorers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.create(
            bash_script="bash_script",
            type="type",
        )
        assert_matches_type(ScorerCreateResponse, scorer, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.scenarios.scorers.with_raw_response.create(
            bash_script="bash_script",
            type="type",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = response.parse()
        assert_matches_type(ScorerCreateResponse, scorer, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.scenarios.scorers.with_streaming_response.create(
            bash_script="bash_script",
            type="type",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = response.parse()
            assert_matches_type(ScorerCreateResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.retrieve(
            "id",
        )
        assert_matches_type(ScorerRetrieveResponse, scorer, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.scenarios.scorers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = response.parse()
        assert_matches_type(ScorerRetrieveResponse, scorer, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.scenarios.scorers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = response.parse()
            assert_matches_type(ScorerRetrieveResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.scorers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.update(
            id="id",
            bash_script="bash_script",
            type="type",
        )
        assert_matches_type(ScorerUpdateResponse, scorer, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.scenarios.scorers.with_raw_response.update(
            id="id",
            bash_script="bash_script",
            type="type",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = response.parse()
        assert_matches_type(ScorerUpdateResponse, scorer, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.scenarios.scorers.with_streaming_response.update(
            id="id",
            bash_script="bash_script",
            type="type",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = response.parse()
            assert_matches_type(ScorerUpdateResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.scorers.with_raw_response.update(
                id="",
                bash_script="bash_script",
                type="type",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.list()
        assert_matches_type(SyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.scenarios.scorers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = response.parse()
        assert_matches_type(SyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.scenarios.scorers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = response.parse()
            assert_matches_type(SyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_validate(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.validate(
            id="id",
            scoring_context={},
        )
        assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

    @parametrize
    def test_method_validate_with_all_params(self, client: Runloop) -> None:
        scorer = client.scenarios.scorers.validate(
            id="id",
            scoring_context={},
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
        )
        assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

    @parametrize
    def test_raw_response_validate(self, client: Runloop) -> None:
        response = client.scenarios.scorers.with_raw_response.validate(
            id="id",
            scoring_context={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = response.parse()
        assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

    @parametrize
    def test_streaming_response_validate(self, client: Runloop) -> None:
        with client.scenarios.scorers.with_streaming_response.validate(
            id="id",
            scoring_context={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = response.parse()
            assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_validate(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.scorers.with_raw_response.validate(
                id="",
                scoring_context={},
            )


class TestAsyncScorers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.create(
            bash_script="bash_script",
            type="type",
        )
        assert_matches_type(ScorerCreateResponse, scorer, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.scorers.with_raw_response.create(
            bash_script="bash_script",
            type="type",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = await response.parse()
        assert_matches_type(ScorerCreateResponse, scorer, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.scorers.with_streaming_response.create(
            bash_script="bash_script",
            type="type",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = await response.parse()
            assert_matches_type(ScorerCreateResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.retrieve(
            "id",
        )
        assert_matches_type(ScorerRetrieveResponse, scorer, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.scorers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = await response.parse()
        assert_matches_type(ScorerRetrieveResponse, scorer, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.scorers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = await response.parse()
            assert_matches_type(ScorerRetrieveResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.scorers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.update(
            id="id",
            bash_script="bash_script",
            type="type",
        )
        assert_matches_type(ScorerUpdateResponse, scorer, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.scorers.with_raw_response.update(
            id="id",
            bash_script="bash_script",
            type="type",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = await response.parse()
        assert_matches_type(ScorerUpdateResponse, scorer, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.scorers.with_streaming_response.update(
            id="id",
            bash_script="bash_script",
            type="type",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = await response.parse()
            assert_matches_type(ScorerUpdateResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.scorers.with_raw_response.update(
                id="",
                bash_script="bash_script",
                type="type",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.list()
        assert_matches_type(AsyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.scorers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = await response.parse()
        assert_matches_type(AsyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.scorers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = await response.parse()
            assert_matches_type(AsyncScenarioScorersCursorIDPage[ScorerListResponse], scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_validate(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.validate(
            id="id",
            scoring_context={},
        )
        assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

    @parametrize
    async def test_method_validate_with_all_params(self, async_client: AsyncRunloop) -> None:
        scorer = await async_client.scenarios.scorers.validate(
            id="id",
            scoring_context={},
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
        )
        assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

    @parametrize
    async def test_raw_response_validate(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.scorers.with_raw_response.validate(
            id="id",
            scoring_context={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = await response.parse()
        assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

    @parametrize
    async def test_streaming_response_validate(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.scorers.with_streaming_response.validate(
            id="id",
            scoring_context={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = await response.parse()
            assert_matches_type(ScorerValidateResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_validate(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.scorers.with_raw_response.validate(
                id="",
                scoring_context={},
            )
