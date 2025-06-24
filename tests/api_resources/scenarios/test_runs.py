# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import ScenarioRunView
from runloop_api_client._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from runloop_api_client.pagination import SyncBenchmarkRunsCursorIDPage, AsyncBenchmarkRunsCursorIDPage

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
        assert_matches_type(SyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        run = client.scenarios.runs.list(
            limit=0,
            scenario_id="scenario_id",
            starting_after="starting_after",
        )
        assert_matches_type(SyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.scenarios.runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(SyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.scenarios.runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(SyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_cancel(self, client: Runloop) -> None:
        run = client.scenarios.runs.cancel(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: Runloop) -> None:
        response = client.scenarios.runs.with_raw_response.cancel(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: Runloop) -> None:
        with client.scenarios.runs.with_streaming_response.cancel(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.runs.with_raw_response.cancel(
                "",
            )

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
    @pytest.mark.respx(base_url=base_url)
    def test_method_download_logs(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/scenarios/runs/id/download_logs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        run = client.scenarios.runs.download_logs(
            "id",
        )
        assert run.is_closed
        assert run.json() == {"foo": "bar"}
        assert cast(Any, run.is_closed) is True
        assert isinstance(run, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download_logs(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/scenarios/runs/id/download_logs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        run = client.scenarios.runs.with_raw_response.download_logs(
            "id",
        )

        assert run.is_closed is True
        assert run.http_request.headers.get("X-Stainless-Lang") == "python"
        assert run.json() == {"foo": "bar"}
        assert isinstance(run, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download_logs(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/scenarios/runs/id/download_logs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.scenarios.runs.with_streaming_response.download_logs(
            "id",
        ) as run:
            assert not run.is_closed
            assert run.http_request.headers.get("X-Stainless-Lang") == "python"

            assert run.json() == {"foo": "bar"}
            assert cast(Any, run.is_closed) is True
            assert isinstance(run, StreamedBinaryAPIResponse)

        assert cast(Any, run.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download_logs(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.scenarios.runs.with_raw_response.download_logs(
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
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

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
        assert_matches_type(AsyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.list(
            limit=0,
            scenario_id="scenario_id",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(AsyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(AsyncBenchmarkRunsCursorIDPage[ScenarioRunView], run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_cancel(self, async_client: AsyncRunloop) -> None:
        run = await async_client.scenarios.runs.cancel(
            "id",
        )
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncRunloop) -> None:
        response = await async_client.scenarios.runs.with_raw_response.cancel(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(ScenarioRunView, run, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncRunloop) -> None:
        async with async_client.scenarios.runs.with_streaming_response.cancel(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(ScenarioRunView, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.runs.with_raw_response.cancel(
                "",
            )

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
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download_logs(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/scenarios/runs/id/download_logs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        run = await async_client.scenarios.runs.download_logs(
            "id",
        )
        assert run.is_closed
        assert await run.json() == {"foo": "bar"}
        assert cast(Any, run.is_closed) is True
        assert isinstance(run, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download_logs(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/scenarios/runs/id/download_logs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        run = await async_client.scenarios.runs.with_raw_response.download_logs(
            "id",
        )

        assert run.is_closed is True
        assert run.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await run.json() == {"foo": "bar"}
        assert isinstance(run, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download_logs(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/scenarios/runs/id/download_logs").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.scenarios.runs.with_streaming_response.download_logs(
            "id",
        ) as run:
            assert not run.is_closed
            assert run.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await run.json() == {"foo": "bar"}
            assert cast(Any, run.is_closed) is True
            assert isinstance(run, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, run.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download_logs(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.scenarios.runs.with_raw_response.download_logs(
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
