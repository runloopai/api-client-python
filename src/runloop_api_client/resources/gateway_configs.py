# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import gateway_config_list_params, gateway_config_create_params, gateway_config_update_params
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
from ..pagination import SyncGatewayConfigsCursorIDPage, AsyncGatewayConfigsCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.gateway_config_view import GatewayConfigView

__all__ = ["GatewayConfigsResource", "AsyncGatewayConfigsResource"]


class GatewayConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GatewayConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return GatewayConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GatewayConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return GatewayConfigsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        auth_mechanism: gateway_config_create_params.AuthMechanism,
        endpoint: str,
        name: str,
        description: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> GatewayConfigView:
        """
        [Beta] Create a new GatewayConfig to proxy API requests through the credential
        gateway. The config specifies the target endpoint and how credentials should be
        applied.

        Args:
          auth_mechanism: How credentials should be applied to proxied requests. Specify the type
              ('header', 'bearer') and optional key field.

          endpoint: The target endpoint URL (e.g., 'https://api.anthropic.com').

          name: The human-readable name for the GatewayConfig. Must be unique within your
              account.

          description: Optional description for this gateway configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/gateway-configs",
            body=maybe_transform(
                {
                    "auth_mechanism": auth_mechanism,
                    "endpoint": endpoint,
                    "name": name,
                    "description": description,
                },
                gateway_config_create_params.GatewayConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=GatewayConfigView,
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
    ) -> GatewayConfigView:
        """
        [Beta] Get a specific GatewayConfig by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/gateway-configs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GatewayConfigView,
        )

    def update(
        self,
        id: str,
        *,
        auth_mechanism: Optional[gateway_config_update_params.AuthMechanism] | Omit = omit,
        description: Optional[str] | Omit = omit,
        endpoint: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> GatewayConfigView:
        """[Beta] Update an existing GatewayConfig.

        All fields are optional.

        Args:
          auth_mechanism: New authentication mechanism for applying credentials to proxied requests.

          description: New description for this gateway configuration.

          endpoint: New target endpoint URL (e.g., 'https://api.anthropic.com').

          name: New name for the GatewayConfig. Must be unique within your account.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/gateway-configs/{id}",
            body=maybe_transform(
                {
                    "auth_mechanism": auth_mechanism,
                    "description": description,
                    "endpoint": endpoint,
                    "name": name,
                },
                gateway_config_update_params.GatewayConfigUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=GatewayConfigView,
        )

    def list(
        self,
        *,
        id: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncGatewayConfigsCursorIDPage[GatewayConfigView]:
        """
        [Beta] List all GatewayConfigs for the authenticated account, including
        system-provided configs like 'anthropic' and 'openai'.

        Args:
          id: Filter by ID.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name (partial match supported).

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/gateway-configs",
            page=SyncGatewayConfigsCursorIDPage[GatewayConfigView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    gateway_config_list_params.GatewayConfigListParams,
                ),
            ),
            model=GatewayConfigView,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> GatewayConfigView:
        """[Beta] Delete an existing GatewayConfig.

        This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/gateway-configs/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=GatewayConfigView,
        )


class AsyncGatewayConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGatewayConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGatewayConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGatewayConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncGatewayConfigsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        auth_mechanism: gateway_config_create_params.AuthMechanism,
        endpoint: str,
        name: str,
        description: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> GatewayConfigView:
        """
        [Beta] Create a new GatewayConfig to proxy API requests through the credential
        gateway. The config specifies the target endpoint and how credentials should be
        applied.

        Args:
          auth_mechanism: How credentials should be applied to proxied requests. Specify the type
              ('header', 'bearer') and optional key field.

          endpoint: The target endpoint URL (e.g., 'https://api.anthropic.com').

          name: The human-readable name for the GatewayConfig. Must be unique within your
              account.

          description: Optional description for this gateway configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/gateway-configs",
            body=await async_maybe_transform(
                {
                    "auth_mechanism": auth_mechanism,
                    "endpoint": endpoint,
                    "name": name,
                    "description": description,
                },
                gateway_config_create_params.GatewayConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=GatewayConfigView,
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
    ) -> GatewayConfigView:
        """
        [Beta] Get a specific GatewayConfig by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/gateway-configs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GatewayConfigView,
        )

    async def update(
        self,
        id: str,
        *,
        auth_mechanism: Optional[gateway_config_update_params.AuthMechanism] | Omit = omit,
        description: Optional[str] | Omit = omit,
        endpoint: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> GatewayConfigView:
        """[Beta] Update an existing GatewayConfig.

        All fields are optional.

        Args:
          auth_mechanism: New authentication mechanism for applying credentials to proxied requests.

          description: New description for this gateway configuration.

          endpoint: New target endpoint URL (e.g., 'https://api.anthropic.com').

          name: New name for the GatewayConfig. Must be unique within your account.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/gateway-configs/{id}",
            body=await async_maybe_transform(
                {
                    "auth_mechanism": auth_mechanism,
                    "description": description,
                    "endpoint": endpoint,
                    "name": name,
                },
                gateway_config_update_params.GatewayConfigUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=GatewayConfigView,
        )

    def list(
        self,
        *,
        id: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[GatewayConfigView, AsyncGatewayConfigsCursorIDPage[GatewayConfigView]]:
        """
        [Beta] List all GatewayConfigs for the authenticated account, including
        system-provided configs like 'anthropic' and 'openai'.

        Args:
          id: Filter by ID.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name (partial match supported).

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/gateway-configs",
            page=AsyncGatewayConfigsCursorIDPage[GatewayConfigView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    gateway_config_list_params.GatewayConfigListParams,
                ),
            ),
            model=GatewayConfigView,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> GatewayConfigView:
        """[Beta] Delete an existing GatewayConfig.

        This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/gateway-configs/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=GatewayConfigView,
        )


class GatewayConfigsResourceWithRawResponse:
    def __init__(self, gateway_configs: GatewayConfigsResource) -> None:
        self._gateway_configs = gateway_configs

        self.create = to_raw_response_wrapper(
            gateway_configs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            gateway_configs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            gateway_configs.update,
        )
        self.list = to_raw_response_wrapper(
            gateway_configs.list,
        )
        self.delete = to_raw_response_wrapper(
            gateway_configs.delete,
        )


class AsyncGatewayConfigsResourceWithRawResponse:
    def __init__(self, gateway_configs: AsyncGatewayConfigsResource) -> None:
        self._gateway_configs = gateway_configs

        self.create = async_to_raw_response_wrapper(
            gateway_configs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            gateway_configs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            gateway_configs.update,
        )
        self.list = async_to_raw_response_wrapper(
            gateway_configs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            gateway_configs.delete,
        )


class GatewayConfigsResourceWithStreamingResponse:
    def __init__(self, gateway_configs: GatewayConfigsResource) -> None:
        self._gateway_configs = gateway_configs

        self.create = to_streamed_response_wrapper(
            gateway_configs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            gateway_configs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            gateway_configs.update,
        )
        self.list = to_streamed_response_wrapper(
            gateway_configs.list,
        )
        self.delete = to_streamed_response_wrapper(
            gateway_configs.delete,
        )


class AsyncGatewayConfigsResourceWithStreamingResponse:
    def __init__(self, gateway_configs: AsyncGatewayConfigsResource) -> None:
        self._gateway_configs = gateway_configs

        self.create = async_to_streamed_response_wrapper(
            gateway_configs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            gateway_configs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            gateway_configs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            gateway_configs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            gateway_configs.delete,
        )
