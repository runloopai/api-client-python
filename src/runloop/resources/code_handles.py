# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import code_handle_list_params, code_handle_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)
from ..types.code_handle import CodeHandle
from ..types.code_handle_list import CodeHandleList

__all__ = ["CodeHandlesResource", "AsyncCodeHandlesResource"]


class CodeHandlesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CodeHandlesResourceWithRawResponse:
        return CodeHandlesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CodeHandlesResourceWithStreamingResponse:
        return CodeHandlesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        auth_token: str | NotGiven = NOT_GIVEN,
        branch: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        owner: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CodeHandle:
        """Create a new code handle for a given repository.

        This can be referenced in other
        parts of the system to refer to a specific version of a repository.

        Args:
          auth_token: A short lived, scoped authentication token.

          branch: Branch or tag to checkout instead of main.

          name: The name of the code repository.

          owner: The account that owns the repository.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/code_handles",
            body=maybe_transform(
                {
                    "auth_token": auth_token,
                    "branch": branch,
                    "name": name,
                    "owner": owner,
                },
                code_handle_create_params.CodeHandleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CodeHandle,
        )

    def list(
        self,
        *,
        owner: str | NotGiven = NOT_GIVEN,
        repo_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CodeHandleList:
        """
        List the code handles that are available for use.

        Args:
          owner: Repo owner name.

          repo_name: Repo name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/code_handles",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "owner": owner,
                        "repo_name": repo_name,
                    },
                    code_handle_list_params.CodeHandleListParams,
                ),
            ),
            cast_to=CodeHandleList,
        )


class AsyncCodeHandlesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCodeHandlesResourceWithRawResponse:
        return AsyncCodeHandlesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCodeHandlesResourceWithStreamingResponse:
        return AsyncCodeHandlesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        auth_token: str | NotGiven = NOT_GIVEN,
        branch: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        owner: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CodeHandle:
        """Create a new code handle for a given repository.

        This can be referenced in other
        parts of the system to refer to a specific version of a repository.

        Args:
          auth_token: A short lived, scoped authentication token.

          branch: Branch or tag to checkout instead of main.

          name: The name of the code repository.

          owner: The account that owns the repository.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/code_handles",
            body=await async_maybe_transform(
                {
                    "auth_token": auth_token,
                    "branch": branch,
                    "name": name,
                    "owner": owner,
                },
                code_handle_create_params.CodeHandleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CodeHandle,
        )

    async def list(
        self,
        *,
        owner: str | NotGiven = NOT_GIVEN,
        repo_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CodeHandleList:
        """
        List the code handles that are available for use.

        Args:
          owner: Repo owner name.

          repo_name: Repo name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/code_handles",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "owner": owner,
                        "repo_name": repo_name,
                    },
                    code_handle_list_params.CodeHandleListParams,
                ),
            ),
            cast_to=CodeHandleList,
        )


class CodeHandlesResourceWithRawResponse:
    def __init__(self, code_handles: CodeHandlesResource) -> None:
        self._code_handles = code_handles

        self.create = to_raw_response_wrapper(
            code_handles.create,
        )
        self.list = to_raw_response_wrapper(
            code_handles.list,
        )


class AsyncCodeHandlesResourceWithRawResponse:
    def __init__(self, code_handles: AsyncCodeHandlesResource) -> None:
        self._code_handles = code_handles

        self.create = async_to_raw_response_wrapper(
            code_handles.create,
        )
        self.list = async_to_raw_response_wrapper(
            code_handles.list,
        )


class CodeHandlesResourceWithStreamingResponse:
    def __init__(self, code_handles: CodeHandlesResource) -> None:
        self._code_handles = code_handles

        self.create = to_streamed_response_wrapper(
            code_handles.create,
        )
        self.list = to_streamed_response_wrapper(
            code_handles.list,
        )


class AsyncCodeHandlesResourceWithStreamingResponse:
    def __init__(self, code_handles: AsyncCodeHandlesResource) -> None:
        self._code_handles = code_handles

        self.create = async_to_streamed_response_wrapper(
            code_handles.create,
        )
        self.list = async_to_streamed_response_wrapper(
            code_handles.list,
        )
