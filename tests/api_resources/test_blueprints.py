# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    BlueprintView,
    BlueprintPreviewView,
    BlueprintBuildLogsListView,
)
from runloop_api_client.pagination import SyncBlueprintsCursorIDPage, AsyncBlueprintsCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBlueprints:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        blueprint = client.blueprints.create(
            name="name",
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.create(
            name="name",
            base_blueprint_id="base_blueprint_id",
            base_blueprint_name="base_blueprint_name",
            build_args={"foo": "string"},
            build_context={
                "object_id": "object_id",
                "type": "object",
            },
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                }
            ],
            dockerfile="dockerfile",
            file_mounts={"foo": "string"},
            launch_parameters={
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
            metadata={"foo": "string"},
            named_build_contexts={
                "foo": {
                    "object_id": "object_id",
                    "type": "object",
                }
            },
            secrets={"foo": "string"},
            services=[
                {
                    "image": "image",
                    "name": "name",
                    "credentials": {
                        "password": "password",
                        "username": "username",
                    },
                    "env": {"foo": "string"},
                    "options": "options",
                    "port_mappings": ["string"],
                }
            ],
            system_setup_commands=["string"],
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_create_rejects_large_file_mount(self, client: Runloop) -> None:
        # 98,250 bytes + 1 byte (pre-encoded limit to stay within ~131,000 b64'd)
        too_large_content = "a" * (98_250 + 1)
        with pytest.raises(ValueError, match=r"over the limit"):
            client.blueprints.create(
                name="name",
                file_mounts={"/tmp/large.txt": too_large_content},
            )

    @parametrize
    def test_create_rejects_total_file_mount_size(self, client: Runloop) -> None:
        # Eighty files at per-file max (98,250) equals current total limit; add 1 byte to exceed
        per_file_max = 98_250
        file_mounts = {f"/tmp/{i}.txt": "a" * per_file_max for i in range(80)}
        file_mounts["/tmp/extra.txt"] = "x"
        with pytest.raises(ValueError, match=r"total file_mounts size .* over the limit"):
            client.blueprints.create(
                name="name",
                file_mounts=file_mounts,
            )

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
        assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.list(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        blueprint = client.blueprints.delete(
            "id",
        )
        assert_matches_type(object, blueprint, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(object, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(object, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.blueprints.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_create_from_inspection(self, client: Runloop) -> None:
        blueprint = client.blueprints.create_from_inspection(
            inspection_source={"inspection_id": "inspection_id"},
            name="name",
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_method_create_from_inspection_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.create_from_inspection(
            inspection_source={
                "inspection_id": "inspection_id",
                "github_auth_token": "github_auth_token",
            },
            name="name",
            file_mounts={"foo": "string"},
            launch_parameters={
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
            metadata={"foo": "string"},
            secrets={"foo": "string"},
            system_setup_commands=["string"],
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_create_from_inspection(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.create_from_inspection(
            inspection_source={"inspection_id": "inspection_id"},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_create_from_inspection(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.create_from_inspection(
            inspection_source={"inspection_id": "inspection_id"},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_public(self, client: Runloop) -> None:
        blueprint = client.blueprints.list_public()
        assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    def test_method_list_public_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.list_public(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    def test_raw_response_list_public(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    def test_streaming_response_list_public(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(SyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

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
        blueprint = client.blueprints.preview(
            name="name",
        )
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    def test_method_preview_with_all_params(self, client: Runloop) -> None:
        blueprint = client.blueprints.preview(
            name="name",
            base_blueprint_id="base_blueprint_id",
            base_blueprint_name="base_blueprint_name",
            build_args={"foo": "string"},
            build_context={
                "object_id": "object_id",
                "type": "object",
            },
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                }
            ],
            dockerfile="dockerfile",
            file_mounts={"foo": "string"},
            launch_parameters={
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
            metadata={"foo": "string"},
            named_build_contexts={
                "foo": {
                    "object_id": "object_id",
                    "type": "object",
                }
            },
            secrets={"foo": "string"},
            services=[
                {
                    "image": "image",
                    "name": "name",
                    "credentials": {
                        "password": "password",
                        "username": "username",
                    },
                    "env": {"foo": "string"},
                    "options": "options",
                    "port_mappings": ["string"],
                }
            ],
            system_setup_commands=["string"],
        )
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    def test_raw_response_preview(self, client: Runloop) -> None:
        response = client.blueprints.with_raw_response.preview(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = response.parse()
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    def test_streaming_response_preview(self, client: Runloop) -> None:
        with client.blueprints.with_streaming_response.preview(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = response.parse()
            assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBlueprints:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.create(
            name="name",
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.create(
            name="name",
            base_blueprint_id="base_blueprint_id",
            base_blueprint_name="base_blueprint_name",
            build_args={"foo": "string"},
            build_context={
                "object_id": "object_id",
                "type": "object",
            },
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                }
            ],
            dockerfile="dockerfile",
            file_mounts={"foo": "string"},
            launch_parameters={
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
            metadata={"foo": "string"},
            named_build_contexts={
                "foo": {
                    "object_id": "object_id",
                    "type": "object",
                }
            },
            secrets={"foo": "string"},
            services=[
                {
                    "image": "image",
                    "name": "name",
                    "credentials": {
                        "password": "password",
                        "username": "username",
                    },
                    "env": {"foo": "string"},
                    "options": "options",
                    "port_mappings": ["string"],
                }
            ],
            system_setup_commands=["string"],
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_create_rejects_large_file_mount(self, async_client: AsyncRunloop) -> None:
        # 98,250 bytes + 1 byte (pre-encoded limit to stay within ~131,000 b64'd)
        too_large_content = "a" * (98_250 + 1)
        with pytest.raises(ValueError, match=r"over the limit"):
            await async_client.blueprints.create(
                name="name",
                file_mounts={"/tmp/large.txt": too_large_content},
            )

    @parametrize
    async def test_create_rejects_total_file_mount_size(self, async_client: AsyncRunloop) -> None:
        # Eighty files at per-file max (98,250) equals current total limit; add 1 byte to exceed
        per_file_max = 98_250
        file_mounts = {f"/tmp/{i}.txt": "a" * per_file_max for i in range(80)}
        file_mounts["/tmp/extra.txt"] = "x"
        with pytest.raises(ValueError, match=r"total file_mounts size .* over the limit"):
            await async_client.blueprints.create(
                name="name",
                file_mounts=file_mounts,
            )

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
        assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.list(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.delete(
            "id",
        )
        assert_matches_type(object, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(object, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(object, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.blueprints.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_create_from_inspection(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.create_from_inspection(
            inspection_source={"inspection_id": "inspection_id"},
            name="name",
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_method_create_from_inspection_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.create_from_inspection(
            inspection_source={
                "inspection_id": "inspection_id",
                "github_auth_token": "github_auth_token",
            },
            name="name",
            file_mounts={"foo": "string"},
            launch_parameters={
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
            metadata={"foo": "string"},
            secrets={"foo": "string"},
            system_setup_commands=["string"],
        )
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_create_from_inspection(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.create_from_inspection(
            inspection_source={"inspection_id": "inspection_id"},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_create_from_inspection(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.create_from_inspection(
            inspection_source={"inspection_id": "inspection_id"},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_public(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.list_public()
        assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    async def test_method_list_public_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.list_public(
            limit=0,
            name="name",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    async def test_raw_response_list_public(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.list_public()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_list_public(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.list_public() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(AsyncBlueprintsCursorIDPage[BlueprintView], blueprint, path=["response"])

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
        blueprint = await async_client.blueprints.preview(
            name="name",
        )
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    async def test_method_preview_with_all_params(self, async_client: AsyncRunloop) -> None:
        blueprint = await async_client.blueprints.preview(
            name="name",
            base_blueprint_id="base_blueprint_id",
            base_blueprint_name="base_blueprint_name",
            build_args={"foo": "string"},
            build_context={
                "object_id": "object_id",
                "type": "object",
            },
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                }
            ],
            dockerfile="dockerfile",
            file_mounts={"foo": "string"},
            launch_parameters={
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
            metadata={"foo": "string"},
            named_build_contexts={
                "foo": {
                    "object_id": "object_id",
                    "type": "object",
                }
            },
            secrets={"foo": "string"},
            services=[
                {
                    "image": "image",
                    "name": "name",
                    "credentials": {
                        "password": "password",
                        "username": "username",
                    },
                    "env": {"foo": "string"},
                    "options": "options",
                    "port_mappings": ["string"],
                }
            ],
            system_setup_commands=["string"],
        )
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    async def test_raw_response_preview(self, async_client: AsyncRunloop) -> None:
        response = await async_client.blueprints.with_raw_response.preview(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        blueprint = await response.parse()
        assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

    @parametrize
    async def test_streaming_response_preview(self, async_client: AsyncRunloop) -> None:
        async with async_client.blueprints.with_streaming_response.preview(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            blueprint = await response.parse()
            assert_matches_type(BlueprintPreviewView, blueprint, path=["response"])

        assert cast(Any, response.is_closed) is True
