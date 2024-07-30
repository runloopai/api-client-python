# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List

import httpx

from .logs import (
    LogsResource,
    AsyncLogsResource,
    LogsResourceWithRawResponse,
    AsyncLogsResourceWithRawResponse,
    LogsResourceWithStreamingResponse,
    AsyncLogsResourceWithStreamingResponse,
)
from ...types import devbox_list_params, devbox_create_params, devbox_execute_sync_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.devbox_view import DevboxView
from ...types.devbox_list_view import DevboxListView
from ...types.devbox_execution_detail_view import DevboxExecutionDetailView

__all__ = ["DevboxesResource", "AsyncDevboxesResource"]


class DevboxesResource(SyncAPIResource):
    @cached_property
    def logs(self) -> LogsResource:
        return LogsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DevboxesResourceWithRawResponse:
        return DevboxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DevboxesResourceWithStreamingResponse:
        return DevboxesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        blueprint_id: str | NotGiven = NOT_GIVEN,
        blueprint_name: str | NotGiven = NOT_GIVEN,
        code_handle: str | NotGiven = NOT_GIVEN,
        entrypoint: str | NotGiven = NOT_GIVEN,
        environment_variables: Dict[str, str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        setup_commands: List[str] | NotGiven = NOT_GIVEN,
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

          code_handle: (Optional) Id of a code handle to mount to devbox.

          entrypoint: (Optional) When specified, the Devbox will run this script as its main
              executable. The devbox lifecycle will be bound to entrypoint, shutting down when
              the process is complete.

          environment_variables: (Optional) Environment variables used to configure your Devbox.

          name: (Optional) A user specified name to give the Devbox.

          setup_commands: (Optional) List of commands needed to set up your Devbox. Examples might include
              fetching a tool or building your dependencies. Runloop will look optimize these
              steps for you.

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
                    "code_handle": code_handle,
                    "entrypoint": entrypoint,
                    "environment_variables": environment_variables,
                    "name": name,
                    "setup_commands": setup_commands,
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
        limit: str | NotGiven = NOT_GIVEN,
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

    def execute_sync(
        self,
        id: str,
        *,
        command: str | NotGiven = NOT_GIVEN,
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

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/execute_sync",
            body=maybe_transform({"command": command}, devbox_execute_sync_params.DevboxExecuteSyncParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxExecutionDetailView,
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


class AsyncDevboxesResource(AsyncAPIResource):
    @cached_property
    def logs(self) -> AsyncLogsResource:
        return AsyncLogsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDevboxesResourceWithRawResponse:
        return AsyncDevboxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDevboxesResourceWithStreamingResponse:
        return AsyncDevboxesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        blueprint_id: str | NotGiven = NOT_GIVEN,
        blueprint_name: str | NotGiven = NOT_GIVEN,
        code_handle: str | NotGiven = NOT_GIVEN,
        entrypoint: str | NotGiven = NOT_GIVEN,
        environment_variables: Dict[str, str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        setup_commands: List[str] | NotGiven = NOT_GIVEN,
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

          code_handle: (Optional) Id of a code handle to mount to devbox.

          entrypoint: (Optional) When specified, the Devbox will run this script as its main
              executable. The devbox lifecycle will be bound to entrypoint, shutting down when
              the process is complete.

          environment_variables: (Optional) Environment variables used to configure your Devbox.

          name: (Optional) A user specified name to give the Devbox.

          setup_commands: (Optional) List of commands needed to set up your Devbox. Examples might include
              fetching a tool or building your dependencies. Runloop will look optimize these
              steps for you.

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
                    "code_handle": code_handle,
                    "entrypoint": entrypoint,
                    "environment_variables": environment_variables,
                    "name": name,
                    "setup_commands": setup_commands,
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
        limit: str | NotGiven = NOT_GIVEN,
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

    async def execute_sync(
        self,
        id: str,
        *,
        command: str | NotGiven = NOT_GIVEN,
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

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/execute_sync",
            body=await async_maybe_transform({"command": command}, devbox_execute_sync_params.DevboxExecuteSyncParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DevboxExecutionDetailView,
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
        self.execute_sync = to_raw_response_wrapper(
            devboxes.execute_sync,
        )
        self.shutdown = to_raw_response_wrapper(
            devboxes.shutdown,
        )

    @cached_property
    def logs(self) -> LogsResourceWithRawResponse:
        return LogsResourceWithRawResponse(self._devboxes.logs)


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
        self.execute_sync = async_to_raw_response_wrapper(
            devboxes.execute_sync,
        )
        self.shutdown = async_to_raw_response_wrapper(
            devboxes.shutdown,
        )

    @cached_property
    def logs(self) -> AsyncLogsResourceWithRawResponse:
        return AsyncLogsResourceWithRawResponse(self._devboxes.logs)


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
        self.execute_sync = to_streamed_response_wrapper(
            devboxes.execute_sync,
        )
        self.shutdown = to_streamed_response_wrapper(
            devboxes.shutdown,
        )

    @cached_property
    def logs(self) -> LogsResourceWithStreamingResponse:
        return LogsResourceWithStreamingResponse(self._devboxes.logs)


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
        self.execute_sync = async_to_streamed_response_wrapper(
            devboxes.execute_sync,
        )
        self.shutdown = async_to_streamed_response_wrapper(
            devboxes.shutdown,
        )

    @cached_property
    def logs(self) -> AsyncLogsResourceWithStreamingResponse:
        return AsyncLogsResourceWithStreamingResponse(self._devboxes.logs)
