# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .spans import (
    SpansResource,
    AsyncSpansResource,
    SpansResourceWithRawResponse,
    AsyncSpansResourceWithRawResponse,
    SpansResourceWithStreamingResponse,
    AsyncSpansResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import (
    make_request_options,
)
from ....types.shared.function_invocation_detail_view import FunctionInvocationDetailView
from ....types.functions.function_invocation_list_view import FunctionInvocationListView

__all__ = ["InvocationsResource", "AsyncInvocationsResource"]


class InvocationsResource(SyncAPIResource):
    @cached_property
    def spans(self) -> SpansResource:
        return SpansResource(self._client)

    @cached_property
    def with_raw_response(self) -> InvocationsResourceWithRawResponse:
        return InvocationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InvocationsResourceWithStreamingResponse:
        return InvocationsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        invocation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvocationDetailView:
        """Get the details of a function invocation.

        This includes the status, response,
        and error message.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invocation_id:
            raise ValueError(f"Expected a non-empty value for `invocation_id` but received {invocation_id!r}")
        return self._get(
            f"/v1/functions/invocations/{invocation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvocationDetailView,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvocationListView:
        """List the functions invocations that are available for invocation."""
        return self._get(
            "/v1/functions/invocations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvocationListView,
        )

    def kill(
        self,
        invocation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Kill the invocation with the given ID.

        This will stop the function execution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invocation_id:
            raise ValueError(f"Expected a non-empty value for `invocation_id` but received {invocation_id!r}")
        return self._post(
            f"/v1/functions/invocations/{invocation_id}/kill",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncInvocationsResource(AsyncAPIResource):
    @cached_property
    def spans(self) -> AsyncSpansResource:
        return AsyncSpansResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncInvocationsResourceWithRawResponse:
        return AsyncInvocationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInvocationsResourceWithStreamingResponse:
        return AsyncInvocationsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        invocation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvocationDetailView:
        """Get the details of a function invocation.

        This includes the status, response,
        and error message.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invocation_id:
            raise ValueError(f"Expected a non-empty value for `invocation_id` but received {invocation_id!r}")
        return await self._get(
            f"/v1/functions/invocations/{invocation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvocationDetailView,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionInvocationListView:
        """List the functions invocations that are available for invocation."""
        return await self._get(
            "/v1/functions/invocations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionInvocationListView,
        )

    async def kill(
        self,
        invocation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Kill the invocation with the given ID.

        This will stop the function execution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invocation_id:
            raise ValueError(f"Expected a non-empty value for `invocation_id` but received {invocation_id!r}")
        return await self._post(
            f"/v1/functions/invocations/{invocation_id}/kill",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class InvocationsResourceWithRawResponse:
    def __init__(self, invocations: InvocationsResource) -> None:
        self._invocations = invocations

        self.retrieve = to_raw_response_wrapper(
            invocations.retrieve,
        )
        self.list = to_raw_response_wrapper(
            invocations.list,
        )
        self.kill = to_raw_response_wrapper(
            invocations.kill,
        )

    @cached_property
    def spans(self) -> SpansResourceWithRawResponse:
        return SpansResourceWithRawResponse(self._invocations.spans)


class AsyncInvocationsResourceWithRawResponse:
    def __init__(self, invocations: AsyncInvocationsResource) -> None:
        self._invocations = invocations

        self.retrieve = async_to_raw_response_wrapper(
            invocations.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            invocations.list,
        )
        self.kill = async_to_raw_response_wrapper(
            invocations.kill,
        )

    @cached_property
    def spans(self) -> AsyncSpansResourceWithRawResponse:
        return AsyncSpansResourceWithRawResponse(self._invocations.spans)


class InvocationsResourceWithStreamingResponse:
    def __init__(self, invocations: InvocationsResource) -> None:
        self._invocations = invocations

        self.retrieve = to_streamed_response_wrapper(
            invocations.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            invocations.list,
        )
        self.kill = to_streamed_response_wrapper(
            invocations.kill,
        )

    @cached_property
    def spans(self) -> SpansResourceWithStreamingResponse:
        return SpansResourceWithStreamingResponse(self._invocations.spans)


class AsyncInvocationsResourceWithStreamingResponse:
    def __init__(self, invocations: AsyncInvocationsResource) -> None:
        self._invocations = invocations

        self.retrieve = async_to_streamed_response_wrapper(
            invocations.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            invocations.list,
        )
        self.kill = async_to_streamed_response_wrapper(
            invocations.kill,
        )

    @cached_property
    def spans(self) -> AsyncSpansResourceWithStreamingResponse:
        return AsyncSpansResourceWithStreamingResponse(self._invocations.spans)
