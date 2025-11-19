# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Dict, List, Mapping, Iterable, Optional, TypedDict, cast
from typing_extensions import Literal

import httpx

# uuid_utils is not typed
from uuid_utils import uuid7  # type: ignore

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
    devbox_update_params,
    devbox_execute_params,
    devbox_upload_file_params,
    devbox_execute_sync_params,
    devbox_create_tunnel_params,
    devbox_download_file_params,
    devbox_execute_async_params,
    devbox_remove_tunnel_params,
    devbox_snapshot_disk_params,
    devbox_wait_for_command_params,
    devbox_read_file_contents_params,
    devbox_list_disk_snapshots_params,
    devbox_snapshot_disk_async_params,
    devbox_write_file_contents_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ..._utils import is_given, extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .browsers import (
    BrowsersResource,
    AsyncBrowsersResource,
    BrowsersResourceWithRawResponse,
    AsyncBrowsersResourceWithRawResponse,
    BrowsersResourceWithStreamingResponse,
    AsyncBrowsersResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .computers import (
    ComputersResource,
    AsyncComputersResource,
    ComputersResourceWithRawResponse,
    AsyncComputersResourceWithRawResponse,
    ComputersResourceWithStreamingResponse,
    AsyncComputersResourceWithStreamingResponse,
)
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
from ..._constants import DEFAULT_TIMEOUT
from ...pagination import (
    SyncDevboxesCursorIDPage,
    AsyncDevboxesCursorIDPage,
    SyncDiskSnapshotsCursorIDPage,
    AsyncDiskSnapshotsCursorIDPage,
)
from ..._exceptions import RunloopError, APIStatusError, APITimeoutError
from ...lib.polling import PollingConfig, poll_until
from ..._base_client import AsyncPaginator, make_request_options
from .disk_snapshots import (
    DiskSnapshotsResource,
    AsyncDiskSnapshotsResource,
    DiskSnapshotsResourceWithRawResponse,
    AsyncDiskSnapshotsResourceWithRawResponse,
    DiskSnapshotsResourceWithStreamingResponse,
    AsyncDiskSnapshotsResourceWithStreamingResponse,
)
from ...lib.polling_async import async_poll_until
from ...types.devbox_view import DevboxView
from ...types.devbox_tunnel_view import DevboxTunnelView
from ...types.shared_params.mount import Mount
from ...types.devbox_snapshot_view import DevboxSnapshotView
from ...types.shared.launch_parameters import LaunchParameters as SharedLaunchParameters
from ...types.devbox_execution_detail_view import DevboxExecutionDetailView
from ...types.devbox_create_ssh_key_response import DevboxCreateSSHKeyResponse
from ...types.shared_params.launch_parameters import LaunchParameters
from ...types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView
from ...types.shared_params.code_mount_parameters import CodeMountParameters

__all__ = ["DevboxesResource", "AsyncDevboxesResource", "DevboxRequestArgs"]

DEVBOX_BOOTING_STATES = frozenset(("provisioning", "initializing"))
DEVBOX_TERMINAL_STATES = frozenset(("suspended", "failure", "shutdown"))


# Type for request arguments that combine polling config with additional request options
class DevboxRequestArgs(TypedDict, total=False):
    polling_config: PollingConfig | None
    extra_headers: Headers | None
    extra_query: Query | None
    extra_body: Body | None
    timeout: float | httpx.Timeout | None | NotGiven


def placeholder_devbox_view(id: str) -> DevboxView:
    return DevboxView(
        id=id,
        status="provisioning",
        capabilities=[],
        create_time_ms=0,
        launch_parameters=SharedLaunchParameters(),
        metadata={},
        state_transitions=[],
    )


class DevboxesResource(SyncAPIResource):
    @cached_property
    def disk_snapshots(self) -> DiskSnapshotsResource:
        return DiskSnapshotsResource(self._client)

    @cached_property
    def browsers(self) -> BrowsersResource:
        return BrowsersResource(self._client)

    @cached_property
    def computers(self) -> ComputersResource:
        return ComputersResource(self._client)

    @cached_property
    def logs(self) -> LogsResource:
        return LogsResource(self._client)

    @cached_property
    def executions(self) -> ExecutionsResource:
        return ExecutionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DevboxesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
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
        blueprint_id: Optional[str] | Omit = omit,
        blueprint_name: Optional[str] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        snapshot_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Create a Devbox and begin the boot process.

        The Devbox will initially launch in
        the 'provisioning' state while Runloop allocates the necessary infrastructure.
        It will transition to the 'initializing' state while the booted Devbox runs any
        Runloop or user defined set up scripts. Finally, the Devbox will transition to
        the 'running' state when it is ready for use.

        Args:
          blueprint_id: Blueprint ID to use for the Devbox. If none set, the Devbox will be created with
              the default Runloop Devbox image. Only one of (Snapshot ID, Blueprint ID,
              Blueprint name) should be specified.

          blueprint_name: Name of Blueprint to use for the Devbox. When set, this will load the latest
              successfully built Blueprint with the given name. Only one of (Snapshot ID,
              Blueprint ID, Blueprint name) should be specified.

          code_mounts: A list of code mounts to be included in the Devbox.

          entrypoint: (Optional) When specified, the Devbox will run this script as its main
              executable. The devbox lifecycle will be bound to entrypoint, shutting down when
              the process is complete.

          environment_variables: (Optional) Environment variables used to configure your Devbox.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure the resources and launch time behavior of the Devbox.

          metadata: User defined metadata to attach to the devbox for organization.

          mounts: A list of file system mounts to be included in the Devbox.

          name: (Optional) A user specified name to give the Devbox.

          repo_connection_id: Repository connection id the devbox should source its base image from.

          secrets: (Optional) Map of environment variable names to secret names. The secret values
              will be securely injected as environment variables in the Devbox. Example:
              {"DB_PASS": "DATABASE_PASSWORD"} sets environment variable 'DB_PASS' to the
              value of secret 'DATABASE_PASSWORD'.

          snapshot_id: Snapshot ID to use for the Devbox. Only one of (Snapshot ID, Blueprint ID,
              Blueprint name) should be specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
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
                    "mounts": mounts,
                    "name": name,
                    "repo_connection_id": repo_connection_id,
                    "secrets": secrets,
                    "snapshot_id": snapshot_id,
                },
                devbox_create_params.DevboxCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DevboxView:
        """
        Get the latest details and status of a Devbox.

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

    def update(
        self,
        id: str,
        *,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """
        Updates a devbox by doing a complete update the existing name,metadata fields.
        It does not patch partial values.

        Args:
          metadata: User defined metadata to attach to the devbox for organization.

          name: (Optional) A user specified name to give the Devbox.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}",
            body=maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                devbox_update_params.DevboxUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
        )

    def await_running(
        self,
        id: str,
        *,
        # Use polling_config to configure the "long" polling behavior.
        polling_config: PollingConfig | None = None,
    ) -> DevboxView:
        """Wait for a devbox to be in running state.

        Args:
            id: The ID of the devbox to wait for
            config: Optional polling configuration
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds

        Returns:
            The devbox in running state

        Raises:
            PollingTimeout: If polling times out before devbox is running
            RunloopError: If devbox enters a non-running terminal state
        """

        def wait_for_devbox_status() -> DevboxView:
            # This wait_for_status endpoint polls the devbox status for 10 seconds until it reaches either running or failure.
            # If it's neither, it will throw an error.
            return self._post(
                f"/v1/devboxes/{id}/wait_for_status",
                body={"statuses": ["running", "failure", "shutdown"]},
                cast_to=DevboxView,
            )

        def handle_timeout_error(error: Exception) -> DevboxView:
            # Handle timeout errors by returning current devbox state to continue polling
            if isinstance(error, APITimeoutError) or (
                isinstance(error, APIStatusError) and error.response.status_code == 408
            ):
                # Return a placeholder result to continue polling
                return placeholder_devbox_view(id)

            # Re-raise other errors to stop polling
            raise error

        def is_done_booting(devbox: DevboxView) -> bool:
            return devbox.status not in DEVBOX_BOOTING_STATES

        devbox = poll_until(wait_for_devbox_status, is_done_booting, polling_config, handle_timeout_error)

        if devbox.status != "running":
            raise RunloopError(f"Devbox entered non-running terminal state: {devbox.status}")

        return devbox

    def await_suspended(
        self,
        id: str,
        *,
        polling_config: PollingConfig | None = None,
    ) -> DevboxView:
        """Wait for a devbox to reach the suspended state.

        Args:
            id: The ID of the devbox to wait for.
            polling_config: Optional polling configuration.

        Returns:
            The devbox in the suspended state.

        Raises:
            PollingTimeout: If polling times out before the devbox is suspended.
            RunloopError: If the devbox enters a non-suspended terminal state.
        """

        def wait_for_devbox_status() -> DevboxView:
            return self._post(
                f"/v1/devboxes/{id}/wait_for_status",
                body={"statuses": list(DEVBOX_TERMINAL_STATES)},
                cast_to=DevboxView,
            )

        def handle_timeout_error(error: Exception) -> DevboxView:
            if isinstance(error, APITimeoutError) or (
                isinstance(error, APIStatusError) and error.response.status_code == 408
            ):
                return placeholder_devbox_view(id)
            raise error

        def is_terminal_state(devbox: DevboxView) -> bool:
            return devbox.status in DEVBOX_TERMINAL_STATES

        devbox = poll_until(wait_for_devbox_status, is_terminal_state, polling_config, handle_timeout_error)

        if devbox.status != "suspended":
            raise RunloopError(f"Devbox entered non-suspended terminal state: {devbox.status}")

        return devbox

    def create_and_await_running(
        self,
        *,
        blueprint_id: Optional[str] | Omit = omit,
        blueprint_name: Optional[str] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        polling_config: PollingConfig | None = None,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        snapshot_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Create a new devbox and wait for it to be in running state.

        This is a wrapper around the `create` method that waits for the devbox to reach running state.

        Args:
            create_args: Arguments to pass to the `create` method. See the `create` method for detailed documentation.
            request_args: Optional request arguments including polling configuration and additional request options

        Returns:
            The devbox in running state

        Raises:
            PollingTimeout: If polling times out before devbox is running
            RunloopError: If devbox enters a non-running terminal state
        """
        # Pass all create_args to the underlying create method
        devbox = self.create(
            blueprint_id=blueprint_id,
            blueprint_name=blueprint_name,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            mounts=mounts,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            snapshot_id=snapshot_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

        return self.await_running(
            devbox.id,
            polling_config=polling_config,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        status: Literal[
            "provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncDevboxesCursorIDPage[DevboxView]:
        """
        List all Devboxes while optionally filtering by status.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          status: Filter by status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/devboxes",
            page=SyncDevboxesCursorIDPage[DevboxView],
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
            model=DevboxView,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxCreateSSHKeyResponse:
        """
        Create an SSH key for a Devbox to enable remote access.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/create_ssh_key",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxCreateSSHKeyResponse,
        )

    def create_tunnel(
        self,
        id: str,
        *,
        port: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxTunnelView:
        """
        Create a live tunnel to an available port on the Devbox.

        Args:
          port: Devbox port that tunnel will expose.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/create_tunnel",
            body=maybe_transform({"port": port}, devbox_create_tunnel_params.DevboxCreateTunnelParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxTunnelView,
        )

    def delete_disk_snapshot(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Delete a previously taken disk snapshot of a Devbox.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/disk_snapshots/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BinaryAPIResponse:
        """
        Download file contents of any type (binary, text, etc) from a specified path on
        the Devbox.

        Args:
          path: The path on the Devbox filesystem to read the file from. Path is relative to
              user home directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return self._post(
            f"/v1/devboxes/{id}/download_file",
            body=maybe_transform({"path": path}, devbox_download_file_params.DevboxDownloadFileParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BinaryAPIResponse,
        )

    def execute(
        self,
        id: str,
        *,
        command: str,
        command_id: str = str(uuid7()),
        last_n: str | Omit = omit,
        optimistic_timeout: Optional[int] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Execute a command with a known command ID on a devbox, optimistically waiting
        for it to complete within the specified timeout. If it completes in time, return
        the result. If not, return a status indicating the command is still running.
        Note: attach_stdin parameter is not supported; use execute_async for stdin
        support.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

          command_id: The command ID in UUIDv7 string format for idempotency and tracking

          last_n: Last n lines of standard error / standard out to return (default: 100)

          optimistic_timeout: Timeout in seconds to wait for command completion. Operation is not killed. Max
              is 600 seconds.

          shell_name: The name of the persistent shell to create or use if already created. When using
              a persistent shell, the command will run from the directory at the end of the
              previous command and environment variables will be preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return self._post(
            f"/v1/devboxes/{id}/execute",
            body=maybe_transform(
                {
                    "command": command,
                    "command_id": command_id,
                    "optimistic_timeout": optimistic_timeout,
                    "shell_name": shell_name,
                },
                devbox_execute_params.DevboxExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform({"last_n": last_n}, devbox_execute_params.DevboxExecuteParams),
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    def execute_and_await_completion(
        self,
        devbox_id: str,
        *,
        command: str,
        command_id: str = str(uuid7()),
        last_n: str | Omit = omit,
        optimistic_timeout: Optional[int] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        polling_config: PollingConfig | None = None,
        # The following are forwarded to the initial execute request
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Execute a command and wait for it to complete with optimal latency for long running commands.

        This method launches an execution and first attempts to
        return the result within the initial request's timeout. If the execution is not yet
        complete, it switches to using wait_for_command to minimize latency while waiting.

        A command_id (UUIDv7) is automatically generated for idempotency and tracking.
        You can provide your own command_id to enable custom retry logic or external tracking.
        """
        execution = self.execute(
            devbox_id,
            command=command,
            command_id=command_id,
            last_n=last_n,
            optimistic_timeout=optimistic_timeout,
            shell_name=shell_name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        if execution.status == "completed":
            return execution

        def handle_timeout_error(error: Exception) -> DevboxAsyncExecutionDetailView:
            if isinstance(error, APITimeoutError) or (
                isinstance(error, APIStatusError) and error.response.status_code == 408
            ):
                return execution
            raise error

        def is_done(result: DevboxAsyncExecutionDetailView) -> bool:
            return result.status == "completed"

        return poll_until(
            lambda: self.wait_for_command(execution.execution_id, devbox_id=devbox_id, statuses=["completed"]),
            is_done,
            polling_config,
            handle_timeout_error,
        )

    def execute_async(
        self,
        id: str,
        *,
        command: str,
        attach_stdin: Optional[bool] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Execute the given command in the Devbox shell asynchronously and returns the
        execution that can be used to track the command's progress.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

          attach_stdin: Whether to attach stdin streaming for async commands. Not valid for execute_sync
              endpoint. Defaults to false if not specified.

          shell_name: The name of the persistent shell to create or use if already created. When using
              a persistent shell, the command will run from the directory at the end of the
              previous command and environment variables will be preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/execute_async",
            body=maybe_transform(
                {
                    "command": command,
                    "attach_stdin": attach_stdin,
                    "shell_name": shell_name,
                },
                devbox_execute_async_params.DevboxExecuteAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    @typing_extensions.deprecated("deprecated")
    # Use execute, execute_async, or execute_and_await_completion instead
    def execute_sync(
        self,
        id: str,
        *,
        command: str,
        attach_stdin: Optional[bool] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView:
        """
        Execute a bash command in the Devbox shell, await the command completion and
        return the output. Note: attach_stdin parameter is not supported for synchronous
        execution.

        .. deprecated::
           Use execute, execute_async, or execute_and_await_completion instead.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

          attach_stdin: Whether to attach stdin streaming for async commands. Not valid for execute_sync
              endpoint. Defaults to false if not specified.

          shell_name: The name of the persistent shell to create or use if already created. When using
              a persistent shell, the command will run from the directory at the end of the
              previous command and environment variables will be preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return self._post(
            f"/v1/devboxes/{id}/execute_sync",
            body=maybe_transform(
                {
                    "command": command,
                    "attach_stdin": attach_stdin,
                    "shell_name": shell_name,
                },
                devbox_execute_sync_params.DevboxExecuteSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxExecutionDetailView,
        )

    def keep_alive(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Send a 'Keep Alive' signal to a running Devbox that is configured to shutdown on
        idle so the idle time resets.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/keep_alive",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def list_disk_snapshots(
        self,
        *,
        devbox_id: str | Omit = omit,
        limit: int | Omit = omit,
        metadata_key: str | Omit = omit,
        metadata_key_in: str | Omit = omit,
        source_blueprint_id: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]:
        """
        List all snapshots of a Devbox while optionally filtering by Devbox ID, source
        Blueprint ID, and metadata.

        Args:
          devbox_id: Devbox ID to filter by.

          limit: The limit of items to return. Default is 20.

          metadata_key: Filter snapshots by metadata key-value pair. Can be used multiple times for
              different keys.

          metadata_key_in: Filter snapshots by metadata key with multiple possible values (OR condition).

          source_blueprint_id: Source Blueprint ID to filter snapshots by.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/devboxes/disk_snapshots",
            page=SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "devbox_id": devbox_id,
                        "limit": limit,
                        "metadata_key": metadata_key,
                        "metadata_key_in": metadata_key_in,
                        "source_blueprint_id": source_blueprint_id,
                        "starting_after": starting_after,
                    },
                    devbox_list_disk_snapshots_params.DevboxListDiskSnapshotsParams,
                ),
            ),
            model=DevboxSnapshotView,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """Read file contents from a file on a Devbox as a UTF-8.

        Note 'downloadFile'
        should be used for large files (greater than 100MB). Returns the file contents
        as a UTF-8 string.

        Args:
          file_path: The path on the Devbox filesystem to read the file from. Path is relative to
              user home directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._post(
            f"/v1/devboxes/{id}/read_file_contents",
            body=maybe_transform(
                {"file_path": file_path}, devbox_read_file_contents_params.DevboxReadFileContentsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    def remove_tunnel(
        self,
        id: str,
        *,
        port: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Remove a previously opened tunnel on the Devbox.

        Args:
          port: Devbox port that tunnel will expose.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/remove_tunnel",
            body=maybe_transform({"port": port}, devbox_remove_tunnel_params.DevboxRemoveTunnelParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def resume(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Resume a suspended Devbox with the disk state captured as suspend time.

        Note
        that any previously running processes or daemons will need to be restarted using
        the Devbox shell tools.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/resume",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Shutdown a running Devbox.

        This will permanently stop the Devbox. If you want to
        save the state of the Devbox, you should take a snapshot before shutting down or
        should suspend the Devbox instead of shutting down.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/shutdown",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
        )

    def snapshot_disk(
        self,
        id: str,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        """
        Create a disk snapshot of a devbox with the specified name and metadata to
        enable launching future Devboxes with the same disk state.

        Args:
          commit_message: (Optional) Commit message associated with the snapshot (max 1000 characters)

          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return self._post(
            f"/v1/devboxes/{id}/snapshot_disk",
            body=maybe_transform(
                {
                    "commit_message": commit_message,
                    "metadata": metadata,
                    "name": name,
                },
                devbox_snapshot_disk_params.DevboxSnapshotDiskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSnapshotView,
        )

    def snapshot_disk_async(
        self,
        id: str,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        """
        Start an asynchronous disk snapshot of a devbox with the specified name and
        metadata. The snapshot operation will continue in the background and can be
        monitored using the query endpoint.

        Args:
          commit_message: (Optional) Commit message associated with the snapshot (max 1000 characters)

          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/snapshot_disk_async",
            body=maybe_transform(
                {
                    "commit_message": commit_message,
                    "metadata": metadata,
                    "name": name,
                },
                devbox_snapshot_disk_async_params.DevboxSnapshotDiskAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSnapshotView,
        )

    def suspend(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """
        Suspend a running Devbox and create a disk snapshot to enable resuming the
        Devbox later with the same disk. Note this will not snapshot memory state such
        as running processes.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/suspend",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
        )

    def upload_file(
        self,
        id: str,
        *,
        path: str,
        file: FileTypes | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """Upload file contents of any type (binary, text, etc) to a Devbox.

        Note this API
        is suitable for large files (larger than 100MB) and efficiently uploads files
        via multipart form data.

        Args:
          path: The path to write the file to on the Devbox. Path is relative to user home
              directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        body = deepcopy_minimal(
            {
                "path": path,
                "file": file,
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
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def wait_for_command(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        statuses: List[Literal["queued", "running", "completed"]],
        last_n: str | Omit = omit,
        timeout_seconds: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Polls the asynchronous execution's status until it reaches one of the desired
        statuses or times out. Defaults to 60 seconds.

        Args:
          statuses: The command execution statuses to wait for. At least one status must be
              provided. The command will be returned as soon as it reaches any of the provided
              statuses.

          last_n: Last n lines of standard error / standard out to return (default: 100)

          timeout_seconds: (Optional) Timeout in seconds to wait for the status, up to 60 seconds. Defaults
              to 60 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return self._post(
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/wait_for_status",
            body=maybe_transform(
                {
                    "statuses": statuses,
                    "timeout_seconds": timeout_seconds,
                },
                devbox_wait_for_command_params.DevboxWaitForCommandParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform({"last_n": last_n}, devbox_wait_for_command_params.DevboxWaitForCommandParams),
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    def write_file_contents(
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView:
        """Write UTF-8 string contents to a file at path on the Devbox.

        Note for large
        files (larger than 100MB), the upload_file endpoint must be used.

        Args:
          contents: The UTF-8 string contents to write to the file.

          file_path: The path to write the file to on the Devbox. Path is relative to user home
              directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return self._post(
            f"/v1/devboxes/{id}/write_file_contents",
            body=maybe_transform(
                {
                    "contents": contents,
                    "file_path": file_path,
                },
                devbox_write_file_contents_params.DevboxWriteFileContentsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxExecutionDetailView,
        )


class AsyncDevboxesResource(AsyncAPIResource):
    @cached_property
    def disk_snapshots(self) -> AsyncDiskSnapshotsResource:
        return AsyncDiskSnapshotsResource(self._client)

    @cached_property
    def browsers(self) -> AsyncBrowsersResource:
        return AsyncBrowsersResource(self._client)

    @cached_property
    def computers(self) -> AsyncComputersResource:
        return AsyncComputersResource(self._client)

    @cached_property
    def logs(self) -> AsyncLogsResource:
        return AsyncLogsResource(self._client)

    @cached_property
    def executions(self) -> AsyncExecutionsResource:
        return AsyncExecutionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDevboxesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
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
        blueprint_id: Optional[str] | Omit = omit,
        blueprint_name: Optional[str] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        snapshot_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Create a Devbox and begin the boot process.

        The Devbox will initially launch in
        the 'provisioning' state while Runloop allocates the necessary infrastructure.
        It will transition to the 'initializing' state while the booted Devbox runs any
        Runloop or user defined set up scripts. Finally, the Devbox will transition to
        the 'running' state when it is ready for use.

        Args:
          blueprint_id: Blueprint ID to use for the Devbox. If none set, the Devbox will be created with
              the default Runloop Devbox image. Only one of (Snapshot ID, Blueprint ID,
              Blueprint name) should be specified.

          blueprint_name: Name of Blueprint to use for the Devbox. When set, this will load the latest
              successfully built Blueprint with the given name. Only one of (Snapshot ID,
              Blueprint ID, Blueprint name) should be specified.

          code_mounts: A list of code mounts to be included in the Devbox.

          entrypoint: (Optional) When specified, the Devbox will run this script as its main
              executable. The devbox lifecycle will be bound to entrypoint, shutting down when
              the process is complete.

          environment_variables: (Optional) Environment variables used to configure your Devbox.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure the resources and launch time behavior of the Devbox.

          metadata: User defined metadata to attach to the devbox for organization.

          mounts: A list of file system mounts to be included in the Devbox.

          name: (Optional) A user specified name to give the Devbox.

          repo_connection_id: Repository connection id the devbox should source its base image from.

          secrets: (Optional) Map of environment variable names to secret names. The secret values
              will be securely injected as environment variables in the Devbox. Example:
              {"DB_PASS": "DATABASE_PASSWORD"} sets environment variable 'DB_PASS' to the
              value of secret 'DATABASE_PASSWORD'.

          snapshot_id: Snapshot ID to use for the Devbox. Only one of (Snapshot ID, Blueprint ID,
              Blueprint name) should be specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
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
                    "mounts": mounts,
                    "name": name,
                    "repo_connection_id": repo_connection_id,
                    "secrets": secrets,
                    "snapshot_id": snapshot_id,
                },
                devbox_create_params.DevboxCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DevboxView:
        """
        Get the latest details and status of a Devbox.

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

    async def create_and_await_running(
        self,
        *,
        blueprint_id: Optional[str] | Omit = omit,
        blueprint_name: Optional[str] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        entrypoint: Optional[str] | Omit = omit,
        environment_variables: Optional[Dict[str, str]] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        mounts: Optional[Iterable[Mount]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        polling_config: PollingConfig | None = None,
        repo_connection_id: Optional[str] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        snapshot_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Create a devbox and wait for it to be in running state.

        This is a wrapper around the `create` method that waits for the devbox to reach running state.

        Args:
            See the `create` method for detailed documentation.
            polling_config: Optional polling configuration

        Returns:
            The devbox in running state

        Raises:
            PollingTimeout: If polling times out before devbox is running
            RunloopError: If devbox enters a non-running terminal state
        """

        # Pass all create_args, relevant request args to the underlying create method
        devbox = await self.create(
            blueprint_id=blueprint_id,
            blueprint_name=blueprint_name,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            mounts=mounts,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            snapshot_id=snapshot_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

        return await self.await_running(
            devbox.id,
            polling_config=polling_config,
        )

    async def await_running(
        self,
        id: str,
        *,
        # Use polling_config to configure the "long" polling behavior.
        polling_config: PollingConfig | None = None,
    ) -> DevboxView:
        """Wait for a devbox to be in running state.

        Args:
            id: The ID of the devbox to wait for
            config: Optional polling configuration
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds

        Returns:
            The devbox in running state

        Raises:
            PollingTimeout: If polling times out before devbox is running
            RunloopError: If devbox enters a non-running terminal state
        """

        async def wait_for_devbox_status() -> DevboxView:
            # This wait_for_status endpoint polls the devbox status for 10 seconds until it reaches either running or failure.
            # If it's neither, it will throw an error.
            try:
                return await self._post(
                    f"/v1/devboxes/{id}/wait_for_status",
                    body={"statuses": ["running", "failure", "shutdown"]},
                    cast_to=DevboxView,
                )
            except (APITimeoutError, APIStatusError) as error:
                # Handle timeout errors by returning current devbox state to continue polling
                if isinstance(error, APITimeoutError) or error.response.status_code == 408:
                    # Return a placeholder result to continue polling
                    return placeholder_devbox_view(id)

                # Re-raise other errors to stop polling
                raise

        def is_done_booting(devbox: DevboxView) -> bool:
            return devbox.status not in DEVBOX_BOOTING_STATES

        devbox = await async_poll_until(wait_for_devbox_status, is_done_booting, polling_config)

        if devbox.status != "running":
            raise RunloopError(f"Devbox entered non-running terminal state: {devbox.status}")

        return devbox

    async def await_suspended(
        self,
        id: str,
        *,
        polling_config: PollingConfig | None = None,
    ) -> DevboxView:
        """Wait for a devbox to reach the suspended state.

        Args:
            id: The ID of the devbox to wait for.
            polling_config: Optional polling configuration.

        Returns:
            The devbox in the suspended state.

        Raises:
            PollingTimeout: If polling times out before the devbox is suspended.
            RunloopError: If the devbox enters a non-suspended terminal state.
        """

        async def wait_for_devbox_status() -> DevboxView:
            try:
                return await self._post(
                    f"/v1/devboxes/{id}/wait_for_status",
                    body={"statuses": list(DEVBOX_TERMINAL_STATES)},
                    cast_to=DevboxView,
                )
            except (APITimeoutError, APIStatusError) as error:
                if isinstance(error, APITimeoutError) or error.response.status_code == 408:
                    return placeholder_devbox_view(id)
                raise

        def is_terminal_state(devbox: DevboxView) -> bool:
            return devbox.status in DEVBOX_TERMINAL_STATES

        devbox = await async_poll_until(wait_for_devbox_status, is_terminal_state, polling_config)

        if devbox.status != "suspended":
            raise RunloopError(f"Devbox entered non-suspended terminal state: {devbox.status}")

        return devbox

    async def update(
        self,
        id: str,
        *,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """
        Updates a devbox by doing a complete update the existing name,metadata fields.
        It does not patch partial values.

        Args:
          metadata: User defined metadata to attach to the devbox for organization.

          name: (Optional) A user specified name to give the Devbox.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}",
            body=await async_maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                devbox_update_params.DevboxUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        status: Literal[
            "provisioning", "initializing", "running", "suspending", "suspended", "resuming", "failure", "shutdown"
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[DevboxView, AsyncDevboxesCursorIDPage[DevboxView]]:
        """
        List all Devboxes while optionally filtering by status.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          status: Filter by status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/devboxes",
            page=AsyncDevboxesCursorIDPage[DevboxView],
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
            model=DevboxView,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxCreateSSHKeyResponse:
        """
        Create an SSH key for a Devbox to enable remote access.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/create_ssh_key",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxCreateSSHKeyResponse,
        )

    async def create_tunnel(
        self,
        id: str,
        *,
        port: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxTunnelView:
        """
        Create a live tunnel to an available port on the Devbox.

        Args:
          port: Devbox port that tunnel will expose.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/create_tunnel",
            body=await async_maybe_transform({"port": port}, devbox_create_tunnel_params.DevboxCreateTunnelParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxTunnelView,
        )

    async def delete_disk_snapshot(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Delete a previously taken disk snapshot of a Devbox.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/disk_snapshots/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncBinaryAPIResponse:
        """
        Download file contents of any type (binary, text, etc) from a specified path on
        the Devbox.

        Args:
          path: The path on the Devbox filesystem to read the file from. Path is relative to
              user home directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return await self._post(
            f"/v1/devboxes/{id}/download_file",
            body=await async_maybe_transform({"path": path}, devbox_download_file_params.DevboxDownloadFileParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def execute(
        self,
        id: str,
        *,
        command: str,
        command_id: str = str(uuid7()),
        last_n: str | Omit = omit,
        optimistic_timeout: Optional[int] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Execute a command with a known command ID on a devbox, optimistically waiting
        for it to complete within the specified timeout. If it completes in time, return
        the result. If not, return a status indicating the command is still running.
        Note: attach_stdin parameter is not supported; use execute_async for stdin
        support.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

          command_id: The command ID in UUIDv7 string format for idempotency and tracking

          last_n: Last n lines of standard error / standard out to return (default: 100)

          optimistic_timeout: Timeout in seconds to wait for command completion. Operation is not killed. Max
              is 600 seconds.

          shell_name: The name of the persistent shell to create or use if already created. When using
              a persistent shell, the command will run from the directory at the end of the
              previous command and environment variables will be preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return await self._post(
            f"/v1/devboxes/{id}/execute",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "command_id": command_id,
                    "optimistic_timeout": optimistic_timeout,
                    "shell_name": shell_name,
                },
                devbox_execute_params.DevboxExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform({"last_n": last_n}, devbox_execute_params.DevboxExecuteParams),
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    async def execute_and_await_completion(
        self,
        devbox_id: str,
        *,
        command: str,
        command_id: str = str(uuid7()),
        last_n: str | Omit = omit,
        optimistic_timeout: Optional[int] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        polling_config: PollingConfig | None = None,
        # The following are forwarded to the initial execute request
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Execute a command and wait for it to complete with optimal latency for long running commands.

        This method launches an execution and first attempts to
        return the result within the initial request's timeout. If the execution is not yet
        complete, it switches to using wait_for_command to minimize latency while waiting.

        A command_id (UUIDv7) is automatically generated for idempotency and tracking.
        You can provide your own command_id to enable custom retry logic or external tracking.
        """

        execution = await self.execute(
            devbox_id,
            command=command,
            command_id=command_id,
            last_n=last_n,
            optimistic_timeout=optimistic_timeout,
            shell_name=shell_name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        if execution.status == "completed":
            return execution

        def handle_timeout_error(error: Exception) -> DevboxAsyncExecutionDetailView:
            if isinstance(error, APITimeoutError) or (
                isinstance(error, APIStatusError) and error.response.status_code == 408
            ):
                return execution
            raise error

        def is_done(result: DevboxAsyncExecutionDetailView) -> bool:
            return result.status == "completed"

        return await async_poll_until(
            lambda: self.wait_for_command(execution.execution_id, devbox_id=devbox_id, statuses=["completed"]),
            is_done,
            polling_config,
            handle_timeout_error,
        )

    async def execute_async(
        self,
        id: str,
        *,
        command: str,
        attach_stdin: Optional[bool] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Execute the given command in the Devbox shell asynchronously and returns the
        execution that can be used to track the command's progress.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

          attach_stdin: Whether to attach stdin streaming for async commands. Not valid for execute_sync
              endpoint. Defaults to false if not specified.

          shell_name: The name of the persistent shell to create or use if already created. When using
              a persistent shell, the command will run from the directory at the end of the
              previous command and environment variables will be preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/execute_async",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "attach_stdin": attach_stdin,
                    "shell_name": shell_name,
                },
                devbox_execute_async_params.DevboxExecuteAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    @typing_extensions.deprecated("deprecated")
    # Use execute, execute_async, or execute_and_await_completion instead
    async def execute_sync(
        self,
        id: str,
        *,
        command: str,
        attach_stdin: Optional[bool] | Omit = omit,
        shell_name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView:
        """
        Execute a bash command in the Devbox shell, await the command completion and
        return the output. Note: attach_stdin parameter is not supported for synchronous
        execution.

        .. deprecated::
           Use execute, execute_async, or execute_and_await_completion instead.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

          attach_stdin: Whether to attach stdin streaming for async commands. Not valid for execute_sync
              endpoint. Defaults to false if not specified.

          shell_name: The name of the persistent shell to create or use if already created. When using
              a persistent shell, the command will run from the directory at the end of the
              previous command and environment variables will be preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return await self._post(
            f"/v1/devboxes/{id}/execute_sync",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "attach_stdin": attach_stdin,
                    "shell_name": shell_name,
                },
                devbox_execute_sync_params.DevboxExecuteSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxExecutionDetailView,
        )

    async def keep_alive(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Send a 'Keep Alive' signal to a running Devbox that is configured to shutdown on
        idle so the idle time resets.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/keep_alive",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def list_disk_snapshots(
        self,
        *,
        devbox_id: str | Omit = omit,
        limit: int | Omit = omit,
        metadata_key: str | Omit = omit,
        metadata_key_in: str | Omit = omit,
        source_blueprint_id: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[DevboxSnapshotView, AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]]:
        """
        List all snapshots of a Devbox while optionally filtering by Devbox ID, source
        Blueprint ID, and metadata.

        Args:
          devbox_id: Devbox ID to filter by.

          limit: The limit of items to return. Default is 20.

          metadata_key: Filter snapshots by metadata key-value pair. Can be used multiple times for
              different keys.

          metadata_key_in: Filter snapshots by metadata key with multiple possible values (OR condition).

          source_blueprint_id: Source Blueprint ID to filter snapshots by.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/devboxes/disk_snapshots",
            page=AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "devbox_id": devbox_id,
                        "limit": limit,
                        "metadata_key": metadata_key,
                        "metadata_key_in": metadata_key_in,
                        "source_blueprint_id": source_blueprint_id,
                        "starting_after": starting_after,
                    },
                    devbox_list_disk_snapshots_params.DevboxListDiskSnapshotsParams,
                ),
            ),
            model=DevboxSnapshotView,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """Read file contents from a file on a Devbox as a UTF-8.

        Note 'downloadFile'
        should be used for large files (greater than 100MB). Returns the file contents
        as a UTF-8 string.

        Args:
          file_path: The path on the Devbox filesystem to read the file from. Path is relative to
              user home directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._post(
            f"/v1/devboxes/{id}/read_file_contents",
            body=await async_maybe_transform(
                {"file_path": file_path}, devbox_read_file_contents_params.DevboxReadFileContentsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    async def remove_tunnel(
        self,
        id: str,
        *,
        port: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Remove a previously opened tunnel on the Devbox.

        Args:
          port: Devbox port that tunnel will expose.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/remove_tunnel",
            body=await async_maybe_transform({"port": port}, devbox_remove_tunnel_params.DevboxRemoveTunnelParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    async def resume(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Resume a suspended Devbox with the disk state captured as suspend time.

        Note
        that any previously running processes or daemons will need to be restarted using
        the Devbox shell tools.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/resume",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """Shutdown a running Devbox.

        This will permanently stop the Devbox. If you want to
        save the state of the Devbox, you should take a snapshot before shutting down or
        should suspend the Devbox instead of shutting down.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/shutdown",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
        )

    async def snapshot_disk(
        self,
        id: str,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        """
        Create a disk snapshot of a devbox with the specified name and metadata to
        enable launching future Devboxes with the same disk state.

        Args:
          commit_message: (Optional) Commit message associated with the snapshot (max 1000 characters)

          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return await self._post(
            f"/v1/devboxes/{id}/snapshot_disk",
            body=await async_maybe_transform(
                {
                    "commit_message": commit_message,
                    "metadata": metadata,
                    "name": name,
                },
                devbox_snapshot_disk_params.DevboxSnapshotDiskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSnapshotView,
        )

    async def snapshot_disk_async(
        self,
        id: str,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        """
        Start an asynchronous disk snapshot of a devbox with the specified name and
        metadata. The snapshot operation will continue in the background and can be
        monitored using the query endpoint.

        Args:
          commit_message: (Optional) Commit message associated with the snapshot (max 1000 characters)

          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/snapshot_disk_async",
            body=await async_maybe_transform(
                {
                    "commit_message": commit_message,
                    "metadata": metadata,
                    "name": name,
                },
                devbox_snapshot_disk_async_params.DevboxSnapshotDiskAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSnapshotView,
        )

    async def suspend(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxView:
        """
        Suspend a running Devbox and create a disk snapshot to enable resuming the
        Devbox later with the same disk. Note this will not snapshot memory state such
        as running processes.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/suspend",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxView,
        )

    async def upload_file(
        self,
        id: str,
        *,
        path: str,
        file: FileTypes | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """Upload file contents of any type (binary, text, etc) to a Devbox.

        Note this API
        is suitable for large files (larger than 100MB) and efficiently uploads files
        via multipart form data.

        Args:
          path: The path to write the file to on the Devbox. Path is relative to user home
              directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        body = deepcopy_minimal(
            {
                "path": path,
                "file": file,
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
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    async def wait_for_command(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        statuses: List[Literal["queued", "running", "completed"]],
        last_n: str | Omit = omit,
        timeout_seconds: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Polls the asynchronous execution's status until it reaches one of the desired
        statuses or times out. Defaults to 60 seconds.

        Args:
          statuses: The command execution statuses to wait for. At least one status must be
              provided. The command will be returned as soon as it reaches any of the provided
              statuses.

          last_n: Last n lines of standard error / standard out to return (default: 100)

          timeout_seconds: (Optional) Timeout in seconds to wait for the status, up to 60 seconds. Defaults
              to 60 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return await self._post(
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/wait_for_status",
            body=await async_maybe_transform(
                {
                    "statuses": statuses,
                    "timeout_seconds": timeout_seconds,
                },
                devbox_wait_for_command_params.DevboxWaitForCommandParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"last_n": last_n}, devbox_wait_for_command_params.DevboxWaitForCommandParams
                ),
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    async def write_file_contents(
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxExecutionDetailView:
        """Write UTF-8 string contents to a file at path on the Devbox.

        Note for large
        files (larger than 100MB), the upload_file endpoint must be used.

        Args:
          contents: The UTF-8 string contents to write to the file.

          file_path: The path to write the file to on the Devbox. Path is relative to user home
              directory.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 600
        return await self._post(
            f"/v1/devboxes/{id}/write_file_contents",
            body=await async_maybe_transform(
                {
                    "contents": contents,
                    "file_path": file_path,
                },
                devbox_write_file_contents_params.DevboxWriteFileContentsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
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
        self.update = to_raw_response_wrapper(
            devboxes.update,
        )
        self.list = to_raw_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = to_raw_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.create_tunnel = to_raw_response_wrapper(
            devboxes.create_tunnel,
        )
        self.delete_disk_snapshot = to_raw_response_wrapper(
            devboxes.delete_disk_snapshot,
        )
        self.download_file = to_custom_raw_response_wrapper(
            devboxes.download_file,
            BinaryAPIResponse,
        )
        self.execute = to_raw_response_wrapper(
            devboxes.execute,
        )
        self.execute_async = to_raw_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                devboxes.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.keep_alive = to_raw_response_wrapper(
            devboxes.keep_alive,
        )
        self.list_disk_snapshots = to_raw_response_wrapper(
            devboxes.list_disk_snapshots,
        )
        self.read_file_contents = to_raw_response_wrapper(
            devboxes.read_file_contents,
        )
        self.remove_tunnel = to_raw_response_wrapper(
            devboxes.remove_tunnel,
        )
        self.resume = to_raw_response_wrapper(
            devboxes.resume,
        )
        self.shutdown = to_raw_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = to_raw_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.snapshot_disk_async = to_raw_response_wrapper(
            devboxes.snapshot_disk_async,
        )
        self.suspend = to_raw_response_wrapper(
            devboxes.suspend,
        )
        self.upload_file = to_raw_response_wrapper(
            devboxes.upload_file,
        )
        self.wait_for_command = to_raw_response_wrapper(
            devboxes.wait_for_command,
        )
        self.write_file_contents = to_raw_response_wrapper(
            devboxes.write_file_contents,
        )

    @cached_property
    def disk_snapshots(self) -> DiskSnapshotsResourceWithRawResponse:
        return DiskSnapshotsResourceWithRawResponse(self._devboxes.disk_snapshots)

    @cached_property
    def browsers(self) -> BrowsersResourceWithRawResponse:
        return BrowsersResourceWithRawResponse(self._devboxes.browsers)

    @cached_property
    def computers(self) -> ComputersResourceWithRawResponse:
        return ComputersResourceWithRawResponse(self._devboxes.computers)

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
        self.update = async_to_raw_response_wrapper(
            devboxes.update,
        )
        self.list = async_to_raw_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = async_to_raw_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.create_tunnel = async_to_raw_response_wrapper(
            devboxes.create_tunnel,
        )
        self.delete_disk_snapshot = async_to_raw_response_wrapper(
            devboxes.delete_disk_snapshot,
        )
        self.download_file = async_to_custom_raw_response_wrapper(
            devboxes.download_file,
            AsyncBinaryAPIResponse,
        )
        self.execute = async_to_raw_response_wrapper(
            devboxes.execute,
        )
        self.execute_async = async_to_raw_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                devboxes.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.keep_alive = async_to_raw_response_wrapper(
            devboxes.keep_alive,
        )
        self.list_disk_snapshots = async_to_raw_response_wrapper(
            devboxes.list_disk_snapshots,
        )
        self.read_file_contents = async_to_raw_response_wrapper(
            devboxes.read_file_contents,
        )
        self.remove_tunnel = async_to_raw_response_wrapper(
            devboxes.remove_tunnel,
        )
        self.resume = async_to_raw_response_wrapper(
            devboxes.resume,
        )
        self.shutdown = async_to_raw_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = async_to_raw_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.snapshot_disk_async = async_to_raw_response_wrapper(
            devboxes.snapshot_disk_async,
        )
        self.suspend = async_to_raw_response_wrapper(
            devboxes.suspend,
        )
        self.upload_file = async_to_raw_response_wrapper(
            devboxes.upload_file,
        )
        self.wait_for_command = async_to_raw_response_wrapper(
            devboxes.wait_for_command,
        )
        self.write_file_contents = async_to_raw_response_wrapper(
            devboxes.write_file_contents,
        )

    @cached_property
    def disk_snapshots(self) -> AsyncDiskSnapshotsResourceWithRawResponse:
        return AsyncDiskSnapshotsResourceWithRawResponse(self._devboxes.disk_snapshots)

    @cached_property
    def browsers(self) -> AsyncBrowsersResourceWithRawResponse:
        return AsyncBrowsersResourceWithRawResponse(self._devboxes.browsers)

    @cached_property
    def computers(self) -> AsyncComputersResourceWithRawResponse:
        return AsyncComputersResourceWithRawResponse(self._devboxes.computers)

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
        self.update = to_streamed_response_wrapper(
            devboxes.update,
        )
        self.list = to_streamed_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = to_streamed_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.create_tunnel = to_streamed_response_wrapper(
            devboxes.create_tunnel,
        )
        self.delete_disk_snapshot = to_streamed_response_wrapper(
            devboxes.delete_disk_snapshot,
        )
        self.download_file = to_custom_streamed_response_wrapper(
            devboxes.download_file,
            StreamedBinaryAPIResponse,
        )
        self.execute = to_streamed_response_wrapper(
            devboxes.execute,
        )
        self.execute_async = to_streamed_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                devboxes.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.keep_alive = to_streamed_response_wrapper(
            devboxes.keep_alive,
        )
        self.list_disk_snapshots = to_streamed_response_wrapper(
            devboxes.list_disk_snapshots,
        )
        self.read_file_contents = to_streamed_response_wrapper(
            devboxes.read_file_contents,
        )
        self.remove_tunnel = to_streamed_response_wrapper(
            devboxes.remove_tunnel,
        )
        self.resume = to_streamed_response_wrapper(
            devboxes.resume,
        )
        self.shutdown = to_streamed_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = to_streamed_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.snapshot_disk_async = to_streamed_response_wrapper(
            devboxes.snapshot_disk_async,
        )
        self.suspend = to_streamed_response_wrapper(
            devboxes.suspend,
        )
        self.upload_file = to_streamed_response_wrapper(
            devboxes.upload_file,
        )
        self.wait_for_command = to_streamed_response_wrapper(
            devboxes.wait_for_command,
        )
        self.write_file_contents = to_streamed_response_wrapper(
            devboxes.write_file_contents,
        )

    @cached_property
    def disk_snapshots(self) -> DiskSnapshotsResourceWithStreamingResponse:
        return DiskSnapshotsResourceWithStreamingResponse(self._devboxes.disk_snapshots)

    @cached_property
    def browsers(self) -> BrowsersResourceWithStreamingResponse:
        return BrowsersResourceWithStreamingResponse(self._devboxes.browsers)

    @cached_property
    def computers(self) -> ComputersResourceWithStreamingResponse:
        return ComputersResourceWithStreamingResponse(self._devboxes.computers)

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
        self.update = async_to_streamed_response_wrapper(
            devboxes.update,
        )
        self.list = async_to_streamed_response_wrapper(
            devboxes.list,
        )
        self.create_ssh_key = async_to_streamed_response_wrapper(
            devboxes.create_ssh_key,
        )
        self.create_tunnel = async_to_streamed_response_wrapper(
            devboxes.create_tunnel,
        )
        self.delete_disk_snapshot = async_to_streamed_response_wrapper(
            devboxes.delete_disk_snapshot,
        )
        self.download_file = async_to_custom_streamed_response_wrapper(
            devboxes.download_file,
            AsyncStreamedBinaryAPIResponse,
        )
        self.execute = async_to_streamed_response_wrapper(
            devboxes.execute,
        )
        self.execute_async = async_to_streamed_response_wrapper(
            devboxes.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                devboxes.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.keep_alive = async_to_streamed_response_wrapper(
            devboxes.keep_alive,
        )
        self.list_disk_snapshots = async_to_streamed_response_wrapper(
            devboxes.list_disk_snapshots,
        )
        self.read_file_contents = async_to_streamed_response_wrapper(
            devboxes.read_file_contents,
        )
        self.remove_tunnel = async_to_streamed_response_wrapper(
            devboxes.remove_tunnel,
        )
        self.resume = async_to_streamed_response_wrapper(
            devboxes.resume,
        )
        self.shutdown = async_to_streamed_response_wrapper(
            devboxes.shutdown,
        )
        self.snapshot_disk = async_to_streamed_response_wrapper(
            devboxes.snapshot_disk,
        )
        self.snapshot_disk_async = async_to_streamed_response_wrapper(
            devboxes.snapshot_disk_async,
        )
        self.suspend = async_to_streamed_response_wrapper(
            devboxes.suspend,
        )
        self.upload_file = async_to_streamed_response_wrapper(
            devboxes.upload_file,
        )
        self.wait_for_command = async_to_streamed_response_wrapper(
            devboxes.wait_for_command,
        )
        self.write_file_contents = async_to_streamed_response_wrapper(
            devboxes.write_file_contents,
        )

    @cached_property
    def disk_snapshots(self) -> AsyncDiskSnapshotsResourceWithStreamingResponse:
        return AsyncDiskSnapshotsResourceWithStreamingResponse(self._devboxes.disk_snapshots)

    @cached_property
    def browsers(self) -> AsyncBrowsersResourceWithStreamingResponse:
        return AsyncBrowsersResourceWithStreamingResponse(self._devboxes.browsers)

    @cached_property
    def computers(self) -> AsyncComputersResourceWithStreamingResponse:
        return AsyncComputersResourceWithStreamingResponse(self._devboxes.computers)

    @cached_property
    def logs(self) -> AsyncLogsResourceWithStreamingResponse:
        return AsyncLogsResourceWithStreamingResponse(self._devboxes.logs)

    @cached_property
    def executions(self) -> AsyncExecutionsResourceWithStreamingResponse:
        return AsyncExecutionsResourceWithStreamingResponse(self._devboxes.executions)
