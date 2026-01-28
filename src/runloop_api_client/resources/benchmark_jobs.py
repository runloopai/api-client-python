# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import benchmark_job_list_params, benchmark_job_create_params
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
from ..types.benchmark_job_view import BenchmarkJobView
from ..types.benchmark_job_list_view import BenchmarkJobListView

__all__ = ["BenchmarkJobsResource", "AsyncBenchmarkJobsResource"]


class BenchmarkJobsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BenchmarkJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return BenchmarkJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BenchmarkJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return BenchmarkJobsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: Optional[str] | Omit = omit,
        spec: Optional[benchmark_job_create_params.Spec] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkJobView:
        """
        [Beta] Create a BenchmarkJob that runs a set of scenarios entirely on runloop.

        Args:
          name: The name of the BenchmarkJob. If not provided, name will be generated based on
              target dataset.

          spec: The job specification. Exactly one spec type must be set.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/benchmark_jobs",
            body=maybe_transform(
                {
                    "name": name,
                    "spec": spec,
                },
                benchmark_job_create_params.BenchmarkJobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkJobView,
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
    ) -> BenchmarkJobView:
        """
        [Beta] Get a BenchmarkJob given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/benchmark_jobs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BenchmarkJobView,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BenchmarkJobListView:
        """
        [Beta] List all BenchmarkJobs matching filter.

        Args:
          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/benchmark_jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    benchmark_job_list_params.BenchmarkJobListParams,
                ),
            ),
            cast_to=BenchmarkJobListView,
        )


class AsyncBenchmarkJobsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBenchmarkJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBenchmarkJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBenchmarkJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncBenchmarkJobsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: Optional[str] | Omit = omit,
        spec: Optional[benchmark_job_create_params.Spec] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkJobView:
        """
        [Beta] Create a BenchmarkJob that runs a set of scenarios entirely on runloop.

        Args:
          name: The name of the BenchmarkJob. If not provided, name will be generated based on
              target dataset.

          spec: The job specification. Exactly one spec type must be set.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/benchmark_jobs",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "spec": spec,
                },
                benchmark_job_create_params.BenchmarkJobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkJobView,
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
    ) -> BenchmarkJobView:
        """
        [Beta] Get a BenchmarkJob given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/benchmark_jobs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BenchmarkJobView,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BenchmarkJobListView:
        """
        [Beta] List all BenchmarkJobs matching filter.

        Args:
          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/benchmark_jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    benchmark_job_list_params.BenchmarkJobListParams,
                ),
            ),
            cast_to=BenchmarkJobListView,
        )


class BenchmarkJobsResourceWithRawResponse:
    def __init__(self, benchmark_jobs: BenchmarkJobsResource) -> None:
        self._benchmark_jobs = benchmark_jobs

        self.create = to_raw_response_wrapper(
            benchmark_jobs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            benchmark_jobs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            benchmark_jobs.list,
        )


class AsyncBenchmarkJobsResourceWithRawResponse:
    def __init__(self, benchmark_jobs: AsyncBenchmarkJobsResource) -> None:
        self._benchmark_jobs = benchmark_jobs

        self.create = async_to_raw_response_wrapper(
            benchmark_jobs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            benchmark_jobs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            benchmark_jobs.list,
        )


class BenchmarkJobsResourceWithStreamingResponse:
    def __init__(self, benchmark_jobs: BenchmarkJobsResource) -> None:
        self._benchmark_jobs = benchmark_jobs

        self.create = to_streamed_response_wrapper(
            benchmark_jobs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            benchmark_jobs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            benchmark_jobs.list,
        )


class AsyncBenchmarkJobsResourceWithStreamingResponse:
    def __init__(self, benchmark_jobs: AsyncBenchmarkJobsResource) -> None:
        self._benchmark_jobs = benchmark_jobs

        self.create = async_to_streamed_response_wrapper(
            benchmark_jobs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            benchmark_jobs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            benchmark_jobs.list,
        )
