# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Optional, cast
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import is_given, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._constants import DEFAULT_TIMEOUT, RAW_RESPONSE_HEADER
from ..._streaming import Stream, AsyncStream, ReconnectingStream, AsyncReconnectingStream
from ..._exceptions import APIStatusError, APITimeoutError
from ...lib.polling import PollingConfig, poll_until
from ..._base_client import make_request_options
from ...types.devboxes import (
    execution_kill_params,
    execution_retrieve_params,
    execution_send_std_in_params,
    execution_execute_sync_params,
    execution_execute_async_params,
    execution_stream_stderr_updates_params,
    execution_stream_stdout_updates_params,
)
from ...lib.polling_async import async_poll_until
from ...types.devbox_send_std_in_result import DevboxSendStdInResult
from ...types.devbox_execution_detail_view import DevboxExecutionDetailView
from ...types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ...types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView

__all__ = ["ExecutionsResource", "AsyncExecutionsResource"]


def placeholder_execution_detail_view(devbox_id: str, execution_id: str) -> DevboxAsyncExecutionDetailView:
    return DevboxAsyncExecutionDetailView(
        devbox_id=devbox_id,
        execution_id=execution_id,
        status="queued",
        stdout="",
        stderr="",
    )


class ExecutionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExecutionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return ExecutionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExecutionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return ExecutionsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        last_n: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Get the latest status of a previously launched asynchronous execuction including
        stdout/error and the exit code if complete.

        Args:
          last_n: Last n lines of standard error / standard out to return (default: 100)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return self._get(
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"last_n": last_n}, execution_retrieve_params.ExecutionRetrieveParams),
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    def await_completed(
        self,
        execution_id: str,
        devbox_id: str,
        *,
        # Use polling_config to configure the "long" polling behavior.
        polling_config: PollingConfig | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """Wait for an execution to complete.

        Args:
            execution_id: The ID of the execution to wait for
            id: The ID of the devbox
            config: Optional polling configuration
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds

        Returns:
            The completed execution

        Raises:
            PollingTimeout: If polling times out before execution completes
        """

        def wait_for_execution_status() -> DevboxAsyncExecutionDetailView:
            # This wait_for_status endpoint polls the execution status for 60 seconds until it reaches either completed.
            return self._post(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/wait_for_status",
                body={"statuses": ["completed"]},
                cast_to=DevboxAsyncExecutionDetailView,
            )

        def handle_timeout_error(error: Exception) -> DevboxAsyncExecutionDetailView:
            # Handle timeout errors by returning current execution state to continue polling
            if isinstance(error, APITimeoutError) or (
                isinstance(error, APIStatusError) and error.response.status_code == 408
            ):
                # Return a placeholder result to continue polling
                return placeholder_execution_detail_view(devbox_id, execution_id)
            else:
                # Re-raise other errors to stop polling
                raise error

        def is_done(execution: DevboxAsyncExecutionDetailView) -> bool:
            return execution.status == "completed"

        return poll_until(wait_for_execution_status, is_done, polling_config, handle_timeout_error)

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
                execution_execute_async_params.ExecutionExecuteAsyncParams,
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
                execution_execute_sync_params.ExecutionExecuteSyncParams,
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

    def kill(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        kill_process_group: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Kill a previously launched asynchronous execution if it is still running by
        killing the launched process. Optionally kill the entire process group.

        Args:
          kill_process_group: Whether to kill the entire process group (default: false). If true, kills all
              processes in the same process group as the target process.

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/kill",
            body=maybe_transform({"kill_process_group": kill_process_group}, execution_kill_params.ExecutionKillParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    def send_std_in(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        signal: Optional[Literal["EOF", "INTERRUPT"]] | Omit = omit,
        text: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSendStdInResult:
        """
        Send content to the Std In of a running execution.

        Args:
          signal: Signal to send to std in of the running execution.

          text: Text to send to std in of the running execution.

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/send_std_in",
            body=maybe_transform(
                {
                    "signal": signal,
                    "text": text,
                },
                execution_send_std_in_params.ExecutionSendStdInParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSendStdInResult,
        )

    def stream_stderr_updates(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        offset: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[ExecutionUpdateChunk]:
        """
        Tails the stderr logs for the given execution with SSE streaming

        Args:
          offset: The byte offset to start the stream from (if unspecified, starts from the
              beginning of the stream)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")

        default_headers: Headers = {"Accept": "text/event-stream"}
        merged_headers = default_headers if extra_headers is None else {**default_headers, **extra_headers}

        if merged_headers and merged_headers.get(RAW_RESPONSE_HEADER):
            return self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {"offset": offset}, execution_stream_stderr_updates_params.ExecutionStreamStderrUpdatesParams
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=Stream[ExecutionUpdateChunk],
            )

        def create_stream(last_offset: str | None) -> Stream[ExecutionUpdateChunk]:
            new_offset = last_offset if last_offset is not None else (None if isinstance(offset, NotGiven) else offset)
            return self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {"offset": new_offset},
                        execution_stream_stderr_updates_params.ExecutionStreamStderrUpdatesParams,
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=Stream[ExecutionUpdateChunk],
            )

        initial_stream = create_stream(None)

        def get_offset(item: ExecutionUpdateChunk) -> str | None:
            value = getattr(item, "offset", None)
            if value is None:
                return None
            return str(value)

        return cast(
            Stream[ExecutionUpdateChunk],
            ReconnectingStream(current_stream=initial_stream, stream_creator=create_stream, get_offset=get_offset),
        )

    def stream_stdout_updates(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        offset: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[ExecutionUpdateChunk]:
        """
        Tails the stdout logs for the given execution with SSE streaming

        Args:
          offset: The byte offset to start the stream from (if unspecified, starts from the
              beginning of the stream)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")

        default_headers: Headers = {"Accept": "text/event-stream"}
        merged_headers = default_headers if extra_headers is None else {**default_headers, **extra_headers}

        if merged_headers and merged_headers.get(RAW_RESPONSE_HEADER):
            return self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {"offset": offset}, execution_stream_stdout_updates_params.ExecutionStreamStdoutUpdatesParams
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=Stream[ExecutionUpdateChunk],
            )

        def create_stream(last_offset: str | None) -> Stream[ExecutionUpdateChunk]:
            new_offset = last_offset if last_offset is not None else (None if isinstance(offset, NotGiven) else offset)
            return self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {"offset": new_offset},
                        execution_stream_stdout_updates_params.ExecutionStreamStdoutUpdatesParams,
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=Stream[ExecutionUpdateChunk],
            )

        initial_stream = create_stream(None)

        def get_offset(item: ExecutionUpdateChunk) -> str | None:
            value = getattr(item, "offset", None)
            if value is None:
                return None
            return str(value)

        return cast(
            Stream[ExecutionUpdateChunk],
            ReconnectingStream(current_stream=initial_stream, stream_creator=create_stream, get_offset=get_offset),
        )


class AsyncExecutionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExecutionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExecutionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExecutionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncExecutionsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        last_n: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Get the latest status of a previously launched asynchronous execuction including
        stdout/error and the exit code if complete.

        Args:
          last_n: Last n lines of standard error / standard out to return (default: 100)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return await self._get(
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"last_n": last_n}, execution_retrieve_params.ExecutionRetrieveParams
                ),
            ),
            cast_to=DevboxAsyncExecutionDetailView,
        )

    async def await_completed(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        # Use polling_config to configure the "long" polling behavior.
        polling_config: PollingConfig | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """Wait for an execution to complete.

        Args:
            execution_id: The ID of the execution to wait for
            id: The ID of the devbox
            polling_config: Optional polling configuration
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds

        Returns:
            The completed execution

        Raises:
            PollingTimeout: If polling times out before execution completes
        """

        async def wait_for_execution_status() -> DevboxAsyncExecutionDetailView:
            try:
                return await self._post(
                    f"/v1/devboxes/{devbox_id}/executions/{execution_id}/wait_for_status",
                    body={"statuses": ["completed"]},
                    cast_to=DevboxAsyncExecutionDetailView,
                )
            except (APITimeoutError, APIStatusError) as error:
                # Handle timeout errors by returning placeholder to continue polling
                if isinstance(error, APITimeoutError) or error.response.status_code == 408:
                    return placeholder_execution_detail_view(devbox_id, execution_id)

                # Re-raise other errors to stop polling
                raise

        def is_done(execution: DevboxAsyncExecutionDetailView) -> bool:
            return execution.status == "completed"

        return await async_poll_until(wait_for_execution_status, is_done, polling_config)

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
                execution_execute_async_params.ExecutionExecuteAsyncParams,
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
                execution_execute_sync_params.ExecutionExecuteSyncParams,
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

    async def kill(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        kill_process_group: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Kill a previously launched asynchronous execution if it is still running by
        killing the launched process. Optionally kill the entire process group.

        Args:
          kill_process_group: Whether to kill the entire process group (default: false). If true, kills all
              processes in the same process group as the target process.

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/kill",
            body=await async_maybe_transform(
                {"kill_process_group": kill_process_group}, execution_kill_params.ExecutionKillParams
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

    async def send_std_in(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        signal: Optional[Literal["EOF", "INTERRUPT"]] | Omit = omit,
        text: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSendStdInResult:
        """
        Send content to the Std In of a running execution.

        Args:
          signal: Signal to send to std in of the running execution.

          text: Text to send to std in of the running execution.

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/send_std_in",
            body=await async_maybe_transform(
                {
                    "signal": signal,
                    "text": text,
                },
                execution_send_std_in_params.ExecutionSendStdInParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSendStdInResult,
        )

    async def stream_stderr_updates(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        offset: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[ExecutionUpdateChunk]:
        """
        Tails the stderr logs for the given execution with SSE streaming

        Args:
          offset: The byte offset to start the stream from (if unspecified, starts from the
              beginning of the stream)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")

        default_headers: Headers = {"Accept": "text/event-stream"}
        merged_headers = default_headers if extra_headers is None else {**default_headers, **extra_headers}

        if merged_headers and merged_headers.get(RAW_RESPONSE_HEADER):
            return await self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"offset": offset}, execution_stream_stderr_updates_params.ExecutionStreamStderrUpdatesParams
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=AsyncStream[ExecutionUpdateChunk],
            )

        async def create_stream(last_offset: str | None) -> AsyncStream[ExecutionUpdateChunk]:
            new_offset = last_offset if last_offset is not None else (None if isinstance(offset, NotGiven) else offset)
            return await self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"offset": new_offset},
                        execution_stream_stderr_updates_params.ExecutionStreamStderrUpdatesParams,
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=AsyncStream[ExecutionUpdateChunk],
            )

        initial_stream = await create_stream(None)

        def get_offset(item: ExecutionUpdateChunk) -> str | None:
            value = getattr(item, "offset", None)
            if value is None:
                return None
            return str(value)

        return cast(
            AsyncStream[ExecutionUpdateChunk],
            AsyncReconnectingStream(current_stream=initial_stream, stream_creator=create_stream, get_offset=get_offset),
        )

    async def stream_stdout_updates(
        self,
        execution_id: str,
        *,
        devbox_id: str,
        offset: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[ExecutionUpdateChunk]:
        """
        Tails the stdout logs for the given execution with SSE streaming

        Args:
          offset: The byte offset to start the stream from (if unspecified, starts from the
              beginning of the stream)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not devbox_id:
            raise ValueError(f"Expected a non-empty value for `devbox_id` but received {devbox_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")

        default_headers: Headers = {"Accept": "text/event-stream"}
        merged_headers = default_headers if extra_headers is None else {**default_headers, **extra_headers}

        # If caller requested a raw or streaming response wrapper, return the underlying stream as-is
        if merged_headers and merged_headers.get(RAW_RESPONSE_HEADER):
            return await self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"offset": offset}, execution_stream_stdout_updates_params.ExecutionStreamStdoutUpdatesParams
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=AsyncStream[ExecutionUpdateChunk],
            )

        async def create_stream(last_offset: str | None) -> AsyncStream[ExecutionUpdateChunk]:
            new_offset = last_offset if last_offset is not None else (None if isinstance(offset, NotGiven) else offset)
            return await self._get(
                f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates",
                options=make_request_options(
                    extra_headers=merged_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"offset": new_offset},
                        execution_stream_stdout_updates_params.ExecutionStreamStdoutUpdatesParams,
                    ),
                ),
                cast_to=DevboxAsyncExecutionDetailView,
                stream=True,
                stream_cls=AsyncStream[ExecutionUpdateChunk],
            )

        initial_stream = await create_stream(None)

        def get_offset(item: ExecutionUpdateChunk) -> str | None:
            value = getattr(item, "offset", None)
            if value is None:
                return None
            return str(value)

        return cast(
            AsyncStream[ExecutionUpdateChunk],
            AsyncReconnectingStream(current_stream=initial_stream, stream_creator=create_stream, get_offset=get_offset),
        )


