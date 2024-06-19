# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ....types.sessions.sessions import kv_list_params
from ....types.sessions.sessions.session_kv import SessionKv

__all__ = ["KvResource", "AsyncKvResource"]


class KvResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> KvResourceWithRawResponse:
        return KvResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KvResourceWithStreamingResponse:
        return KvResourceWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        keys: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SessionKv:
        """
        List the sessions associated with your application.

        Args:
          keys: Filter KV to specific keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            f"/v1/sessions/sessions/{session_id}/kv",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"keys": keys}, kv_list_params.KvListParams),
            ),
            cast_to=SessionKv,
        )


class AsyncKvResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncKvResourceWithRawResponse:
        return AsyncKvResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKvResourceWithStreamingResponse:
        return AsyncKvResourceWithStreamingResponse(self)

    async def list(
        self,
        session_id: str,
        *,
        keys: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SessionKv:
        """
        List the sessions associated with your application.

        Args:
          keys: Filter KV to specific keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            f"/v1/sessions/sessions/{session_id}/kv",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"keys": keys}, kv_list_params.KvListParams),
            ),
            cast_to=SessionKv,
        )


class KvResourceWithRawResponse:
    def __init__(self, kv: KvResource) -> None:
        self._kv = kv

        self.list = to_raw_response_wrapper(
            kv.list,
        )


class AsyncKvResourceWithRawResponse:
    def __init__(self, kv: AsyncKvResource) -> None:
        self._kv = kv

        self.list = async_to_raw_response_wrapper(
            kv.list,
        )


class KvResourceWithStreamingResponse:
    def __init__(self, kv: KvResource) -> None:
        self._kv = kv

        self.list = to_streamed_response_wrapper(
            kv.list,
        )


class AsyncKvResourceWithStreamingResponse:
    def __init__(self, kv: AsyncKvResource) -> None:
        self._kv = kv

        self.list = async_to_streamed_response_wrapper(
            kv.list,
        )
