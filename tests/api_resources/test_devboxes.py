# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    DevboxView,
    DevboxListView,
    DevboxExecutionDetailView,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDevboxes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        devbox = client.devboxes.create()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.create(
            blueprint_id="blueprint_id",
            blueprint_name="blueprint_name",
            entrypoint="entrypoint",
            environment_variables={"foo": "string"},
            file_mounts={"foo": "string"},
            launch_parameters={
                "keep_alive_time_seconds": 0,
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "MINI",
            },
            name="name",
            setup_commands=["string", "string", "string"],
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        devbox = client.devboxes.retrieve(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        devbox = client.devboxes.list()
        assert_matches_type(DevboxListView, devbox, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.list(
            limit="limit",
            starting_after="starting_after",
            status="status",
        )
        assert_matches_type(DevboxListView, devbox, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxListView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxListView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_execute_sync(self, client: Runloop) -> None:
        devbox = client.devboxes.execute_sync(
            id="id",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_execute_sync_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.execute_sync(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_execute_sync(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.execute_sync(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_execute_sync(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.execute_sync(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute_sync(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.execute_sync(
                id="",
            )

    @parametrize
    def test_method_read_file(self, client: Runloop) -> None:
        devbox = client.devboxes.read_file(
            id="id",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_read_file_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.read_file(
            id="id",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_read_file(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.read_file(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_read_file(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.read_file(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_read_file(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.read_file(
                id="",
            )

    @parametrize
    def test_method_read_file_contents(self, client: Runloop) -> None:
        devbox = client.devboxes.read_file_contents(
            id="id",
        )
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    def test_method_read_file_contents_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.read_file_contents(
            id="id",
            file_path="file_path",
        )
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    def test_raw_response_read_file_contents(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.read_file_contents(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    def test_streaming_response_read_file_contents(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.read_file_contents(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(str, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_read_file_contents(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.read_file_contents(
                id="",
            )

    @parametrize
    def test_method_shutdown(self, client: Runloop) -> None:
        devbox = client.devboxes.shutdown(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_raw_response_shutdown(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.shutdown(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_shutdown(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.shutdown(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_shutdown(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.shutdown(
                "",
            )

    @parametrize
    def test_method_upload_file(self, client: Runloop) -> None:
        devbox = client.devboxes.upload_file(
            id="id",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_method_upload_file_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.upload_file(
            id="id",
            file_input_stream=b"raw file contents",
            path="path",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_raw_response_upload_file(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.upload_file(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_streaming_response_upload_file(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.upload_file(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_upload_file(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.upload_file(
                id="",
            )

    @parametrize
    def test_method_write_file(self, client: Runloop) -> None:
        devbox = client.devboxes.write_file(
            id="id",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_write_file_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.write_file(
            id="id",
            contents="contents",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_write_file(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.write_file(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_write_file(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.write_file(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_write_file(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.write_file(
                id="",
            )


class TestAsyncDevboxes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.create()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.create(
            blueprint_id="blueprint_id",
            blueprint_name="blueprint_name",
            entrypoint="entrypoint",
            environment_variables={"foo": "string"},
            file_mounts={"foo": "string"},
            launch_parameters={
                "keep_alive_time_seconds": 0,
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "MINI",
            },
            name="name",
            setup_commands=["string", "string", "string"],
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.retrieve(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.list()
        assert_matches_type(DevboxListView, devbox, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.list(
            limit="limit",
            starting_after="starting_after",
            status="status",
        )
        assert_matches_type(DevboxListView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxListView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxListView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_execute_sync(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute_sync(
            id="id",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_execute_sync_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute_sync(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.execute_sync(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.execute_sync(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.execute_sync(
                id="",
            )

    @parametrize
    async def test_method_read_file(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.read_file(
            id="id",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_read_file_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.read_file(
            id="id",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_read_file(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.read_file(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_read_file(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.read_file(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_read_file(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.read_file(
                id="",
            )

    @parametrize
    async def test_method_read_file_contents(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.read_file_contents(
            id="id",
        )
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    async def test_method_read_file_contents_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.read_file_contents(
            id="id",
            file_path="file_path",
        )
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    async def test_raw_response_read_file_contents(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.read_file_contents(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_read_file_contents(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.read_file_contents(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(str, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_read_file_contents(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.read_file_contents(
                id="",
            )

    @parametrize
    async def test_method_shutdown(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.shutdown(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_shutdown(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.shutdown(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_shutdown(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.shutdown(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_shutdown(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.shutdown(
                "",
            )

    @parametrize
    async def test_method_upload_file(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.upload_file(
            id="id",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_method_upload_file_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.upload_file(
            id="id",
            file_input_stream=b"raw file contents",
            path="path",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_raw_response_upload_file(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.upload_file(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_upload_file(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.upload_file(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_upload_file(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.upload_file(
                id="",
            )

    @parametrize
    async def test_method_write_file(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.write_file(
            id="id",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_write_file_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.write_file(
            id="id",
            contents="contents",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_write_file(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.write_file(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_write_file(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.write_file(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_write_file(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.write_file(
                id="",
            )
