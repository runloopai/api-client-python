# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast
from unittest.mock import Mock, patch

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    DevboxView,
    DevboxTunnelView,
    DevboxSnapshotView,
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
from runloop_api_client.pagination import (
    SyncDevboxesCursorIDPage,
    AsyncDevboxesCursorIDPage,
    SyncDiskSnapshotsCursorIDPage,
    AsyncDiskSnapshotsCursorIDPage,
)
from runloop_api_client._exceptions import RunloopError, APIStatusError
from runloop_api_client.lib.polling import PollingConfig, PollingTimeout
from runloop_api_client.types.shared.launch_parameters import LaunchParameters

# pyright: reportDeprecated=false

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
                }
            ],
            entrypoint="entrypoint",
            environment_variables={"foo": "string"},
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
            mounts=[
                {
                    "object_id": "object_id",
                    "object_path": "object_path",
                    "type": "object_mount",
                }
            ],
            name="name",
            repo_connection_id="repo_connection_id",
            secrets={"foo": "string"},
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
    def test_method_update(self, client: Runloop) -> None:
        devbox = client.devboxes.update(
            id="id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.update(
            id="id",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        devbox = client.devboxes.list()
        assert_matches_type(SyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.list(
            limit=0,
            starting_after="starting_after",
            status="provisioning",
        )
        assert_matches_type(SyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(SyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(SyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

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
    def test_method_create_tunnel(self, client: Runloop) -> None:
        devbox = client.devboxes.create_tunnel(
            id="id",
            port=0,
        )
        assert_matches_type(DevboxTunnelView, devbox, path=["response"])

    @parametrize
    def test_raw_response_create_tunnel(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.create_tunnel(
            id="id",
            port=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxTunnelView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_create_tunnel(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.create_tunnel(
            id="id",
            port=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxTunnelView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_tunnel(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.create_tunnel(
                id="",
                port=0,
            )

    @parametrize
    def test_method_delete_disk_snapshot(self, client: Runloop) -> None:
        devbox = client.devboxes.delete_disk_snapshot(
            "id",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_raw_response_delete_disk_snapshot(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.delete_disk_snapshot(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_streaming_response_delete_disk_snapshot(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.delete_disk_snapshot(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete_disk_snapshot(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.delete_disk_snapshot(
                "",
            )

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
    def test_method_execute(self, client: Runloop) -> None:
        devbox = client.devboxes.execute(
            id="id",
            command="command",
            command_id="command_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.execute(
            id="id",
            command="command",
            command_id="command_id",
            last_n="last_n",
            optimistic_timeout=0,
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.execute(
            id="id",
            command="command",
            command_id="command_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.execute(
            id="id",
            command="command",
            command_id="command_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.execute(
                id="",
                command="command",
                command_id="command_id",
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
            attach_stdin=True,
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
        with pytest.warns(DeprecationWarning):
            devbox = client.devboxes.execute_sync(
                id="id",
                command="command",
            )

        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_execute_sync_with_all_params(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            devbox = client.devboxes.execute_sync(
                id="id",
                command="command",
                attach_stdin=True,
                shell_name="shell_name",
            )

        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_execute_sync(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
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
        with pytest.warns(DeprecationWarning):
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
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                client.devboxes.with_raw_response.execute_sync(
                    id="",
                    command="command",
                )

    @parametrize
    def test_method_keep_alive(self, client: Runloop) -> None:
        devbox = client.devboxes.keep_alive(
            "id",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_raw_response_keep_alive(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.keep_alive(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_streaming_response_keep_alive(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.keep_alive(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_keep_alive(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.keep_alive(
                "",
            )

    @parametrize
    def test_method_list_disk_snapshots(self, client: Runloop) -> None:
        devbox = client.devboxes.list_disk_snapshots()
        assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

    @parametrize
    def test_method_list_disk_snapshots_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.list_disk_snapshots(
            devbox_id="devbox_id",
            limit=0,
            metadata_key="metadata[key]",
            metadata_key_in="metadata[key][in]",
            source_blueprint_id="source_blueprint_id",
            starting_after="starting_after",
        )
        assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

    @parametrize
    def test_raw_response_list_disk_snapshots(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.list_disk_snapshots()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

    @parametrize
    def test_streaming_response_list_disk_snapshots(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.list_disk_snapshots() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

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
    def test_method_remove_tunnel(self, client: Runloop) -> None:
        devbox = client.devboxes.remove_tunnel(
            id="id",
            port=0,
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_raw_response_remove_tunnel(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.remove_tunnel(
            id="id",
            port=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_streaming_response_remove_tunnel(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.remove_tunnel(
            id="id",
            port=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove_tunnel(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.remove_tunnel(
                id="",
                port=0,
            )

    @parametrize
    def test_method_resume(self, client: Runloop) -> None:
        devbox = client.devboxes.resume(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_raw_response_resume(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_resume(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_resume(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.resume(
                "",
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
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    def test_method_snapshot_disk_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.snapshot_disk(
            id="id",
            commit_message="commit_message",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    def test_raw_response_snapshot_disk(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.snapshot_disk(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_snapshot_disk(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.snapshot_disk(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_snapshot_disk(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.snapshot_disk(
                id="",
            )

    @parametrize
    def test_method_snapshot_disk_async(self, client: Runloop) -> None:
        devbox = client.devboxes.snapshot_disk_async(
            id="id",
        )
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    def test_method_snapshot_disk_async_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.snapshot_disk_async(
            id="id",
            commit_message="commit_message",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    def test_raw_response_snapshot_disk_async(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.snapshot_disk_async(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_snapshot_disk_async(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.snapshot_disk_async(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_snapshot_disk_async(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.snapshot_disk_async(
                id="",
            )

    @parametrize
    def test_method_suspend(self, client: Runloop) -> None:
        devbox = client.devboxes.suspend(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_raw_response_suspend(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.suspend(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_suspend(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.suspend(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_suspend(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.suspend(
                "",
            )

    @parametrize
    def test_method_upload_file(self, client: Runloop) -> None:
        devbox = client.devboxes.upload_file(
            id="id",
            path="path",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_method_upload_file_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.upload_file(
            id="id",
            path="path",
            file=b"raw file contents",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_raw_response_upload_file(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.upload_file(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    def test_streaming_response_upload_file(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.upload_file(
            id="id",
            path="path",
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
                path="path",
            )

    @parametrize
    def test_method_wait_for_command(self, client: Runloop) -> None:
        devbox = client.devboxes.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_method_wait_for_command_with_all_params(self, client: Runloop) -> None:
        devbox = client.devboxes.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
            last_n="last_n",
            timeout_seconds=0,
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_wait_for_command(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_wait_for_command(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_wait_for_command(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.with_raw_response.wait_for_command(
                execution_id="execution_id",
                devbox_id="",
                statuses=["queued"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.with_raw_response.wait_for_command(
                execution_id="",
                devbox_id="devbox_id",
                statuses=["queued"],
            )

    @parametrize
    def test_method_write_file_contents(self, client: Runloop) -> None:
        devbox = client.devboxes.write_file_contents(
            id="id",
            contents="contents",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_raw_response_write_file_contents(self, client: Runloop) -> None:
        response = client.devboxes.with_raw_response.write_file_contents(
            id="id",
            contents="contents",
            file_path="file_path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    def test_streaming_response_write_file_contents(self, client: Runloop) -> None:
        with client.devboxes.with_streaming_response.write_file_contents(
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
    def test_path_params_write_file_contents(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.with_raw_response.write_file_contents(
                id="",
                contents="contents",
                file_path="file_path",
            )

    # Polling method tests
    @parametrize
    def test_method_await_running_success(self, client: Runloop) -> None:
        """Test await_running with successful polling to running state"""

        # Mock the wait_for_status calls - first returns provisioning, then running
        mock_devbox_provisioning = DevboxView(
            id="test_id",
            status="provisioning",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.side_effect = [mock_devbox_provisioning, mock_devbox_running]

            result = client.devboxes.await_running("test_id")

            assert result.id == "test_id"
            assert result.status == "running"
            assert mock_post.call_count == 2

    @parametrize
    def test_method_await_running_immediate_success(self, client: Runloop) -> None:
        """Test await_running when devbox is already running"""

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_running

            result = client.devboxes.await_running("test_id")

            assert result.id == "test_id"
            assert result.status == "running"
            assert mock_post.call_count == 1

    @parametrize
    def test_method_await_running_failure_state(self, client: Runloop) -> None:
        """Test await_running when devbox enters failure state"""

        mock_devbox_failed = DevboxView(
            id="test_id",
            status="failure",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_failed

            with pytest.raises(RunloopError, match="Devbox entered non-running terminal state: failure"):
                client.devboxes.await_running("test_id")

    @parametrize
    def test_method_await_running_timeout_handling(self, client: Runloop) -> None:
        """Test await_running handles 408 timeouts correctly"""

        # Create a mock 408 response
        mock_response = Mock()
        mock_response.status_code = 408
        mock_408_error = APIStatusError("Request timeout", response=mock_response, body=None)

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            # First call raises 408, second call succeeds
            mock_post.side_effect = [mock_408_error, mock_devbox_running]

            result = client.devboxes.await_running("test_id")

            assert result.id == "test_id"
            assert result.status == "running"
            assert mock_post.call_count == 2

    @parametrize
    def test_method_await_running_other_error(self, client: Runloop) -> None:
        """Test await_running re-raises non-408 errors"""

        # Create a mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_500_error = APIStatusError("Internal server error", response=mock_response, body=None)

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.side_effect = mock_500_error

            with pytest.raises(APIStatusError, match="Internal server error"):
                client.devboxes.await_running("test_id")

    @parametrize
    def test_method_await_running_with_config(self, client: Runloop) -> None:
        """Test await_running with custom polling configuration"""

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_running

            result = client.devboxes.await_running("test_id", polling_config=config)

            assert result.id == "test_id"
            assert result.status == "running"

    @parametrize
    def test_method_await_running_polling_timeout(self, client: Runloop) -> None:
        """Test await_running raises PollingTimeout when max attempts exceeded"""

        mock_devbox_provisioning = DevboxView(
            id="test_id",
            status="provisioning",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_provisioning

            with pytest.raises(PollingTimeout):
                client.devboxes.await_running("test_id", polling_config=config)

    @parametrize
    def test_method_create_and_await_running_success(self, client: Runloop) -> None:
        """Test create_and_await_running successful flow"""

        mock_devbox_creating = DevboxView(
            id="test_id",
            status="provisioning",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "create") as mock_create:
            with patch.object(client.devboxes, "await_running") as mock_await:
                mock_create.return_value = mock_devbox_creating
                mock_await.return_value = mock_devbox_running

                result = client.devboxes.create_and_await_running(
                    name="test",
                )

                assert result.id == "test_id"
                assert result.status == "running"
                mock_create.assert_called_once()
                mock_await.assert_called_once_with("test_id", polling_config=None)

    @parametrize
    def test_method_create_and_await_running_with_config(self, client: Runloop) -> None:
        """Test create_and_await_running with custom polling configuration"""

        mock_devbox_creating = DevboxView(
            id="test_id",
            status="provisioning",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(client.devboxes, "create") as mock_create:
            with patch.object(client.devboxes, "await_running") as mock_await:
                mock_create.return_value = mock_devbox_creating
                mock_await.return_value = mock_devbox_running

                result = client.devboxes.create_and_await_running(
                    name="test",
                    polling_config=config,
                )

                assert result.id == "test_id"
                assert result.status == "running"
                mock_await.assert_called_once_with("test_id", polling_config=config)

    @parametrize
    def test_method_create_and_await_running_create_failure(self, client: Runloop) -> None:
        """Test create_and_await_running when create fails"""

        mock_response = Mock()
        mock_response.status_code = 400
        mock_error = APIStatusError("Bad request", response=mock_response, body=None)

        with patch.object(client.devboxes, "create") as mock_create:
            mock_create.side_effect = mock_error

            with pytest.raises(APIStatusError, match="Bad request"):
                client.devboxes.create_and_await_running(
                    name="test",
                )

    @parametrize
    def test_method_create_and_await_running_await_failure(self, client: Runloop) -> None:
        """Test create_and_await_running when await_running fails"""

        mock_devbox_creating = DevboxView(
            id="test_id",
            status="provisioning",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "create") as mock_create:
            with patch.object(client.devboxes, "await_running") as mock_await:
                mock_create.return_value = mock_devbox_creating
                mock_await.side_effect = RunloopError("Devbox entered non-running terminal state: failed")

                with pytest.raises(RunloopError, match="Devbox entered non-running terminal state: failed"):
                    client.devboxes.create_and_await_running(
                        name="test",
                    )

    @parametrize
    def test_method_await_suspended_success(self, client: Runloop) -> None:
        """Test await_suspended with successful polling to suspended state"""

        # Mock the wait_for_status calls - first returns running, then suspended
        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.side_effect = [mock_devbox_running, mock_devbox_suspended]

            result = client.devboxes.await_suspended("test_id")

            assert result.id == "test_id"
            assert result.status == "suspended"
            assert mock_post.call_count == 2

    @parametrize
    def test_method_await_suspended_immediate_success(self, client: Runloop) -> None:
        """Test await_suspended when devbox is already suspended"""

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_suspended

            result = client.devboxes.await_suspended("test_id")

            assert result.id == "test_id"
            assert result.status == "suspended"
            assert mock_post.call_count == 1

    @parametrize
    def test_method_await_suspended_failure_state(self, client: Runloop) -> None:
        """Test await_suspended when devbox enters failure state"""

        mock_devbox_failed = DevboxView(
            id="test_id",
            status="failure",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_failed

            with pytest.raises(RunloopError, match="Devbox entered non-suspended terminal state: failure"):
                client.devboxes.await_suspended("test_id")

    @parametrize
    def test_method_await_suspended_shutdown_state(self, client: Runloop) -> None:
        """Test await_suspended when devbox enters shutdown state"""

        mock_devbox_shutdown = DevboxView(
            id="test_id",
            status="shutdown",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_shutdown

            with pytest.raises(RunloopError, match="Devbox entered non-suspended terminal state: shutdown"):
                client.devboxes.await_suspended("test_id")

    @parametrize
    def test_method_await_suspended_timeout_handling(self, client: Runloop) -> None:
        """Test await_suspended handles 408 timeouts correctly"""

        # Create a mock 408 response
        mock_response = Mock()
        mock_response.status_code = 408
        mock_408_error = APIStatusError("Request timeout", response=mock_response, body=None)

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(client.devboxes, "_post") as mock_post:
            # First call raises 408, second call succeeds
            mock_post.side_effect = [mock_408_error, mock_devbox_suspended]

            result = client.devboxes.await_suspended("test_id")

            assert result.id == "test_id"
            assert result.status == "suspended"
            assert mock_post.call_count == 2

    @parametrize
    def test_method_await_suspended_other_error(self, client: Runloop) -> None:
        """Test await_suspended re-raises non-408 errors"""

        # Create a mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_500_error = APIStatusError("Internal server error", response=mock_response, body=None)

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.side_effect = mock_500_error

            with pytest.raises(APIStatusError, match="Internal server error"):
                client.devboxes.await_suspended("test_id")

    @parametrize
    def test_method_await_suspended_with_config(self, client: Runloop) -> None:
        """Test await_suspended with custom polling configuration"""

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_suspended

            result = client.devboxes.await_suspended("test_id", polling_config=config)

            assert result.id == "test_id"
            assert result.status == "suspended"

    @parametrize
    def test_method_await_suspended_polling_timeout(self, client: Runloop) -> None:
        """Test await_suspended raises PollingTimeout when max attempts exceeded"""

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_running

            with pytest.raises(PollingTimeout):
                client.devboxes.await_suspended("test_id", polling_config=config)


class TestAsyncDevboxes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

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
                }
            ],
            entrypoint="entrypoint",
            environment_variables={"foo": "string"},
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
            mounts=[
                {
                    "object_id": "object_id",
                    "object_path": "object_path",
                    "type": "object_mount",
                }
            ],
            name="name",
            repo_connection_id="repo_connection_id",
            secrets={"foo": "string"},
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
    async def test_method_update(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.update(
            id="id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.update(
            id="id",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.list()
        assert_matches_type(AsyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.list(
            limit=0,
            starting_after="starting_after",
            status="provisioning",
        )
        assert_matches_type(AsyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(AsyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(AsyncDevboxesCursorIDPage[DevboxView], devbox, path=["response"])

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
    async def test_method_create_tunnel(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.create_tunnel(
            id="id",
            port=0,
        )
        assert_matches_type(DevboxTunnelView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_create_tunnel(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.create_tunnel(
            id="id",
            port=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxTunnelView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_create_tunnel(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.create_tunnel(
            id="id",
            port=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxTunnelView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_tunnel(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.create_tunnel(
                id="",
                port=0,
            )

    @parametrize
    async def test_method_delete_disk_snapshot(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.delete_disk_snapshot(
            "id",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_raw_response_delete_disk_snapshot(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.delete_disk_snapshot(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_delete_disk_snapshot(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.delete_disk_snapshot(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete_disk_snapshot(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.delete_disk_snapshot(
                "",
            )

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
    async def test_method_execute(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute(
            id="id",
            command="command",
            command_id="command_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.execute(
            id="id",
            command="command",
            command_id="command_id",
            last_n="last_n",
            optimistic_timeout=0,
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.execute(
            id="id",
            command="command",
            command_id="command_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.execute(
            id="id",
            command="command",
            command_id="command_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.execute(
                id="",
                command="command",
                command_id="command_id",
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
            attach_stdin=True,
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
        with pytest.warns(DeprecationWarning):
            devbox = await async_client.devboxes.execute_sync(
                id="id",
                command="command",
            )

        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_execute_sync_with_all_params(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            devbox = await async_client.devboxes.execute_sync(
                id="id",
                command="command",
                attach_stdin=True,
                shell_name="shell_name",
            )

        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
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
        with pytest.warns(DeprecationWarning):
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
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                await async_client.devboxes.with_raw_response.execute_sync(
                    id="",
                    command="command",
                )

    @parametrize
    async def test_method_keep_alive(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.keep_alive(
            "id",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_raw_response_keep_alive(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.keep_alive(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_keep_alive(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.keep_alive(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_keep_alive(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.keep_alive(
                "",
            )

    @parametrize
    async def test_method_list_disk_snapshots(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.list_disk_snapshots()
        assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

    @parametrize
    async def test_method_list_disk_snapshots_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.list_disk_snapshots(
            devbox_id="devbox_id",
            limit=0,
            metadata_key="metadata[key]",
            metadata_key_in="metadata[key][in]",
            source_blueprint_id="source_blueprint_id",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

    @parametrize
    async def test_raw_response_list_disk_snapshots(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.list_disk_snapshots()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

    @parametrize
    async def test_streaming_response_list_disk_snapshots(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.list_disk_snapshots() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView], devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

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
    async def test_method_remove_tunnel(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.remove_tunnel(
            id="id",
            port=0,
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_raw_response_remove_tunnel(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.remove_tunnel(
            id="id",
            port=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_remove_tunnel(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.remove_tunnel(
            id="id",
            port=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(object, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove_tunnel(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.remove_tunnel(
                id="",
                port=0,
            )

    @parametrize
    async def test_method_resume(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.resume(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_resume(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_resume(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_resume(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.resume(
                "",
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
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    async def test_method_snapshot_disk_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.snapshot_disk(
            id="id",
            commit_message="commit_message",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.snapshot_disk(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.snapshot_disk(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_snapshot_disk(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.snapshot_disk(
                id="",
            )

    @parametrize
    async def test_method_snapshot_disk_async(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.snapshot_disk_async(
            id="id",
        )
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    async def test_method_snapshot_disk_async_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.snapshot_disk_async(
            id="id",
            commit_message="commit_message",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_snapshot_disk_async(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.snapshot_disk_async(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_snapshot_disk_async(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.snapshot_disk_async(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxSnapshotView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_snapshot_disk_async(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.snapshot_disk_async(
                id="",
            )

    @parametrize
    async def test_method_suspend(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.suspend(
            "id",
        )
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_suspend(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.suspend(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_suspend(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.suspend(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_suspend(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.suspend(
                "",
            )

    @parametrize
    async def test_method_upload_file(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.upload_file(
            id="id",
            path="path",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_method_upload_file_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.upload_file(
            id="id",
            path="path",
            file=b"raw file contents",
        )
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_raw_response_upload_file(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.upload_file(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(object, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_upload_file(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.upload_file(
            id="id",
            path="path",
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
                path="path",
            )

    @parametrize
    async def test_method_wait_for_command(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_method_wait_for_command_with_all_params(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
            last_n="last_n",
            timeout_seconds=0,
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_wait_for_command(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_wait_for_command(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.wait_for_command(
            execution_id="execution_id",
            devbox_id="devbox_id",
            statuses=["queued"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            devbox = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, devbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_wait_for_command(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.with_raw_response.wait_for_command(
                execution_id="execution_id",
                devbox_id="",
                statuses=["queued"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.with_raw_response.wait_for_command(
                execution_id="",
                devbox_id="devbox_id",
                statuses=["queued"],
            )

    @parametrize
    async def test_method_write_file_contents(self, async_client: AsyncRunloop) -> None:
        devbox = await async_client.devboxes.write_file_contents(
            id="id",
            contents="contents",
            file_path="file_path",
        )
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_raw_response_write_file_contents(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.with_raw_response.write_file_contents(
            id="id",
            contents="contents",
            file_path="file_path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        devbox = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, devbox, path=["response"])

    @parametrize
    async def test_streaming_response_write_file_contents(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.with_streaming_response.write_file_contents(
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
    async def test_path_params_write_file_contents(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.with_raw_response.write_file_contents(
                id="",
                contents="contents",
                file_path="file_path",
            )

    # Polling method tests
    @parametrize
    async def test_method_await_suspended_success(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended with successful polling to suspended state"""

        # Mock the wait_for_status calls - first returns running, then suspended
        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.side_effect = [mock_devbox_running, mock_devbox_suspended]

            result = await async_client.devboxes.await_suspended("test_id")

            assert result.id == "test_id"
            assert result.status == "suspended"
            assert mock_post.call_count == 2

    @parametrize
    async def test_method_await_suspended_immediate_success(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended when devbox is already suspended"""

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_suspended

            result = await async_client.devboxes.await_suspended("test_id")

            assert result.id == "test_id"
            assert result.status == "suspended"
            assert mock_post.call_count == 1

    @parametrize
    async def test_method_await_suspended_failure_state(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended when devbox enters failure state"""

        mock_devbox_failed = DevboxView(
            id="test_id",
            status="failure",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_failed

            with pytest.raises(RunloopError, match="Devbox entered non-suspended terminal state: failure"):
                await async_client.devboxes.await_suspended("test_id")

    @parametrize
    async def test_method_await_suspended_shutdown_state(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended when devbox enters shutdown state"""

        mock_devbox_shutdown = DevboxView(
            id="test_id",
            status="shutdown",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_shutdown

            with pytest.raises(RunloopError, match="Devbox entered non-suspended terminal state: shutdown"):
                await async_client.devboxes.await_suspended("test_id")

    @parametrize
    async def test_method_await_suspended_timeout_handling(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended handles 408 timeouts correctly"""

        # Create a mock 408 response
        mock_response = Mock()
        mock_response.status_code = 408
        mock_408_error = APIStatusError("Request timeout", response=mock_response, body=None)

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        with patch.object(async_client.devboxes, "_post") as mock_post:
            # First call raises 408, second call succeeds
            mock_post.side_effect = [mock_408_error, mock_devbox_suspended]

            result = await async_client.devboxes.await_suspended("test_id")

            assert result.id == "test_id"
            assert result.status == "suspended"
            assert mock_post.call_count == 2

    @parametrize
    async def test_method_await_suspended_other_error(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended re-raises non-408 errors"""

        # Create a mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_500_error = APIStatusError("Internal server error", response=mock_response, body=None)

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.side_effect = mock_500_error

            with pytest.raises(APIStatusError, match="Internal server error"):
                await async_client.devboxes.await_suspended("test_id")

    @parametrize
    async def test_method_await_suspended_with_config(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended with custom polling configuration"""

        mock_devbox_suspended = DevboxView(
            id="test_id",
            status="suspended",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_suspended

            result = await async_client.devboxes.await_suspended("test_id", polling_config=config)

            assert result.id == "test_id"
            assert result.status == "suspended"

    @parametrize
    async def test_method_await_suspended_polling_timeout(self, async_client: AsyncRunloop) -> None:
        """Test await_suspended raises PollingTimeout when max attempts exceeded"""

        mock_devbox_running = DevboxView(
            id="test_id",
            status="running",
            capabilities=[],
            create_time_ms=1234567890,
            launch_parameters=LaunchParameters(resource_size_request="X_SMALL"),
            metadata={},
            state_transitions=[],
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(async_client.devboxes, "_post") as mock_post:
            mock_post.return_value = mock_devbox_running

            with pytest.raises(PollingTimeout):
                await async_client.devboxes.await_suspended("test_id", polling_config=config)
