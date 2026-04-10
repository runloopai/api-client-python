# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import apikey_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.api_key_created_view import APIKeyCreatedView

__all__ = ["ApikeysResource", "AsyncApikeysResource"]


class ApikeysResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApikeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return ApikeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApikeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return ApikeysResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        expires_at_ms: Optional[int] | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> APIKeyCreatedView:
        """Create a new API key for the authenticated account.

        Use a standard API key (ak*)
        or a restricted key (rk*) with RESOURCE_TYPE_ACCOUNT write scope.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/apikeys",
            body=maybe_transform(
                {
                    "expires_at_ms": expires_at_ms,
                    "name": name,
                },
                apikey_create_params.ApikeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=APIKeyCreatedView,
        )


class AsyncApikeysResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApikeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApikeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApikeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncApikeysResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        expires_at_ms: Optional[int] | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> APIKeyCreatedView:
        """Create a new API key for the authenticated account.

        Use a standard API key (ak*)
        or a restricted key (rk*) with RESOURCE_TYPE_ACCOUNT write scope.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/apikeys",
            body=await async_maybe_transform(
                {
                    "expires_at_ms": expires_at_ms,
                    "name": name,
                },
                apikey_create_params.ApikeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=APIKeyCreatedView,
        )


class ApikeysResourceWithRawResponse:
    def __init__(self, apikeys: ApikeysResource) -> None:
        self._apikeys = apikeys

        self.create = to_raw_response_wrapper(
            apikeys.create,
        )


class AsyncApikeysResourceWithRawResponse:
    def __init__(self, apikeys: AsyncApikeysResource) -> None:
        self._apikeys = apikeys

        self.create = async_to_raw_response_wrapper(
            apikeys.create,
        )


class ApikeysResourceWithStreamingResponse:
    def __init__(self, apikeys: ApikeysResource) -> None:
        self._apikeys = apikeys

        self.create = to_streamed_response_wrapper(
            apikeys.create,
        )


class AsyncApikeysResourceWithStreamingResponse:
    def __init__(self, apikeys: AsyncApikeysResource) -> None:
        self._apikeys = apikeys

        self.create = async_to_streamed_response_wrapper(
            apikeys.create,
        )
