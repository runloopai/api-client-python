# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import (
    make_request_options,
)

__all__ = ["OpenAPIResource", "AsyncOpenAPIResource"]


class OpenAPIResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OpenAPIResourceWithRawResponse:
        return OpenAPIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OpenAPIResourceWithStreamingResponse:
        return OpenAPIResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Get the OpenAPI Spec for this project."""
        return self._get(
            "/v1/functions/openapi",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncOpenAPIResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOpenAPIResourceWithRawResponse:
        return AsyncOpenAPIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOpenAPIResourceWithStreamingResponse:
        return AsyncOpenAPIResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Get the OpenAPI Spec for this project."""
        return await self._get(
            "/v1/functions/openapi",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class OpenAPIResourceWithRawResponse:
    def __init__(self, openapi: OpenAPIResource) -> None:
        self._openapi = openapi

        self.retrieve = to_raw_response_wrapper(
            openapi.retrieve,
        )


class AsyncOpenAPIResourceWithRawResponse:
    def __init__(self, openapi: AsyncOpenAPIResource) -> None:
        self._openapi = openapi

        self.retrieve = async_to_raw_response_wrapper(
            openapi.retrieve,
        )


class OpenAPIResourceWithStreamingResponse:
    def __init__(self, openapi: OpenAPIResource) -> None:
        self._openapi = openapi

        self.retrieve = to_streamed_response_wrapper(
            openapi.retrieve,
        )


class AsyncOpenAPIResourceWithStreamingResponse:
    def __init__(self, openapi: AsyncOpenAPIResource) -> None:
        self._openapi = openapi

        self.retrieve = async_to_streamed_response_wrapper(
            openapi.retrieve,
        )
