# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from .sql import (
    SqlResource,
    AsyncSqlResource,
    SqlResourceWithRawResponse,
    AsyncSqlResourceWithRawResponse,
    SqlResourceWithStreamingResponse,
    AsyncSqlResourceWithStreamingResponse,
)
from ...types import axon_list_params, axon_create_params, axon_publish_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._streaming import Stream, AsyncStream
from ...pagination import SyncAxonsCursorIDPage, AsyncAxonsCursorIDPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.axon_view import AxonView
from ...types.axon_event_view import AxonEventView
from ...types.publish_result_view import PublishResultView

__all__ = ["AxonsResource", "AsyncAxonsResource"]


class AxonsResource(SyncAPIResource):
    @cached_property
    def sql(self) -> SqlResource:
        return SqlResource(self._client)

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
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AxonView:
        """
        [Beta] Create a new axon.

        Args:
          name: (Optional) Name for the axon.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/axons",
            body=maybe_transform({"name": name}, axon_create_params.AxonCreateParams),
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
        id: str | Omit = omit,
        include_total_count: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncAxonsCursorIDPage[AxonView]:
        """
        [Beta] List all active axons.

        Args:
          id: Filter by axon ID.

          include_total_count: If true (default), includes total_count in the response. Set to false to skip
              the count query for better performance on large datasets.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by axon name (prefix match supported).

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/axons",
            page=SyncAxonsCursorIDPage[AxonView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "include_total_count": include_total_count,
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    axon_list_params.AxonListParams,
                ),
            ),
            model=AxonView,
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
        default_headers: Headers = {"Accept": "text/event-stream"}
        merged_headers = default_headers if extra_headers is None else {**default_headers, **extra_headers}
        return self._get(
            path_template("/v1/axons/{id}/subscribe/sse", id=id),
            options=make_request_options(
                extra_headers=merged_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AxonEventView,
            stream=True,
            stream_cls=Stream[AxonEventView],
        )


class AsyncAxonsResource(AsyncAPIResource):
    @cached_property
    def sql(self) -> AsyncSqlResource:
        return AsyncSqlResource(self._client)

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
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AxonView:
        """
        [Beta] Create a new axon.

        Args:
          name: (Optional) Name for the axon.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/axons",
            body=await async_maybe_transform({"name": name}, axon_create_params.AxonCreateParams),
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

    def list(
        self,
        *,
        id: str | Omit = omit,
        include_total_count: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AxonView, AsyncAxonsCursorIDPage[AxonView]]:
        """
        [Beta] List all active axons.

        Args:
          id: Filter by axon ID.

          include_total_count: If true (default), includes total_count in the response. Set to false to skip
              the count query for better performance on large datasets.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by axon name (prefix match supported).

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/axons",
            page=AsyncAxonsCursorIDPage[AxonView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "include_total_count": include_total_count,
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    axon_list_params.AxonListParams,
                ),
            ),
            model=AxonView,
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
        default_headers: Headers = {"Accept": "text/event-stream"}
        merged_headers = default_headers if extra_headers is None else {**default_headers, **extra_headers}
        return await self._get(
            path_template("/v1/axons/{id}/subscribe/sse", id=id),
            options=make_request_options(
                extra_headers=merged_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
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

    @cached_property
    def sql(self) -> SqlResourceWithRawResponse:
        return SqlResourceWithRawResponse(self._axons.sql)


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

    @cached_property
    def sql(self) -> AsyncSqlResourceWithRawResponse:
        return AsyncSqlResourceWithRawResponse(self._axons.sql)


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

    @cached_property
    def sql(self) -> SqlResourceWithStreamingResponse:
        return SqlResourceWithStreamingResponse(self._axons.sql)


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

    @cached_property
    def sql(self) -> AsyncSqlResourceWithStreamingResponse:
        return AsyncSqlResourceWithStreamingResponse(self._axons.sql)