class ExecutionsResourceWithRawResponse:
    def __init__(self, executions: ExecutionsResource) -> None:
        self._executions = executions

        self.retrieve = to_raw_response_wrapper(
            executions.retrieve,
        )
        self.execute_async = to_raw_response_wrapper(
            executions.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                executions.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.kill = to_raw_response_wrapper(
            executions.kill,
        )
        self.send_std_in = to_raw_response_wrapper(
            executions.send_std_in,
        )
        self.stream_stdout_updates = to_raw_response_wrapper(
            executions.stream_stdout_updates,
        )
        self.stream_stderr_updates = to_raw_response_wrapper(
            executions.stream_stderr_updates,
        )


class AsyncExecutionsResourceWithRawResponse:
    def __init__(self, executions: AsyncExecutionsResource) -> None:
        self._executions = executions

        self.retrieve = async_to_raw_response_wrapper(
            executions.retrieve,
        )
        self.execute_async = async_to_raw_response_wrapper(
            executions.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                executions.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.kill = async_to_raw_response_wrapper(
            executions.kill,
        )
        self.send_std_in = async_to_raw_response_wrapper(
            executions.send_std_in,
        )
        self.stream_stdout_updates = async_to_raw_response_wrapper(
            executions.stream_stdout_updates,
        )
        self.stream_stderr_updates = async_to_raw_response_wrapper(
            executions.stream_stderr_updates,
        )


class ExecutionsResourceWithStreamingResponse:
    def __init__(self, executions: ExecutionsResource) -> None:
        self._executions = executions

        self.retrieve = to_streamed_response_wrapper(
            executions.retrieve,
        )
        self.execute_async = to_streamed_response_wrapper(
            executions.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                executions.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.kill = to_streamed_response_wrapper(
            executions.kill,
        )
        self.send_std_in = to_streamed_response_wrapper(
            executions.send_std_in,
        )
        self.stream_stdout_updates = to_streamed_response_wrapper(
            executions.stream_stdout_updates,
        )
        self.stream_stderr_updates = to_streamed_response_wrapper(
            executions.stream_stderr_updates,
        )


class AsyncExecutionsResourceWithStreamingResponse:
    def __init__(self, executions: AsyncExecutionsResource) -> None:
        self._executions = executions

        self.retrieve = async_to_streamed_response_wrapper(
            executions.retrieve,
        )
        self.execute_async = async_to_streamed_response_wrapper(
            executions.execute_async,
        )
        self.execute_sync = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                executions.execute_sync,  # pyright: ignore[reportDeprecated],
            )
        )
        self.kill = async_to_streamed_response_wrapper(
            executions.kill,
        )
        self.send_std_in = async_to_streamed_response_wrapper(
            executions.send_std_in,
        )
        self.stream_stdout_updates = async_to_streamed_response_wrapper(
            executions.stream_stdout_updates,
        )
        self.stream_stderr_updates = async_to_streamed_response_wrapper(
            executions.stream_stderr_updates,
        )
