# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Optional

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
from ..._constants import DEFAULT_TIMEOUT
from ..._streaming import Stream, AsyncStream
from ..._base_client import make_request_options
from ...types.devboxes import (
    execution_kill_params,
    execution_retrieve_params,
    execution_execute_sync_params,
    execution_execute_async_params,
    execution_stream_stderr_updates_params,
    execution_stream_stdout_updates_params,
)
from ...types.devbox_execution_detail_view import DevboxExecutionDetailView
from ...types.devboxes.execution_update_chunk import ExecutionUpdateChunk
from ...types.devbox_async_execution_detail_view import DevboxAsyncExecutionDetailView

__all__ = ["ExecutionsResource", "AsyncExecutionsResource"]


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
          last_n: Last n lines of standard error / standard out to return

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

    def execute_async(
        self,
        id: str,
        *,
        command: str,
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
        return the output.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

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
          offset: The byte offset to start the stream from

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"offset": offset}, execution_stream_stderr_updates_params.ExecutionStreamStderrUpdatesParams
                ),
            ),
            cast_to=ExecutionUpdateChunk,
            stream=True,
            stream_cls=Stream[ExecutionUpdateChunk],
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
          offset: The byte offset to start the stream from

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"offset": offset}, execution_stream_stdout_updates_params.ExecutionStreamStdoutUpdatesParams
                ),
            ),
            cast_to=ExecutionUpdateChunk,
            stream=True,
            stream_cls=Stream[ExecutionUpdateChunk],
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
          last_n: Last n lines of standard error / standard out to return

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

    async def execute_async(
        self,
        id: str,
        *,
        command: str,
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
        return the output.

        Args:
          command: The command to execute via the Devbox shell. By default, commands are run from
              the user home directory unless shell_name is specified. If shell_name is
              specified the command is run from the directory based on the recent state of the
              persistent shell.

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
          offset: The byte offset to start the stream from

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"offset": offset}, execution_stream_stderr_updates_params.ExecutionStreamStderrUpdatesParams
                ),
            ),
            cast_to=ExecutionUpdateChunk,
            stream=True,
            stream_cls=AsyncStream[ExecutionUpdateChunk],
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
          offset: The byte offset to start the stream from

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
            f"/v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"offset": offset}, execution_stream_stdout_updates_params.ExecutionStreamStdoutUpdatesParams
                ),
            ),
            cast_to=ExecutionUpdateChunk,
            stream=True,
            stream_cls=AsyncStream[ExecutionUpdateChunk],
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
        self.stream_stderr_updates = to_raw_response_wrapper(
            executions.stream_stderr_updates,
        )
        self.stream_stdout_updates = to_raw_response_wrapper(
            executions.stream_stdout_updates,
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
        self.stream_stderr_updates = async_to_raw_response_wrapper(
            executions.stream_stderr_updates,
        )
        self.stream_stdout_updates = async_to_raw_response_wrapper(
            executions.stream_stdout_updates,
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
        self.stream_stderr_updates = to_streamed_response_wrapper(
            executions.stream_stderr_updates,
        )
        self.stream_stdout_updates = to_streamed_response_wrapper(
            executions.stream_stdout_updates,
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
        self.stream_stderr_updates = async_to_streamed_response_wrapper(
            executions.stream_stderr_updates,
        )
        self.stream_stdout_updates = async_to_streamed_response_wrapper(
            executions.stream_stdout_updates,
        )
