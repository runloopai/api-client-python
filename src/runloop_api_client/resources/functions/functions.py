# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import function_invoke_sync_params, function_invoke_async_params
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
from .invocations import (
    InvocationsResource,
    AsyncInvocationsResource,
    InvocationsResourceWithRawResponse,
    AsyncInvocationsResourceWithRawResponse,
    InvocationsResourceWithStreamingResponse,
    AsyncInvocationsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .invocations.invocations import InvocationsResource, AsyncInvocationsResource
from ...types.function_list_view import FunctionListView
from ...types.function_invoke_sync_response import FunctionInvokeSyncResponse
from ...types.function_invoke_async_response import FunctionInvokeAsyncResponse

__all__ = ["FunctionsResource", "AsyncFunctionsResource"]


class FunctionsResource(SyncAPIResource):
    @cached_property
    def invocations(self) -> InvocationsResource:
        return InvocationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> FunctionsResourceWithRawResponse:
        return FunctionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FunctionsResourceWithStreamingResponse:
        return FunctionsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionListView:
        """List the functions that are available for invocation."""
        return self._get(
            "/v1/functions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionListView,
        )

    def invoke_async(
        self,
        function_name: str,
        *,
        project_name: str,
        request: object,
        runloop_meta: function_invoke_async_params.RunloopMeta | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvokeAsyncResponse:
        """Invoke the remote function asynchronously.

        This will return a job id that can be
        used to query the status of the function invocation.

        Args:
          request: Json of the request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_name:
            raise ValueError(f"Expected a non-empty value for `project_name` but received {project_name!r}")
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return self._post(
            f"/v1/functions/{project_name}/{function_name}/invoke_async",
            body=maybe_transform(
                {
                    "request": request,
                    "runloop_meta": runloop_meta,
                },
                function_invoke_async_params.FunctionInvokeAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvokeAsyncResponse,
        )

    def invoke_sync(
        self,
        function_name: str,
        *,
        project_name: str,
        request: object,
        runloop_meta: function_invoke_sync_params.RunloopMeta | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvokeSyncResponse:
        """Invoke the remote function synchronously.

        This will block until the function
        completes and return the result. If the function call takes too long, the
        request will timeout.

        Args:
          request: Json of the request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_name:
            raise ValueError(f"Expected a non-empty value for `project_name` but received {project_name!r}")
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return self._post(
            f"/v1/functions/{project_name}/{function_name}/invoke_sync",
            body=maybe_transform(
                {
                    "request": request,
                    "runloop_meta": runloop_meta,
                },
                function_invoke_sync_params.FunctionInvokeSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvokeSyncResponse,
        )


class AsyncFunctionsResource(AsyncAPIResource):
    @cached_property
    def invocations(self) -> AsyncInvocationsResource:
        return AsyncInvocationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFunctionsResourceWithRawResponse:
        return AsyncFunctionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFunctionsResourceWithStreamingResponse:
        return AsyncFunctionsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionListView:
        """List the functions that are available for invocation."""
        return await self._get(
            "/v1/functions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionListView,
        )

    async def invoke_async(
        self,
        function_name: str,
        *,
        project_name: str,
        request: object,
        runloop_meta: function_invoke_async_params.RunloopMeta | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvokeAsyncResponse:
        """Invoke the remote function asynchronously.

        This will return a job id that can be
        used to query the status of the function invocation.

        Args:
          request: Json of the request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_name:
            raise ValueError(f"Expected a non-empty value for `project_name` but received {project_name!r}")
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return await self._post(
            f"/v1/functions/{project_name}/{function_name}/invoke_async",
            body=await async_maybe_transform(
                {
                    "request": request,
                    "runloop_meta": runloop_meta,
                },
                function_invoke_async_params.FunctionInvokeAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvokeAsyncResponse,
        )

    async def invoke_sync(
        self,
        function_name: str,
        *,
        project_name: str,
        request: object,
        runloop_meta: function_invoke_sync_params.RunloopMeta | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvokeSyncResponse:
        """Invoke the remote function synchronously.

        This will block until the function
        completes and return the result. If the function call takes too long, the
        request will timeout.

        Args:
          request: Json of the request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_name:
            raise ValueError(f"Expected a non-empty value for `project_name` but received {project_name!r}")
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return await self._post(
            f"/v1/functions/{project_name}/{function_name}/invoke_sync",
            body=await async_maybe_transform(
                {
                    "request": request,
                    "runloop_meta": runloop_meta,
                },
                function_invoke_sync_params.FunctionInvokeSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvokeSyncResponse,
        )


class FunctionsResourceWithRawResponse:
    def __init__(self, functions: FunctionsResource) -> None:
        self._functions = functions

        self.list = to_raw_response_wrapper(
            functions.list,
        )
        self.invoke_async = to_raw_response_wrapper(
            functions.invoke_async,
        )
        self.invoke_sync = to_raw_response_wrapper(
            functions.invoke_sync,
        )

    @cached_property
    def invocations(self) -> InvocationsResourceWithRawResponse:
        return InvocationsResourceWithRawResponse(self._functions.invocations)


class AsyncFunctionsResourceWithRawResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

        self.list = async_to_raw_response_wrapper(
            functions.list,
        )
        self.invoke_async = async_to_raw_response_wrapper(
            functions.invoke_async,
        )
        self.invoke_sync = async_to_raw_response_wrapper(
            functions.invoke_sync,
        )

    @cached_property
    def invocations(self) -> AsyncInvocationsResourceWithRawResponse:
        return AsyncInvocationsResourceWithRawResponse(self._functions.invocations)


class FunctionsResourceWithStreamingResponse:
    def __init__(self, functions: FunctionsResource) -> None:
        self._functions = functions

        self.list = to_streamed_response_wrapper(
            functions.list,
        )
        self.invoke_async = to_streamed_response_wrapper(
            functions.invoke_async,
        )
        self.invoke_sync = to_streamed_response_wrapper(
            functions.invoke_sync,
        )

    @cached_property
    def invocations(self) -> InvocationsResourceWithStreamingResponse:
        return InvocationsResourceWithStreamingResponse(self._functions.invocations)


class AsyncFunctionsResourceWithStreamingResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

        self.list = async_to_streamed_response_wrapper(
            functions.list,
        )
        self.invoke_async = async_to_streamed_response_wrapper(
            functions.invoke_async,
        )
        self.invoke_sync = async_to_streamed_response_wrapper(
            functions.invoke_sync,
        )

    @cached_property
    def invocations(self) -> AsyncInvocationsResourceWithStreamingResponse:
        return AsyncInvocationsResourceWithStreamingResponse(self._functions.invocations)
