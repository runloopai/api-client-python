# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    BlueprintView,
    BlueprintListView,
    BlueprintPreviewView,
    BlueprintBuildLogsListView,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBlueprints:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        blueprint = client.blueprints.create()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.create(
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
            ],
            dockerfile="dockerfile",
            launch_parameters={
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "MINI",
            },
            name="name",
            system_setup_commands=["string", "string", "string"],
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        blueprint = client.blueprints.retrieve(
            "id",
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.blueprints.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        blueprint = client.blueprints.list()
        assert_matches_type(BlueprintListView, blueprint, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.list(
            limit="limit",
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(BlueprintListView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintListView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintListView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_logs(self, client: Runloop) -> None:
        blueprint = client.blueprints.logs(
            "id",
        )
        assert_matches_type(BlueprintBuildLogsListView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_logs(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.logs(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintBuildLogsListView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_logs(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.logs(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintBuildLogsListView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_logs(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.blueprints.with_raw_response.logs(
                "",
            )

    @parametrize
    def test_method_preview(self, client: Runloop) -> None:
        blueprint = client.blueprints.preview()
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    def test_method_preview_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.preview(
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
            ],
            dockerfile="dockerfile",
            launch_parameters={
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "MINI",
            },
            name="name",
            system_setup_commands=["string", "string", "string"],
        )
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_preview(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.preview()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_preview(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.preview() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBlueprints:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.create()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.create(
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
            ],
            dockerfile="dockerfile",
            launch_parameters={
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "MINI",
            },
            name="name",
            system_setup_commands=["string", "string", "string"],
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.retrieve(
            "id",
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.blueprints.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.list()
        assert_matches_type(BlueprintListView, blueprint, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.list(
            limit="limit",
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(BlueprintListView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintListView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintListView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_logs(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.logs(
            "id",
        )
        assert_matches_type(BlueprintBuildLogsListView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_logs(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.logs(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintBuildLogsListView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_logs(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.logs(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintBuildLogsListView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_logs(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.blueprints.with_raw_response.logs(
                "",
            )

    @parametrize
    async def test_method_preview(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.preview()
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    async def test_method_preview_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.preview(
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "install_command": "install_command",
                    "token": "token",
                },
            ],
            dockerfile="dockerfile",
            launch_parameters={
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "MINI",
            },
            name="name",
            system_setup_commands=["string", "string", "string"],
        )
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_preview(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.preview()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_preview(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.preview() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True
