# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import agent_list_params, agent_create_params
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
from ..pagination import SyncAgentsCursorIDPage, AsyncAgentsCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.agent_view import AgentView
from ..types.shared_params.agent_source import AgentSource

__all__ = ["AgentsResource", "AsyncAgentsResource"]


class AgentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AgentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        source: Optional[AgentSource] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AgentView:
        """Create a new Agent with a name and optional public visibility.

        The Agent will be
        assigned a unique ID.

        Args:
          name: The name of the Agent.

          source: The source configuration for the Agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/agents",
            body=maybe_transform(
                {
                    "name": name,
                    "source": source,
                },
                agent_create_params.AgentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=AgentView,
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
    ) -> AgentView:
        """
        Retrieve a specific Agent by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/agents/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentView,
        )

    def list(
        self,
        *,
        is_public: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncAgentsCursorIDPage[AgentView]:
        """
        List all Agents for the authenticated account with pagination support.

        Args:
          is_public: Filter agents by public visibility.

          limit: The limit of items to return. Default is 20.

          name: Filter agents by name (partial match supported).

          search: Search by agent ID or name.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/agents",
            page=SyncAgentsCursorIDPage[AgentView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "is_public": is_public,
                        "limit": limit,
                        "name": name,
                        "search": search,
                        "starting_after": starting_after,
                    },
                    agent_list_params.AgentListParams,
                ),
            ),
            model=AgentView,
        )


class AsyncAgentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncAgentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        source: Optional[AgentSource] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AgentView:
        """Create a new Agent with a name and optional public visibility.

        The Agent will be
        assigned a unique ID.

        Args:
          name: The name of the Agent.

          source: The source configuration for the Agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/agents",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "source": source,
                },
                agent_create_params.AgentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=AgentView,
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
    ) -> AgentView:
        """
        Retrieve a specific Agent by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/agents/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentView,
        )

    def list(
        self,
        *,
        is_public: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AgentView, AsyncAgentsCursorIDPage[AgentView]]:
        """
        List all Agents for the authenticated account with pagination support.

        Args:
          is_public: Filter agents by public visibility.

          limit: The limit of items to return. Default is 20.

          name: Filter agents by name (partial match supported).

          search: Search by agent ID or name.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/agents",
            page=AsyncAgentsCursorIDPage[AgentView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "is_public": is_public,
                        "limit": limit,
                        "name": name,
                        "search": search,
                        "starting_after": starting_after,
                    },
                    agent_list_params.AgentListParams,
                ),
            ),
            model=AgentView,
        )


class AgentsResourceWithRawResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.create = to_raw_response_wrapper(
            agents.create,
        )
        self.retrieve = to_raw_response_wrapper(
            agents.retrieve,
        )
        self.list = to_raw_response_wrapper(
            agents.list,
        )


class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.create = async_to_raw_response_wrapper(
            agents.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            agents.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            agents.list,
        )


class AgentsResourceWithStreamingResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.create = to_streamed_response_wrapper(
            agents.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            agents.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            agents.list,
        )


class AsyncAgentsResourceWithStreamingResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.create = async_to_streamed_response_wrapper(
            agents.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            agents.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            agents.list,
        )
