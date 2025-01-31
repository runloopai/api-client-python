# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import ScenarioRunView, ScenarioRunListView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        run = client.scenarios.runs.retrieve(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.scenarios.runs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.scenarios.runs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.runs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        run = client.scenarios.runs.list()
        assert_matches_type(ScenarioRunListView, run, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        run = client.scenarios.runs.list(
            limit=0,
            scenario_id="scenario_id",
            starting_after="starting_after",
        )
        assert_matches_type(ScenarioRunListView, run, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.scenarios.runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(ScenarioRunListView, run, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.scenarios.runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(ScenarioRunListView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_complete(self, client: Runloop) -> None:
        run = client.scenarios.runs.complete(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_raw_response_complete(self, client: Runloop) -> None:
        response = client.scenarios.runs.with_raw_response.complete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_streaming_response_complete(self, client: Runloop) -> None:
        with client.scenarios.runs.with_streaming_response.complete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_complete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.runs.with_raw_response.complete(
                "",
            )

    @parametrize
    def test_method_score(self, client: Runloop) -> None:
        run = client.scenarios.runs.score(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_raw_response_score(self, client: Runloop) -> None:
        response = client.scenarios.runs.with_raw_response.score(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_streaming_response_score(self, client: Runloop) -> None:
        with client.scenarios.runs.with_streaming_response.score(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_score(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.runs.with_raw_response.score(
                "",
            )


class TestAsyncRuns:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.retrieve(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.runs.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.runs.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.runs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.list()
        assert_matches_type(ScenarioRunListView, run, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.list(
            limit=0,
            scenario_id="scenario_id",
            starting_after="starting_after",
        )
        assert_matches_type(ScenarioRunListView, run, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(ScenarioRunListView, run, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(ScenarioRunListView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_complete(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.complete(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_raw_response_complete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.runs.with_raw_response.complete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_streaming_response_complete(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.runs.with_streaming_response.complete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_complete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.runs.with_raw_response.complete(
                "",
            )

    @parametrize
    async def test_method_score(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.score(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_raw_response_score(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.runs.with_raw_response.score(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_streaming_response_score(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.runs.with_streaming_response.score(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_score(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.runs.with_raw_response.score(
                "",
            )
