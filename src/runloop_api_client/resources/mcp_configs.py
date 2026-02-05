# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import mcp_config_list_params, mcp_config_create_params, mcp_config_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncMcpConfigsCursorIDPage, AsyncMcpConfigsCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.mcp_config_view import McpConfigView

__all__ = ["McpConfigsResource", "AsyncMcpConfigsResource"]


class McpConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> McpConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return McpConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> McpConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return McpConfigsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        allowed_tools: SequenceNotStr[str],
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
    ) -> McpConfigView:
        """
        [Beta] Create a new McpConfig to connect to an upstream MCP (Model Context
        Protocol) server. The config specifies the target endpoint and which tools are
        allowed.

        Args:
          allowed_tools:
              Glob patterns specifying which tools are allowed from this MCP server. Examples:
              ['*'] for all tools, ['github.search_*', 'github.get_*'] for specific patterns.

          endpoint: The target MCP server endpoint URL (e.g., 'https://mcp.example.com').

          name: The human-readable name for the McpConfig. Must be unique within your account.
              The first segment before '-' is used as the service name for tool routing (e.g.,
              'github-readonly' uses 'github' as the service name).

          description: Optional description for this MCP configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/mcp-configs",
            body=maybe_transform(
                {
                    "allowed_tools": allowed_tools,
                    "endpoint": endpoint,
                    "name": name,
                    "description": description,
                },
                mcp_config_create_params.McpConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=McpConfigView,
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
    ) -> McpConfigView:
        """
        [Beta] Get a specific McpConfig by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/mcp-configs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=McpConfigView,
        )

    def update(
        self,
        id: str,
        *,
        allowed_tools: Optional[SequenceNotStr[str]] | Omit = omit,
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
    ) -> McpConfigView:
        """[Beta] Update an existing McpConfig.

        All fields are optional.

        Args:
          allowed_tools: New glob patterns specifying which tools are allowed. Examples: ['*'] for all
              tools, ['github.search_*'] for specific patterns.

          description: New description for this MCP configuration.

          endpoint: New target MCP server endpoint URL.

          name: New name for the McpConfig. Must be unique within your account.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/mcp-configs/{id}",
            body=maybe_transform(
                {
                    "allowed_tools": allowed_tools,
                    "description": description,
                    "endpoint": endpoint,
                    "name": name,
                },
                mcp_config_update_params.McpConfigUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=McpConfigView,
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
    ) -> SyncMcpConfigsCursorIDPage[McpConfigView]:
        """
        [Beta] List all McpConfigs for the authenticated account.

        Args:
          id: Filter by ID.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name (prefix match supported).

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/mcp-configs",
            page=SyncMcpConfigsCursorIDPage[McpConfigView],
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
                    mcp_config_list_params.McpConfigListParams,
                ),
            ),
            model=McpConfigView,
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
    ) -> McpConfigView:
        """[Beta] Delete an existing McpConfig.

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
            f"/v1/mcp-configs/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=McpConfigView,
        )


class AsyncMcpConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMcpConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMcpConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMcpConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncMcpConfigsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        allowed_tools: SequenceNotStr[str],
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
    ) -> McpConfigView:
        """
        [Beta] Create a new McpConfig to connect to an upstream MCP (Model Context
        Protocol) server. The config specifies the target endpoint and which tools are
        allowed.

        Args:
          allowed_tools:
              Glob patterns specifying which tools are allowed from this MCP server. Examples:
              ['*'] for all tools, ['github.search_*', 'github.get_*'] for specific patterns.

          endpoint: The target MCP server endpoint URL (e.g., 'https://mcp.example.com').

          name: The human-readable name for the McpConfig. Must be unique within your account.
              The first segment before '-' is used as the service name for tool routing (e.g.,
              'github-readonly' uses 'github' as the service name).

          description: Optional description for this MCP configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/mcp-configs",
            body=await async_maybe_transform(
                {
                    "allowed_tools": allowed_tools,
                    "endpoint": endpoint,
                    "name": name,
                    "description": description,
                },
                mcp_config_create_params.McpConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=McpConfigView,
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
    ) -> McpConfigView:
        """
        [Beta] Get a specific McpConfig by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/mcp-configs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=McpConfigView,
        )

    async def update(
        self,
        id: str,
        *,
        allowed_tools: Optional[SequenceNotStr[str]] | Omit = omit,
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
    ) -> McpConfigView:
        """[Beta] Update an existing McpConfig.

        All fields are optional.

        Args:
          allowed_tools: New glob patterns specifying which tools are allowed. Examples: ['*'] for all
              tools, ['github.search_*'] for specific patterns.

          description: New description for this MCP configuration.

          endpoint: New target MCP server endpoint URL.

          name: New name for the McpConfig. Must be unique within your account.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/mcp-configs/{id}",
            body=await async_maybe_transform(
                {
                    "allowed_tools": allowed_tools,
                    "description": description,
                    "endpoint": endpoint,
                    "name": name,
                },
                mcp_config_update_params.McpConfigUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=McpConfigView,
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
    ) -> AsyncPaginator[McpConfigView, AsyncMcpConfigsCursorIDPage[McpConfigView]]:
        """
        [Beta] List all McpConfigs for the authenticated account.

        Args:
          id: Filter by ID.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name (prefix match supported).

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/mcp-configs",
            page=AsyncMcpConfigsCursorIDPage[McpConfigView],
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
                    mcp_config_list_params.McpConfigListParams,
                ),
            ),
            model=McpConfigView,
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
    ) -> McpConfigView:
        """[Beta] Delete an existing McpConfig.

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
            f"/v1/mcp-configs/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=McpConfigView,
        )


class McpConfigsResourceWithRawResponse:
    def __init__(self, mcp_configs: McpConfigsResource) -> None:
        self._mcp_configs = mcp_configs

        self.create = to_raw_response_wrapper(
            mcp_configs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            mcp_configs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            mcp_configs.update,
        )
        self.list = to_raw_response_wrapper(
            mcp_configs.list,
        )
        self.delete = to_raw_response_wrapper(
            mcp_configs.delete,
        )


class AsyncMcpConfigsResourceWithRawResponse:
    def __init__(self, mcp_configs: AsyncMcpConfigsResource) -> None:
        self._mcp_configs = mcp_configs

        self.create = async_to_raw_response_wrapper(
            mcp_configs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            mcp_configs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            mcp_configs.update,
        )
        self.list = async_to_raw_response_wrapper(
            mcp_configs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            mcp_configs.delete,
        )


class McpConfigsResourceWithStreamingResponse:
    def __init__(self, mcp_configs: McpConfigsResource) -> None:
        self._mcp_configs = mcp_configs

        self.create = to_streamed_response_wrapper(
            mcp_configs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            mcp_configs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            mcp_configs.update,
        )
        self.list = to_streamed_response_wrapper(
            mcp_configs.list,
        )
        self.delete = to_streamed_response_wrapper(
            mcp_configs.delete,
        )


class AsyncMcpConfigsResourceWithStreamingResponse:
    def __init__(self, mcp_configs: AsyncMcpConfigsResource) -> None:
        self._mcp_configs = mcp_configs

        self.create = async_to_streamed_response_wrapper(
            mcp_configs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            mcp_configs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            mcp_configs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            mcp_configs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            mcp_configs.delete,
        )
