# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import network_policy_list_params, network_policy_create_params, network_policy_update_params
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
from ..pagination import SyncNetworkPoliciesCursorIDPage, AsyncNetworkPoliciesCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.network_policy_view import NetworkPolicyView

__all__ = ["NetworkPoliciesResource", "AsyncNetworkPoliciesResource"]


class NetworkPoliciesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NetworkPoliciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return NetworkPoliciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NetworkPoliciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return NetworkPoliciesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        allow_all: Optional[bool] | Omit = omit,
        allow_devbox_to_devbox: Optional[bool] | Omit = omit,
        allowed_hostnames: Optional[SequenceNotStr[str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NetworkPolicyView:
        """Create a new NetworkPolicy with the specified egress rules.

        The policy can then
        be applied to blueprints, devboxes, or snapshot resumes.

        Args:
          name: The human-readable name for the NetworkPolicy. Must be unique within the
              account.

          allow_all: (Optional) If true, all egress traffic is allowed (ALLOW_ALL policy). Defaults
              to false.

          allow_devbox_to_devbox: (Optional) If true, allows traffic between the account's own devboxes via
              tunnels. Defaults to false. If allow_all is true, this is automatically set to
              true.

          allowed_hostnames: (Optional) DNS-based allow list with wildcard support. Examples: ['github.com',
              '*.npmjs.org'].

          description: Optional description for the NetworkPolicy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/network-policies",
            body=maybe_transform(
                {
                    "name": name,
                    "allow_all": allow_all,
                    "allow_devbox_to_devbox": allow_devbox_to_devbox,
                    "allowed_hostnames": allowed_hostnames,
                    "description": description,
                },
                network_policy_create_params.NetworkPolicyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NetworkPolicyView,
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
    ) -> NetworkPolicyView:
        """
        Get a specific NetworkPolicy by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/network-policies/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NetworkPolicyView,
        )

    def update(
        self,
        id: str,
        *,
        allow_all: Optional[bool] | Omit = omit,
        allow_devbox_to_devbox: Optional[bool] | Omit = omit,
        allowed_hostnames: Optional[SequenceNotStr[str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NetworkPolicyView:
        """Update an existing NetworkPolicy.

        All fields are optional.

        Args:
          allow_all: If true, all egress traffic is allowed (ALLOW_ALL policy).

          allow_devbox_to_devbox: If true, allows traffic between the account's own devboxes via tunnels.

          allowed_hostnames: Updated DNS-based allow list with wildcard support. Examples: ['github.com',
              '*.npmjs.org'].

          description: Updated description for the NetworkPolicy.

          name: Updated human-readable name for the NetworkPolicy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/network-policies/{id}",
            body=maybe_transform(
                {
                    "allow_all": allow_all,
                    "allow_devbox_to_devbox": allow_devbox_to_devbox,
                    "allowed_hostnames": allowed_hostnames,
                    "description": description,
                    "name": name,
                },
                network_policy_update_params.NetworkPolicyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NetworkPolicyView,
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
    ) -> SyncNetworkPoliciesCursorIDPage[NetworkPolicyView]:
        """
        List all NetworkPolicies for the authenticated account.

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
            "/v1/network-policies",
            page=SyncNetworkPoliciesCursorIDPage[NetworkPolicyView],
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
                    network_policy_list_params.NetworkPolicyListParams,
                ),
            ),
            model=NetworkPolicyView,
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
    ) -> NetworkPolicyView:
        """Delete an existing NetworkPolicy.

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
            f"/v1/network-policies/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NetworkPolicyView,
        )


class AsyncNetworkPoliciesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNetworkPoliciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncNetworkPoliciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNetworkPoliciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncNetworkPoliciesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        allow_all: Optional[bool] | Omit = omit,
        allow_devbox_to_devbox: Optional[bool] | Omit = omit,
        allowed_hostnames: Optional[SequenceNotStr[str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NetworkPolicyView:
        """Create a new NetworkPolicy with the specified egress rules.

        The policy can then
        be applied to blueprints, devboxes, or snapshot resumes.

        Args:
          name: The human-readable name for the NetworkPolicy. Must be unique within the
              account.

          allow_all: (Optional) If true, all egress traffic is allowed (ALLOW_ALL policy). Defaults
              to false.

          allow_devbox_to_devbox: (Optional) If true, allows traffic between the account's own devboxes via
              tunnels. Defaults to false. If allow_all is true, this is automatically set to
              true.

          allowed_hostnames: (Optional) DNS-based allow list with wildcard support. Examples: ['github.com',
              '*.npmjs.org'].

          description: Optional description for the NetworkPolicy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/network-policies",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "allow_all": allow_all,
                    "allow_devbox_to_devbox": allow_devbox_to_devbox,
                    "allowed_hostnames": allowed_hostnames,
                    "description": description,
                },
                network_policy_create_params.NetworkPolicyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NetworkPolicyView,
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
    ) -> NetworkPolicyView:
        """
        Get a specific NetworkPolicy by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/network-policies/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NetworkPolicyView,
        )

    async def update(
        self,
        id: str,
        *,
        allow_all: Optional[bool] | Omit = omit,
        allow_devbox_to_devbox: Optional[bool] | Omit = omit,
        allowed_hostnames: Optional[SequenceNotStr[str]] | Omit = omit,
        description: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NetworkPolicyView:
        """Update an existing NetworkPolicy.

        All fields are optional.

        Args:
          allow_all: If true, all egress traffic is allowed (ALLOW_ALL policy).

          allow_devbox_to_devbox: If true, allows traffic between the account's own devboxes via tunnels.

          allowed_hostnames: Updated DNS-based allow list with wildcard support. Examples: ['github.com',
              '*.npmjs.org'].

          description: Updated description for the NetworkPolicy.

          name: Updated human-readable name for the NetworkPolicy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/network-policies/{id}",
            body=await async_maybe_transform(
                {
                    "allow_all": allow_all,
                    "allow_devbox_to_devbox": allow_devbox_to_devbox,
                    "allowed_hostnames": allowed_hostnames,
                    "description": description,
                    "name": name,
                },
                network_policy_update_params.NetworkPolicyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NetworkPolicyView,
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
    ) -> AsyncPaginator[NetworkPolicyView, AsyncNetworkPoliciesCursorIDPage[NetworkPolicyView]]:
        """
        List all NetworkPolicies for the authenticated account.

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
            "/v1/network-policies",
            page=AsyncNetworkPoliciesCursorIDPage[NetworkPolicyView],
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
                    network_policy_list_params.NetworkPolicyListParams,
                ),
            ),
            model=NetworkPolicyView,
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
    ) -> NetworkPolicyView:
        """Delete an existing NetworkPolicy.

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
            f"/v1/network-policies/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NetworkPolicyView,
        )


