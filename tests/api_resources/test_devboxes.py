# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    DevboxView,
    DevboxListView,
    DevboxSnapshotListView,
    DevboxExecutionDetailView,
    DevboxCreateSSHKeyResponse,
    DevboxAsyncExecutionDetailView,
)
from runloop_api_client._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
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
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                },
            ],
            entrypoint="entrypoint",
            environment_variables={"foo": "string"},
            file_mounts={"foo": "string"},
            launch_parameters={
                "keep_alive_time_seconds": 0,
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "SMALL",
            },
            metadata={"foo": "string"},
            name="name",
            prebuilt="prebuilt",
            setup_commands=["string", "string", "string"],
            snapshot_id="snapshot_id",
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
            limit=0,
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
    def test_method_create_ssh_key(self, client: Runloop) -> None:
        devbox = client.devboxes.create_ssh_key(
            "id",
        )
        assert_matches_type(DevboxCreateSSHKeyResponse, devbox, path=["response"])

    @parametrize
    def test_raw_response_create_ssh_key(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.create_ssh_key(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxCreateSSHKeyResponse, devbox, path=["response"])

    @parametrize
    def test_streaming_response_create_ssh_key(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.create_ssh_key(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxCreateSSHKeyResponse, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_ssh_key(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.create_ssh_key(
                "",
            )

    @parametrize
    def test_method_disk_snapshots(self, client: Runloop) -> None:
        devbox = client.devboxes.disk_snapshots()
        assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

    @parametrize
    def test_method_disk_snapshots_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.disk_snapshots(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

    @parametrize
    def test_raw_response_disk_snapshots(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.disk_snapshots()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_disk_snapshots(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.disk_snapshots() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download_file(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/devboxes/id/download_file").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        devbox = client.devboxes.download_file(
            id="id",
            path="path",
        )
        assert devbox.is_closed
        assert devbox.json() == {"foo": "bar"}
        assert cast(Any, devbox.is_closed) is True
        assert isinstance(devbox, BinaryAPIResponse)

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download_file(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/devboxes/id/download_file").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        devbox = client.devboxes.with_raw_response.download_file(
            id="id",
            path="path",
        )

        assert devbox.is_closed is True
        assert devbox.http_request.headers.get("X-Stainless-Lang") == "python"
        assert devbox.json() == {"foo": "bar"}
        assert isinstance(devbox, BinaryAPIResponse)

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download_file(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/devboxes/id/download_file").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.devboxes.with_streaming_response.download_file(
            id="id",
            path="path",
        ) as devbox:
            assert not devbox.is_closed
            assert devbox.http_request.headers.get("X-Stainless-Lang") == "python"

            assert devbox.json() == {"foo": "bar"}
            assert cast(Any, devbox.is_closed) is True
            assert isinstance(devbox, StreamedBinaryAPIResponse)

        assert cast(Any, devbox.is_closed) is True

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download_file(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.download_file(
                id="",
                path="path",
            )

    @parametrize
    def test_method_execute_async(self, client: Runloop) -> None:
        devbox = client.devboxes.execute_async(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_execute_async_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.execute_async(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_execute_async(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.execute_async(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_execute_async(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.execute_async(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute_async(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.execute_async(
                id="",
                command="command",
            )

    @parametrize
    def test_method_execute_sync(self, client: Runloop) -> None:
        devbox = client.devboxes.execute_sync(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_execute_sync_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.execute_sync(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_execute_sync(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.execute_sync(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_execute_sync(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.execute_sync(
            id="id",
            command="command",
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
                command="command",
            )

    @parametrize
    def test_method_read_file_contents(self, client: Runloop) -> None:
        devbox = client.devboxes.read_file_contents(
            id="id",
            file_path="file_path",
        )
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    def test_raw_response_read_file_contents(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.read_file_contents(
            id="id",
            file_path="file_path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    def test_streaming_response_read_file_contents(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.read_file_contents(
            id="id",
            file_path="file_path",
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
                file_path="file_path",
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
    def test_method_snapshot_disk(self, client: Runloop) -> None:
        devbox = client.devboxes.snapshot_disk(
            id="id",
        )
        assert devbox is None

    @parametrize
    def test_method_snapshot_disk_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.snapshot_disk(
            id="id",
            metadata={"foo": "string"},
            name="name",
        )
        assert devbox is None

    @parametrize
    def test_raw_response_snapshot_disk(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.snapshot_disk(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert devbox is None

    @parametrize
    def test_streaming_response_snapshot_disk(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.snapshot_disk(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert devbox is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_snapshot_disk(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.snapshot_disk(
                id="",
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
            file=b"raw file contents",
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
            contents="contents",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_write_file(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.write_file(
            id="id",
            contents="contents",
            file_path="file_path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_write_file(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.write_file(
            id="id",
            contents="contents",
            file_path="file_path",
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
                contents="contents",
                file_path="file_path",
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
            code_mounts=[
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                },
                {
                    "repo_name": "repo_name",
                    "repo_owner": "repo_owner",
                    "token": "token",
                    "install_command": "install_command",
                },
            ],
            entrypoint="entrypoint",
            environment_variables={"foo": "string"},
            file_mounts={"foo": "string"},
            launch_parameters={
                "keep_alive_time_seconds": 0,
                "launch_commands": ["string", "string", "string"],
                "resource_size_request": "SMALL",
            },
            metadata={"foo": "string"},
            name="name",
            prebuilt="prebuilt",
            setup_commands=["string", "string", "string"],
            snapshot_id="snapshot_id",
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
            limit=0,
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
    async def test_method_create_ssh_key(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.create_ssh_key(
            "id",
        )
        assert_matches_type(DevboxCreateSSHKeyResponse, devbox, path=["response"])

    @parametrize
    async def test_raw_response_create_ssh_key(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.create_ssh_key(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxCreateSSHKeyResponse, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_create_ssh_key(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.create_ssh_key(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxCreateSSHKeyResponse, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_ssh_key(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.create_ssh_key(
                "",
            )

    @parametrize
    async def test_method_disk_snapshots(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.disk_snapshots()
        assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

    @parametrize
    async def test_method_disk_snapshots_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.disk_snapshots(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_disk_snapshots(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.disk_snapshots()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_disk_snapshots(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.disk_snapshots() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxSnapshotListView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download_file(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/devboxes/id/download_file").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        devbox = await async_client.devboxes.download_file(
            id="id",
            path="path",
        )
        assert devbox.is_closed
        assert await devbox.json() == {"foo": "bar"}
        assert cast(Any, devbox.is_closed) is True
        assert isinstance(devbox, AsyncBinaryAPIResponse)

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download_file(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/devboxes/id/download_file").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        devbox = await async_client.devboxes.with_raw_response.download_file(
            id="id",
            path="path",
        )

        assert devbox.is_closed is True
        assert devbox.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await devbox.json() == {"foo": "bar"}
        assert isinstance(devbox, AsyncBinaryAPIResponse)

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download_file(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/devboxes/id/download_file").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.devboxes.with_streaming_response.download_file(
            id="id",
            path="path",
        ) as devbox:
            assert not devbox.is_closed
            assert devbox.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await devbox.json() == {"foo": "bar"}
            assert cast(Any, devbox.is_closed) is True
            assert isinstance(devbox, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, devbox.is_closed) is True

    @pytest.mark.skip(reason="prism can't support octet")
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download_file(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.download_file(
                id="",
                path="path",
            )

    @parametrize
    async def test_method_execute_async(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute_async(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_execute_async_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute_async(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_execute_async(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.execute_async(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_execute_async(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.execute_async(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute_async(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.execute_async(
                id="",
                command="command",
            )

    @parametrize
    async def test_method_execute_sync(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute_sync(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_execute_sync_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute_sync(
            id="id",
            command="command",
            shell_name="shell_name",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.execute_sync(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.execute_sync(
            id="id",
            command="command",
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
                command="command",
            )

    @parametrize
    async def test_method_read_file_contents(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.read_file_contents(
            id="id",
            file_path="file_path",
        )
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    async def test_raw_response_read_file_contents(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.read_file_contents(
            id="id",
            file_path="file_path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(str, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_read_file_contents(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.read_file_contents(
            id="id",
            file_path="file_path",
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
                file_path="file_path",
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
    async def test_method_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.snapshot_disk(
            id="id",
        )
        assert devbox is None

    @parametrize
    async def test_method_snapshot_disk_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.snapshot_disk(
            id="id",
            metadata={"foo": "string"},
            name="name",
        )
        assert devbox is None

    @parametrize
    async def test_raw_response_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.snapshot_disk(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert devbox is None

    @parametrize
    async def test_streaming_response_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.snapshot_disk(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert devbox is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.snapshot_disk(
                id="",
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
            file=b"raw file contents",
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
            contents="contents",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_write_file(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.write_file(
            id="id",
            contents="contents",
            file_path="file_path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_write_file(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.write_file(
            id="id",
            contents="contents",
            file_path="file_path",
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
                contents="contents",
                file_path="file_path",
            )
