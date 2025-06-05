# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import repository_list_params, repository_create_params, repository_refresh_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncRepositoriesCursorIDPage, AsyncRepositoriesCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.repository_connection_view import RepositoryConnectionView
from ..types.repository_inspection_list_view import RepositoryInspectionListView

__all__ = ["RepositoriesResource", "AsyncRepositoriesResource"]


class RepositoriesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RepositoriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return RepositoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RepositoriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return RepositoriesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        owner: str,
        blueprint_id: Optional[str] | NotGiven = NOT_GIVEN,
        github_auth_token: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> RepositoryConnectionView:
        """
        Create a connection to a Github Repository and trigger an initial inspection of
        the repo's technical stack and developer environment requirements.

        Args:
          name: Name of the repository.

          owner: Account owner of the repository.

          blueprint_id: ID of blueprint to use as base for resulting RepositoryVersion blueprint.

          github_auth_token: GitHub authentication token for accessing private repositories.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/repositories",
            body=maybe_transform(
                {
                    "name": name,
                    "owner": owner,
                    "blueprint_id": blueprint_id,
                    "github_auth_token": github_auth_token,
                },
                repository_create_params.RepositoryCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=RepositoryConnectionView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RepositoryConnectionView:
        """
        Get Repository Connection details including latest inspection status and
        generated repository insights.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/repositories/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RepositoryConnectionView,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        owner: str | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncRepositoriesCursorIDPage[RepositoryConnectionView]:
        """
        List all available repository connections.

        Args:
          limit: The limit of items to return. Default is 20.

          name: Filter by repository name

          owner: Filter by repository owner

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/repositories",
            page=SyncRepositoriesCursorIDPage[RepositoryConnectionView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "owner": owner,
                        "starting_after": starting_after,
                    },
                    repository_list_params.RepositoryListParams,
                ),
            ),
            model=RepositoryConnectionView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Permanently Delete a Repository Connection including any automatically generated
        inspection insights.

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
            f"/v1/repositories/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def list_inspections(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RepositoryInspectionListView:
        """
        List all inspections of a repository connection including automatically
        generated insights for each inspection.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/repositories/{id}/inspections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RepositoryInspectionListView,
        )

    def refresh(
        self,
        id: str,
        *,
        blueprint_id: Optional[str] | NotGiven = NOT_GIVEN,
        github_auth_token: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Refresh a repository connection by inspecting the latest version including
        repo's technical stack and developer environment requirements.

        Args:
          blueprint_id: ID of blueprint to use as base for resulting RepositoryVersion blueprint.

          github_auth_token: GitHub authentication token for accessing private repositories.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/repositories/{id}/refresh",
            body=maybe_transform(
                {
                    "blueprint_id": blueprint_id,
                    "github_auth_token": github_auth_token,
                },
                repository_refresh_params.RepositoryRefreshParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )


class AsyncRepositoriesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRepositoriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRepositoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRepositoriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncRepositoriesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        owner: str,
        blueprint_id: Optional[str] | NotGiven = NOT_GIVEN,
        github_auth_token: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> RepositoryConnectionView:
        """
        Create a connection to a Github Repository and trigger an initial inspection of
        the repo's technical stack and developer environment requirements.

        Args:
          name: Name of the repository.

          owner: Account owner of the repository.

          blueprint_id: ID of blueprint to use as base for resulting RepositoryVersion blueprint.

          github_auth_token: GitHub authentication token for accessing private repositories.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/repositories",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "owner": owner,
                    "blueprint_id": blueprint_id,
                    "github_auth_token": github_auth_token,
                },
                repository_create_params.RepositoryCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=RepositoryConnectionView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RepositoryConnectionView:
        """
        Get Repository Connection details including latest inspection status and
        generated repository insights.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/repositories/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RepositoryConnectionView,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        owner: str | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[RepositoryConnectionView, AsyncRepositoriesCursorIDPage[RepositoryConnectionView]]:
        """
        List all available repository connections.

        Args:
          limit: The limit of items to return. Default is 20.

          name: Filter by repository name

          owner: Filter by repository owner

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/repositories",
            page=AsyncRepositoriesCursorIDPage[RepositoryConnectionView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "owner": owner,
                        "starting_after": starting_after,
                    },
                    repository_list_params.RepositoryListParams,
                ),
            ),
            model=RepositoryConnectionView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Permanently Delete a Repository Connection including any automatically generated
        inspection insights.

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
            f"/v1/repositories/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    async def list_inspections(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RepositoryInspectionListView:
        """
        List all inspections of a repository connection including automatically
        generated insights for each inspection.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/repositories/{id}/inspections",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RepositoryInspectionListView,
        )

    async def refresh(
        self,
        id: str,
        *,
        blueprint_id: Optional[str] | NotGiven = NOT_GIVEN,
        github_auth_token: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Refresh a repository connection by inspecting the latest version including
        repo's technical stack and developer environment requirements.

        Args:
          blueprint_id: ID of blueprint to use as base for resulting RepositoryVersion blueprint.

          github_auth_token: GitHub authentication token for accessing private repositories.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/repositories/{id}/refresh",
            body=await async_maybe_transform(
                {
                    "blueprint_id": blueprint_id,
                    "github_auth_token": github_auth_token,
                },
                repository_refresh_params.RepositoryRefreshParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )


class RepositoriesResourceWithRawResponse:
    def __init__(self, repositories: RepositoriesResource) -> None:
        self._repositories = repositories

        self.create = to_raw_response_wrapper(
            repositories.create,
        )
        self.retrieve = to_raw_response_wrapper(
            repositories.retrieve,
        )
        self.list = to_raw_response_wrapper(
            repositories.list,
        )
        self.delete = to_raw_response_wrapper(
            repositories.delete,
        )
        self.list_inspections = to_raw_response_wrapper(
            repositories.list_inspections,
        )
        self.refresh = to_raw_response_wrapper(
            repositories.refresh,
        )


class AsyncRepositoriesResourceWithRawResponse:
    def __init__(self, repositories: AsyncRepositoriesResource) -> None:
        self._repositories = repositories

        self.create = async_to_raw_response_wrapper(
            repositories.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            repositories.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            repositories.list,
        )
        self.delete = async_to_raw_response_wrapper(
            repositories.delete,
        )
        self.list_inspections = async_to_raw_response_wrapper(
            repositories.list_inspections,
        )
        self.refresh = async_to_raw_response_wrapper(
            repositories.refresh,
        )


class RepositoriesResourceWithStreamingResponse:
    def __init__(self, repositories: RepositoriesResource) -> None:
        self._repositories = repositories

        self.create = to_streamed_response_wrapper(
            repositories.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            repositories.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            repositories.list,
        )
        self.delete = to_streamed_response_wrapper(
            repositories.delete,
        )
        self.list_inspections = to_streamed_response_wrapper(
            repositories.list_inspections,
        )
        self.refresh = to_streamed_response_wrapper(
            repositories.refresh,
        )


class AsyncRepositoriesResourceWithStreamingResponse:
    def __init__(self, repositories: AsyncRepositoriesResource) -> None:
        self._repositories = repositories

        self.create = async_to_streamed_response_wrapper(
            repositories.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            repositories.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            repositories.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            repositories.delete,
        )
        self.list_inspections = async_to_streamed_response_wrapper(
            repositories.list_inspections,
        )
        self.refresh = async_to_streamed_response_wrapper(
            repositories.refresh,
        )
