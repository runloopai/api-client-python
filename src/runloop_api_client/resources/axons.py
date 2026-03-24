# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import axon_publish_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options
from ..types.axon_view import AxonView
from ..types.axon_list_view import AxonListView
from ..types.axon_event_view import AxonEventView
from ..types.publish_result_view import PublishResultView

__all__ = ["AxonsResource", "AsyncAxonsResource"]


class AxonsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AxonsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AxonsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AxonsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AxonsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AxonView:
        """[Beta] Create a new axon."""
        return self._post(
            "/v1/axons",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=AxonView,
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
    ) -> AxonView:
        """
        [Beta] Get an axon given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/axons/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonView,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AxonListView:
        """[Beta] List all active axons."""
        return self._get(
            "/v1/axons",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonListView,
        )

    def publish(
        self,
        id: str,
        *,
        event_type: str,
        origin: Literal["EXTERNAL_EVENT", "AGENT_EVENT", "USER_EVENT"],
        payload: str,
        source: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PublishResultView:
        """
        [Beta] Publish an event to a specified axon.

        Args:
          event_type: The event type (e.g. push, pull_request).

          origin: Event origin.

          payload: Event payload.

          source: The source of the event (e.g. github, slack).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/axons/{id}/publish", id=id),
            body=maybe_transform(
                {
                    "event_type": event_type,
                    "origin": origin,
                    "payload": payload,
                    "source": source,
                },
                axon_publish_params.AxonPublishParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PublishResultView,
        )

    def subscribe_sse(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[AxonEventView]:
        """
        [Beta] Subscribe to an axon event stream via server-sent events.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/axons/{id}/subscribe/sse", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonEventView,
            stream=True,
            stream_cls=Stream[AxonEventView],
        )


class AsyncAxonsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAxonsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAxonsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAxonsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncAxonsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AxonView:
        """[Beta] Create a new axon."""
        return await self._post(
            "/v1/axons",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=AxonView,
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
    ) -> AxonView:
        """
        [Beta] Get an axon given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/axons/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonView,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AxonListView:
        """[Beta] List all active axons."""
        return await self._get(
            "/v1/axons",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonListView,
        )

    async def publish(
        self,
        id: str,
        *,
        event_type: str,
        origin: Literal["EXTERNAL_EVENT", "AGENT_EVENT", "USER_EVENT"],
        payload: str,
        source: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PublishResultView:
        """
        [Beta] Publish an event to a specified axon.

        Args:
          event_type: The event type (e.g. push, pull_request).

          origin: Event origin.

          payload: Event payload.

          source: The source of the event (e.g. github, slack).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/axons/{id}/publish", id=id),
            body=await async_maybe_transform(
                {
                    "event_type": event_type,
                    "origin": origin,
                    "payload": payload,
                    "source": source,
                },
                axon_publish_params.AxonPublishParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PublishResultView,
        )

    async def subscribe_sse(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[AxonEventView]:
        """
        [Beta] Subscribe to an axon event stream via server-sent events.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/axons/{id}/subscribe/sse", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonEventView,
            stream=True,
            stream_cls=AsyncStream[AxonEventView],
        )


class AxonsResourceWithRawResponse:
    def __init__(self, axons: AxonsResource) -> None:
        self._axons = axons

        self.create = to_raw_response_wrapper(
            axons.create,
        )
        self.retrieve = to_raw_response_wrapper(
            axons.retrieve,
        )
        self.list = to_raw_response_wrapper(
            axons.list,
        )
        self.publish = to_raw_response_wrapper(
            axons.publish,
        )
        self.subscribe_sse = to_raw_response_wrapper(
            axons.subscribe_sse,
        )


class AsyncAxonsResourceWithRawResponse:
    def __init__(self, axons: AsyncAxonsResource) -> None:
        self._axons = axons

        self.create = async_to_raw_response_wrapper(
            axons.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            axons.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            axons.list,
        )
        self.publish = async_to_raw_response_wrapper(
            axons.publish,
        )
        self.subscribe_sse = async_to_raw_response_wrapper(
            axons.subscribe_sse,
        )


class AxonsResourceWithStreamingResponse:
    def __init__(self, axons: AxonsResource) -> None:
        self._axons = axons

        self.create = to_streamed_response_wrapper(
            axons.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            axons.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            axons.list,
        )
        self.publish = to_streamed_response_wrapper(
            axons.publish,
        )
        self.subscribe_sse = to_streamed_response_wrapper(
            axons.subscribe_sse,
        )


class AsyncAxonsResourceWithStreamingResponse:
    def __init__(self, axons: AsyncAxonsResource) -> None:
        self._axons = axons

        self.create = async_to_streamed_response_wrapper(
            axons.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            axons.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            axons.list,
        )
        self.publish = async_to_streamed_response_wrapper(
            axons.publish,
        )
        self.subscribe_sse = async_to_streamed_response_wrapper(
            axons.subscribe_sse,
        )
