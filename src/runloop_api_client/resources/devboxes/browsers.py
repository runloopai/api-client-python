# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.devboxes import browser_create_params
from ...types.devboxes.browser_view import BrowserView

__all__ = ["BrowsersResource", "AsyncBrowsersResource"]


class BrowsersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BrowsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return BrowsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BrowsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return BrowsersResourceWithStreamingResponse(self)

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
    ) -> BrowserView:
        """Create a Devbox that has a managed Browser and begin the boot process.

        As part
        of booting the Devbox, the browser will automatically be started with connection
        utilities activated.

        Args:
          name: The name to use for the created Devbox with a Browser.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/devboxes/browsers",
            body=maybe_transform({"name": name}, browser_create_params.BrowserCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BrowserView,
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
    ) -> BrowserView:
        """
        Get Browser Details.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/devboxes/browsers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BrowserView,
        )


class AsyncBrowsersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBrowsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBrowsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBrowsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncBrowsersResourceWithStreamingResponse(self)

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
    ) -> BrowserView:
        """Create a Devbox that has a managed Browser and begin the boot process.

        As part
        of booting the Devbox, the browser will automatically be started with connection
        utilities activated.

        Args:
          name: The name to use for the created Devbox with a Browser.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/devboxes/browsers",
            body=await async_maybe_transform({"name": name}, browser_create_params.BrowserCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BrowserView,
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
    ) -> BrowserView:
        """
        Get Browser Details.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/devboxes/browsers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BrowserView,
        )


class BrowsersResourceWithRawResponse:
    def __init__(self, browsers: BrowsersResource) -> None:
        self._browsers = browsers

        self.create = to_raw_response_wrapper(
            browsers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            browsers.retrieve,
        )


class AsyncBrowsersResourceWithRawResponse:
    def __init__(self, browsers: AsyncBrowsersResource) -> None:
        self._browsers = browsers

        self.create = async_to_raw_response_wrapper(
            browsers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            browsers.retrieve,
        )


class BrowsersResourceWithStreamingResponse:
    def __init__(self, browsers: BrowsersResource) -> None:
        self._browsers = browsers

        self.create = to_streamed_response_wrapper(
            browsers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            browsers.retrieve,
        )


class AsyncBrowsersResourceWithStreamingResponse:
    def __init__(self, browsers: AsyncBrowsersResource) -> None:
        self._browsers = browsers

        self.create = async_to_streamed_response_wrapper(
            browsers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            browsers.retrieve,
        )
