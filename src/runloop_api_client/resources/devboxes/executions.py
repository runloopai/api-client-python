# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import is_given, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...lib.polling import PollingConfig, poll_until
from ..._constants import DEFAULT_TIMEOUT
from ..._base_client import make_request_options
from ...types.devboxes import execution_retrieve_params, execution_execute_sync_params, execution_execute_async_params
from ...lib.polling_async import async_poll_until
from ...types.devbox_execution_detail_view import DevboxExecutionDetailView
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
        last_n: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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

    def await_completed(
        self,
        execution_id: str,
        devbox_id: str,
        *,
        config: PollingConfig | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
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
        def retrieve_execution() -> DevboxAsyncExecutionDetailView:
            return self.retrieve(
                execution_id,
                devbox_id=devbox_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout
            )

        def is_done(execution: DevboxAsyncExecutionDetailView) -> bool:
            return execution.status == 'completed'

        return poll_until(retrieve_execution, is_done, config)    

    def execute_async(
        self,
        id: str,
        *,
        command: str,
        shell_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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

    def execute_sync(
        self,
        id: str,
        *,
        command: str,
        shell_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Kill a previously launched asynchronous execution if it is still running by
        killing the launched process.

        Args:
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
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxAsyncExecutionDetailView,
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
        last_n: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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

    async def await_completed(
        self,
        execution_id: str,        
        *,
        devbox_id: str,
        polling_config: PollingConfig | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
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
        async def retrieve_execution() -> DevboxAsyncExecutionDetailView:
            return await self.retrieve(
                execution_id,
                devbox_id=devbox_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout
            )

        def is_done(execution: DevboxAsyncExecutionDetailView) -> bool:
            return execution.status == 'completed'

        return await async_poll_until(retrieve_execution, is_done, polling_config)

    async def execute_async(
        self,
        id: str,
        *,
        command: str,
        shell_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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

    async def execute_sync(
        self,
        id: str,
        *,
        command: str,
        shell_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DevboxAsyncExecutionDetailView:
        """
        Kill a previously launched asynchronous execution if it is still running by
        killing the launched process.

        Args:
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
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxAsyncExecutionDetailView,
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
        self.execute_sync = to_raw_response_wrapper(
            executions.execute_sync,
        )
        self.kill = to_raw_response_wrapper(
            executions.kill,
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
        self.execute_sync = async_to_raw_response_wrapper(
            executions.execute_sync,
        )
        self.kill = async_to_raw_response_wrapper(
            executions.kill,
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
        self.execute_sync = to_streamed_response_wrapper(
            executions.execute_sync,
        )
        self.kill = to_streamed_response_wrapper(
            executions.kill,
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
        self.execute_sync = async_to_streamed_response_wrapper(
            executions.execute_sync,
        )
        self.kill = async_to_streamed_response_wrapper(
            executions.kill,
        )
