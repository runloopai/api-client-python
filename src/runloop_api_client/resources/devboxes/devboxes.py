# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Mapping, Iterable, cast

import httpx

from .logs import (
    LogsResource,
    AsyncLogsResource,
    LogsResourceWithRawResponse,
    AsyncLogsResourceWithRawResponse,
    LogsResourceWithStreamingResponse,
    AsyncLogsResourceWithStreamingResponse,
)
from ...types import (
    devbox_list_params,
    devbox_create_params,
    devbox_write_file_params,
    devbox_upload_file_params,
    devbox_execute_sync_params,
    devbox_download_file_params,
    devbox_execute_async_params,
    devbox_snapshot_disk_params,
    devbox_disk_snapshots_params,
    devbox_read_file_contents_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven, FileTypes
from ..._utils import (
    extract_files,
    maybe_transform,
    deepcopy_minimal,
    async_maybe_transform,
)
from ..._compat import cached_property
from .executions import (
    ExecutionsResource,
    AsyncExecutionsResource,
    ExecutionsResourceWithRawResponse,
    AsyncExecutionsResourceWithRawResponse,
    ExecutionsResourceWithStreamingResponse,
    AsyncExecutionsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.devbox_view import DevboxView
from ...types.devbox_list_view import DevboxListView
from ...types.devbox_snapshot_list_view import DevboxSnapshotListView
from ...types.code_mount_parameters_param import CodeMountParametersParam
from ...types.devbox_execution_detail_view import DevboxExecutionDetailView
from ...types.devbox_create_ssh_key_response import DevboxCreateSSHKeyResponse
from ...types.shared_params.launch_parameters import LaunchParameters
from ...types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView

__all__ = ["DevboxesResource", "AsyncDevboxesResource"]


class DevboxesResource(SyncAPIResource):
    @cached_property
    def logs(self) -> LogsResource:
        return LogsResource(self._client)

    @cached_property
    def executions(self) -> ExecutionsResource:
        return ExecutionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DevboxesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return DevboxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DevboxesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return DevboxesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        blueprint_id: str | NotGiven = NOT_GIVEN,
        blueprint_name: str | NotGiven = NOT_GIVEN,
        code_mounts: Iterable[CodeMountParametersParam] | NotGiven = NOT_GIVEN,
        entrypoint: str | NotGiven = NOT_GIVEN,
        environment_variables: Dict[str, str] | NotGiven = NOT_GIVEN,
        file_mounts: Dict[str, str] | NotGiven = NOT_GIVEN,
        launch_parameters: LaunchParameters | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        prebuilt: str | NotGiven = NOT_GIVEN,
        setup_commands: List[str] | NotGiven = NOT_GIVEN,
        snapshot_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxView:
        """Create a Devbox with the specified configuration.

        The Devbox will be created in
        the 'pending' state and will transition to 'running' once it is ready.

        Args:
          blueprint_id: (Optional) Blueprint to use for the Devbox. If none set, the Devbox will be
              created with the default Runloop Devbox image.

          blueprint_name: (Optional) Name of Blueprint to use for the Devbox. When set, this will load the
              latest successfully built Blueprint with the given name.

          code_mounts: A list of code mounts to be included in the Devbox.

          entrypoint: (Optional) When specified, the Devbox will run this script as its main
              executable. The devbox lifecycle will be bound to entrypoint, shutting down when
              the process is complete.

          environment_variables: (Optional) Environment variables used to configure your Devbox.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure the resources and launch time behavior of the Devbox.

          metadata: User defined metadata to attach to the devbox for organization.

          name: (Optional) A user specified name to give the Devbox.

          prebuilt: Reference to prebuilt Blueprint.

          setup_commands: (Optional) List of commands needed to set up your Devbox. Examples might include
              fetching a tool or building your dependencies. Runloop will look optimize these
              steps for you.

          snapshot_id: Snapshot ID to use for the Devbox.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/devboxes",
            body=maybe_transform(
                {
                    "blueprint_id": blueprint_id,
                    "blueprint_name": blueprint_name,
                    "code_mounts": code_mounts,
                    "entrypoint": entrypoint,
                    "environment_variables": environment_variables,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "metadata": metadata,
                    "name": name,
                    "prebuilt": prebuilt,
                    "setup_commands": setup_commands,
                    "snapshot_id": snapshot_id,
                },
                devbox_create_params.DevboxCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxView,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxView:
        """Get a devbox by id.

        If the devbox does not exist, a 404 is returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/devboxes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxView,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxListView:
        """List all devboxes or filter by status.

        If no status is provided, all devboxes
        are returned.

        Args:
          limit: Page Limit

          starting_after: Load the next page starting after the given token.

          status: Filter by status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/devboxes",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                        "status": status,
                    },
                    devbox_list_params.DevboxListParams,
                ),
            ),
            cast_to=DevboxListView,
        )

    def create_ssh_key(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxCreateSSHKeyResponse:
        """
        Create an SSH key for a devbox by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/create_ssh_key",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxCreateSSHKeyResponse,
        )

    def disk_snapshots(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxSnapshotListView:
        """
        List all snapshots of a devbox by id.

        Args:
          limit: Page Limit

          starting_after: Load the next page starting after the given token.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/devboxes/disk_snapshots",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    devbox_disk_snapshots_params.DevboxDiskSnapshotsParams,
                ),
            ),
            cast_to=DevboxSnapshotListView,
        )

    def download_file(
        self,
        id: str,
        *,
        path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Download file contents to a file at path on the Devbox.

        Args:
          path: The path on the devbox to read the file

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return self._post(
            f"/v1/devboxes/{id}/download_file",
            body=maybe_transform({"path": path}, devbox_download_file_params.DevboxDownloadFileParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def execute_async(
        self,
        id: str,
        *,
        command: str,
        shell_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Asynchronously execute a command on a devbox

        Args:
          command: The command to execute on the Devbox.

          shell_name: Which named shell to run the command in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/execute_async",
            body=maybe_transform(
                {
                    "command": command,
                    "shell_name": shell_name,
                },
                devbox_execute_async_params.DevboxExecuteAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    def execute_sync(
        self,
        id: str,
        *,
        command: str,
        shell_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxExecutionDetailView:
        """
        Synchronously execute a command on a devbox

        Args:
          command: The command to execute on the Devbox.

          shell_name: Which named shell to run the command in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/execute_sync",
            body=maybe_transform(
                {
                    "command": command,
                    "shell_name": shell_name,
                },
                devbox_execute_sync_params.DevboxExecuteSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxExecutionDetailView,
        )

    def read_file_contents(
        self,
        id: str,
        *,
        file_path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Read file contents from a file on given Devbox.

        Args:
          file_path: The path of the file to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._post(
            f"/v1/devboxes/{id}/read_file_contents",
            body=maybe_transform(
                {"file_path": file_path}, devbox_read_file_contents_params.DevboxReadFileContentsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    def shutdown(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxView:
        """Shutdown a running devbox by id.

        This will take the devbox out of service.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/shutdown",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxView,
        )

    def snapshot_disk(
        self,
        id: str,
        *,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a filesystem snapshot of a devbox with the specified name and metadata.

        Args:
          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/v1/devboxes/{id}/snapshot_disk",
            body=maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                devbox_snapshot_disk_params.DevboxSnapshotDiskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def upload_file(
        self,
        id: str,
        *,
        file: FileTypes | NotGiven = NOT_GIVEN,
        path: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Upload file contents to a file at path on the Devbox.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        body = deepcopy_minimal(
            {
                "file": file,
                "path": path,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            f"/v1/devboxes/{id}/upload_file",
            body=maybe_transform(body, devbox_upload_file_params.DevboxUploadFileParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def write_file(
        self,
        id: str,
        *,
        contents: str,
        file_path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxExecutionDetailView:
        """
        Write contents to a file at path on the Devbox.

        Args:
          contents: The contents to write to file.

          file_path: The path of the file to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/write_file",
            body=maybe_transform(
                {
                    "contents": contents,
                    "file_path": file_path,
                },
                devbox_write_file_params.DevboxWriteFileParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxExecutionDetailView,
        )


class AsyncDevboxesResource(AsyncAPIResource):
    @cached_property
    def logs(self) -> AsyncLogsResource:
        return AsyncLogsResource(self._client)

    @cached_property
    def executions(self) -> AsyncExecutionsResource:
        return AsyncExecutionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDevboxesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDevboxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDevboxesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncDevboxesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        blueprint_id: str | NotGiven = NOT_GIVEN,
        blueprint_name: str | NotGiven = NOT_GIVEN,
        code_mounts: Iterable[CodeMountParametersParam] | NotGiven = NOT_GIVEN,
        entrypoint: str | NotGiven = NOT_GIVEN,
        environment_variables: Dict[str, str] | NotGiven = NOT_GIVEN,
        file_mounts: Dict[str, str] | NotGiven = NOT_GIVEN,
        launch_parameters: LaunchParameters | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        prebuilt: str | NotGiven = NOT_GIVEN,
        setup_commands: List[str] | NotGiven = NOT_GIVEN,
        snapshot_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxView:
        """Create a Devbox with the specified configuration.

        The Devbox will be created in
        the 'pending' state and will transition to 'running' once it is ready.

        Args:
          blueprint_id: (Optional) Blueprint to use for the Devbox. If none set, the Devbox will be
              created with the default Runloop Devbox image.

          blueprint_name: (Optional) Name of Blueprint to use for the Devbox. When set, this will load the
              latest successfully built Blueprint with the given name.

          code_mounts: A list of code mounts to be included in the Devbox.

          entrypoint: (Optional) When specified, the Devbox will run this script as its main
              executable. The devbox lifecycle will be bound to entrypoint, shutting down when
              the process is complete.

          environment_variables: (Optional) Environment variables used to configure your Devbox.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure the resources and launch time behavior of the Devbox.

          metadata: User defined metadata to attach to the devbox for organization.

          name: (Optional) A user specified name to give the Devbox.

          prebuilt: Reference to prebuilt Blueprint.

          setup_commands: (Optional) List of commands needed to set up your Devbox. Examples might include
              fetching a tool or building your dependencies. Runloop will look optimize these
              steps for you.

          snapshot_id: Snapshot ID to use for the Devbox.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/devboxes",
            body=await async_maybe_transform(
                {
                    "blueprint_id": blueprint_id,
                    "blueprint_name": blueprint_name,
                    "code_mounts": code_mounts,
                    "entrypoint": entrypoint,
                    "environment_variables": environment_variables,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "metadata": metadata,
                    "name": name,
                    "prebuilt": prebuilt,
                    "setup_commands": setup_commands,
                    "snapshot_id": snapshot_id,
                },
                devbox_create_params.DevboxCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxView,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxView:
        """Get a devbox by id.

        If the devbox does not exist, a 404 is returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/devboxes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxView,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxListView:
        """List all devboxes or filter by status.

        If no status is provided, all devboxes
        are returned.

        Args:
          limit: Page Limit

          starting_after: Load the next page starting after the given token.

          status: Filter by status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/devboxes",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                        "status": status,
                    },
                    devbox_list_params.DevboxListParams,
                ),
            ),
            cast_to=DevboxListView,
        )

    async def create_ssh_key(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxCreateSSHKeyResponse:
        """
        Create an SSH key for a devbox by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/create_ssh_key",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxCreateSSHKeyResponse,
        )

    async def disk_snapshots(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxSnapshotListView:
        """
        List all snapshots of a devbox by id.

        Args:
          limit: Page Limit

          starting_after: Load the next page starting after the given token.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/devboxes/disk_snapshots",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    devbox_disk_snapshots_params.DevboxDiskSnapshotsParams,
                ),
            ),
            cast_to=DevboxSnapshotListView,
        )

    async def download_file(
        self,
        id: str,
        *,
        path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Download file contents to a file at path on the Devbox.

        Args:
          path: The path on the devbox to read the file

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return await self._post(
            f"/v1/devboxes/{id}/download_file",
            body=await async_maybe_transform({"path": path}, devbox_download_file_params.DevboxDownloadFileParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def execute_async(
        self,
        id: str,
        *,
        command: str,
        shell_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Asynchronously execute a command on a devbox

        Args:
          command: The command to execute on the Devbox.

          shell_name: Which named shell to run the command in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/execute_async",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "shell_name": shell_name,
                },
                devbox_execute_async_params.DevboxExecuteAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    async def execute_sync(
        self,
        id: str,
        *,
        command: str,
        shell_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxExecutionDetailView:
        """
        Synchronously execute a command on a devbox

        Args:
          command: The command to execute on the Devbox.

          shell_name: Which named shell to run the command in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/execute_sync",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "shell_name": shell_name,
                },
                devbox_execute_sync_params.DevboxExecuteSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxExecutionDetailView,
        )

    async def read_file_contents(
        self,
        id: str,
        *,
        file_path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Read file contents from a file on given Devbox.

        Args:
          file_path: The path of the file to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._post(
            f"/v1/devboxes/{id}/read_file_contents",
            body=await async_maybe_transform(
                {"file_path": file_path}, devbox_read_file_contents_params.DevboxReadFileContentsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    async def shutdown(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxView:
        """Shutdown a running devbox by id.

        This will take the devbox out of service.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/shutdown",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxView,
        )

    async def snapshot_disk(
        self,
        id: str,
        *,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a filesystem snapshot of a devbox with the specified name and metadata.

        Args:
          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/v1/devboxes/{id}/snapshot_disk",
            body=await async_maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                devbox_snapshot_disk_params.DevboxSnapshotDiskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def upload_file(
        self,
        id: str,
        *,
        file: FileTypes | NotGiven = NOT_GIVEN,
        path: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Upload file contents to a file at path on the Devbox.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        body = deepcopy_minimal(
            {
                "file": file,
                "path": path,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            f"/v1/devboxes/{id}/upload_file",
            body=await async_maybe_transform(body, devbox_upload_file_params.DevboxUploadFileParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def write_file(
        self,
        id: str,
        *,
        contents: str,
        file_path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DevboxExecutionDetailView:
        """
        Write contents to a file at path on the Devbox.

        Args:
          contents: The contents to write to file.

          file_path: The path of the file to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/write_file",
            body=await async_maybe_transform(
                {
                    "contents": contents,
                    "file_path": file_path,
                },
                devbox_write_file_params.DevboxWriteFileParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxExecutionDetailView,
        )


class DevboxesResourceWithRawResponse:
    def __init__(self, devboxes: DevboxesResource) -> None:
        self._devboxes = devboxes

        self.create = to_raw_response_wrapper(
            devboxes.create,
        )
        self.retrieve = to_raw_response_wrapper(
            devboxes.retrieve,
        )
        self.list = to_raw_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = to_raw_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.disk_snapshots = to_raw_response_wrapper(
            devboxes.disk_snapshots,
        )
        self.download_file = to_custom_raw_response_wrapper(
            devboxes.download_file,
            BinaryAPIResponse,
        )
        self.execute_async = to_raw_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = to_raw_response_wrapper(
            devboxes.execute_sync,
        )
        self.read_file_contents = to_raw_response_wrapper(
            devboxes.read_file_contents,
        )
        self.shutdown = to_raw_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = to_raw_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.upload_file = to_raw_response_wrapper(
            devboxes.upload_file,
        )
        self.write_file = to_raw_response_wrapper(
            devboxes.write_file,
        )

    @cached_property
    def logs(self) -> LogsResourceWithRawResponse:
        return LogsResourceWithRawResponse(self._devboxes.logs)

    @cached_property
    def executions(self) -> ExecutionsResourceWithRawResponse:
        return ExecutionsResourceWithRawResponse(self._devboxes.executions)


class AsyncDevboxesResourceWithRawResponse:
    def __init__(self, devboxes: AsyncDevboxesResource) -> None:
        self._devboxes = devboxes

        self.create = async_to_raw_response_wrapper(
            devboxes.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            devboxes.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = async_to_raw_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.disk_snapshots = async_to_raw_response_wrapper(
            devboxes.disk_snapshots,
        )
        self.download_file = async_to_custom_raw_response_wrapper(
            devboxes.download_file,
            AsyncBinaryAPIResponse,
        )
        self.execute_async = async_to_raw_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = async_to_raw_response_wrapper(
            devboxes.execute_sync,
        )
        self.read_file_contents = async_to_raw_response_wrapper(
            devboxes.read_file_contents,
        )
        self.shutdown = async_to_raw_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = async_to_raw_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.upload_file = async_to_raw_response_wrapper(
            devboxes.upload_file,
        )
        self.write_file = async_to_raw_response_wrapper(
            devboxes.write_file,
        )

    @cached_property
    def logs(self) -> AsyncLogsResourceWithRawResponse:
        return AsyncLogsResourceWithRawResponse(self._devboxes.logs)

    @cached_property
    def executions(self) -> AsyncExecutionsResourceWithRawResponse:
        return AsyncExecutionsResourceWithRawResponse(self._devboxes.executions)


class DevboxesResourceWithStreamingResponse:
    def __init__(self, devboxes: DevboxesResource) -> None:
        self._devboxes = devboxes

        self.create = to_streamed_response_wrapper(
            devboxes.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            devboxes.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = to_streamed_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.disk_snapshots = to_streamed_response_wrapper(
            devboxes.disk_snapshots,
        )
        self.download_file = to_custom_streamed_response_wrapper(
            devboxes.download_file,
            StreamedBinaryAPIResponse,
        )
        self.execute_async = to_streamed_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = to_streamed_response_wrapper(
            devboxes.execute_sync,
        )
        self.read_file_contents = to_streamed_response_wrapper(
            devboxes.read_file_contents,
        )
        self.shutdown = to_streamed_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = to_streamed_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.upload_file = to_streamed_response_wrapper(
            devboxes.upload_file,
        )
        self.write_file = to_streamed_response_wrapper(
            devboxes.write_file,
        )

    @cached_property
    def logs(self) -> LogsResourceWithStreamingResponse:
        return LogsResourceWithStreamingResponse(self._devboxes.logs)

    @cached_property
    def executions(self) -> ExecutionsResourceWithStreamingResponse:
        return ExecutionsResourceWithStreamingResponse(self._devboxes.executions)


class AsyncDevboxesResourceWithStreamingResponse:
    def __init__(self, devboxes: AsyncDevboxesResource) -> None:
        self._devboxes = devboxes

        self.create = async_to_streamed_response_wrapper(
            devboxes.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            devboxes.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = async_to_streamed_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.disk_snapshots = async_to_streamed_response_wrapper(
            devboxes.disk_snapshots,
        )
        self.download_file = async_to_custom_streamed_response_wrapper(
            devboxes.download_file,
            AsyncStreamedBinaryAPIResponse,
        )
        self.execute_async = async_to_streamed_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = async_to_streamed_response_wrapper(
            devboxes.execute_sync,
        )
        self.read_file_contents = async_to_streamed_response_wrapper(
            devboxes.read_file_contents,
        )
        self.shutdown = async_to_streamed_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = async_to_streamed_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.upload_file = async_to_streamed_response_wrapper(
            devboxes.upload_file,
        )
        self.write_file = async_to_streamed_response_wrapper(
            devboxes.write_file,
        )

    @cached_property
    def logs(self) -> AsyncLogsResourceWithStreamingResponse:
        return AsyncLogsResourceWithStreamingResponse(self._devboxes.logs)

    @cached_property
    def executions(self) -> AsyncExecutionsResourceWithStreamingResponse:
        return AsyncExecutionsResourceWithStreamingResponse(self._devboxes.executions)