class NetworkPoliciesResourceWithRawResponse:
    def __init__(self, network_policies: NetworkPoliciesResource) -> None:
        self._network_policies = network_policies

        self.create = to_raw_response_wrapper(
            network_policies.create,
        )
        self.retrieve = to_raw_response_wrapper(
            network_policies.retrieve,
        )
        self.update = to_raw_response_wrapper(
            network_policies.update,
        )
        self.list = to_raw_response_wrapper(
            network_policies.list,
        )
        self.delete = to_raw_response_wrapper(
            network_policies.delete,
        )


class AsyncNetworkPoliciesResourceWithRawResponse:
    def __init__(self, network_policies: AsyncNetworkPoliciesResource) -> None:
        self._network_policies = network_policies

        self.create = async_to_raw_response_wrapper(
            network_policies.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            network_policies.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            network_policies.update,
        )
        self.list = async_to_raw_response_wrapper(
            network_policies.list,
        )
        self.delete = async_to_raw_response_wrapper(
            network_policies.delete,
        )


class NetworkPoliciesResourceWithStreamingResponse:
    def __init__(self, network_policies: NetworkPoliciesResource) -> None:
        self._network_policies = network_policies

        self.create = to_streamed_response_wrapper(
            network_policies.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            network_policies.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            network_policies.update,
        )
        self.list = to_streamed_response_wrapper(
            network_policies.list,
        )
        self.delete = to_streamed_response_wrapper(
            network_policies.delete,
        )


class AsyncNetworkPoliciesResourceWithStreamingResponse:
    def __init__(self, network_policies: AsyncNetworkPoliciesResource) -> None:
        self._network_policies = network_policies

        self.create = async_to_streamed_response_wrapper(
            network_policies.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            network_policies.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            network_policies.update,
        )
        self.list = async_to_streamed_response_wrapper(
            network_policies.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            network_policies.delete,
        )
