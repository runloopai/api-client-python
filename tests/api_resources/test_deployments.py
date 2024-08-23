# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    DeploymentGetResponse,
    DeploymentLogsResponse,
    DeploymentTailResponse,
    DeploymentRedeployResponse,
    DeploymentRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        deployment = client.deployments.retrieve(
            "deployment_id",
        )
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.deployments.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.deployments.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_get(self, client: Runloop) -> None:
        deployment = client.deployments.get()
        assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

    @parametrize
    def test_method_get_with_all_params(self, client: Runloop) -> None:
        deployment = client.deployments.get(
            limit="limit",
            starting_after="starting_after",
        )
        assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Runloop) -> None:
        response = client.deployments.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Runloop) -> None:
        with client.deployments.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_logs(self, client: Runloop) -> None:
        deployment = client.deployments.logs(
            "deployment_id",
        )
        assert_matches_type(DeploymentLogsResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_logs(self, client: Runloop) -> None:
        response = client.deployments.with_raw_response.logs(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentLogsResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_logs(self, client: Runloop) -> None:
        with client.deployments.with_streaming_response.logs(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentLogsResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_logs(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.logs(
                "",
            )

    @parametrize
    def test_method_redeploy(self, client: Runloop) -> None:
        deployment = client.deployments.redeploy(
            "deployment_id",
        )
        assert_matches_type(DeploymentRedeployResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_redeploy(self, client: Runloop) -> None:
        response = client.deployments.with_raw_response.redeploy(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentRedeployResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_redeploy(self, client: Runloop) -> None:
        with client.deployments.with_streaming_response.redeploy(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentRedeployResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_redeploy(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.redeploy(
                "",
            )

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    def test_method_tail(self, client: Runloop) -> None:
        deployment = client.deployments.tail(
            "deployment_id",
        )
        assert_matches_type(DeploymentTailResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    def test_raw_response_tail(self, client: Runloop) -> None:
        response = client.deployments.with_raw_response.tail(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentTailResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    def test_streaming_response_tail(self, client: Runloop) -> None:
        with client.deployments.with_streaming_response.tail(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentTailResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    def test_path_params_tail(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deployments.with_raw_response.tail(
                "",
            )


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        deployment = await async_client.deployments.retrieve(
            "deployment_id",
        )
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.deployments.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.deployments.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncRunloop) -> None:
        deployment = await async_client.deployments.get()
        assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

    @parametrize
    async def test_method_get_with_all_params(self, async_client: AsyncRunloop) -> None:
        deployment = await async_client.deployments.get(
            limit="limit",
            starting_after="starting_after",
        )
        assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncRunloop) -> None:
        response = await async_client.deployments.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncRunloop) -> None:
        async with async_client.deployments.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentGetResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_logs(self, async_client: AsyncRunloop) -> None:
        deployment = await async_client.deployments.logs(
            "deployment_id",
        )
        assert_matches_type(DeploymentLogsResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_logs(self, async_client: AsyncRunloop) -> None:
        response = await async_client.deployments.with_raw_response.logs(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentLogsResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_logs(self, async_client: AsyncRunloop) -> None:
        async with async_client.deployments.with_streaming_response.logs(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentLogsResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_logs(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.logs(
                "",
            )

    @parametrize
    async def test_method_redeploy(self, async_client: AsyncRunloop) -> None:
        deployment = await async_client.deployments.redeploy(
            "deployment_id",
        )
        assert_matches_type(DeploymentRedeployResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_redeploy(self, async_client: AsyncRunloop) -> None:
        response = await async_client.deployments.with_raw_response.redeploy(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentRedeployResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_redeploy(self, async_client: AsyncRunloop) -> None:
        async with async_client.deployments.with_streaming_response.redeploy(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentRedeployResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_redeploy(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.redeploy(
                "",
            )

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    async def test_method_tail(self, async_client: AsyncRunloop) -> None:
        deployment = await async_client.deployments.tail(
            "deployment_id",
        )
        assert_matches_type(DeploymentTailResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    async def test_raw_response_tail(self, async_client: AsyncRunloop) -> None:
        response = await async_client.deployments.with_raw_response.tail(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentTailResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    async def test_streaming_response_tail(self, async_client: AsyncRunloop) -> None:
        async with async_client.deployments.with_streaming_response.tail(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentTailResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="cannot test text/event-stream")
    @parametrize
    async def test_path_params_tail(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deployments.with_raw_response.tail(
                "",
            )
