# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx

from .runs import (
    RunsResource,
    AsyncRunsResource,
    RunsResourceWithRawResponse,
    AsyncRunsResourceWithRawResponse,
    RunsResourceWithStreamingResponse,
    AsyncRunsResourceWithStreamingResponse,
)
from ...types import benchmark_list_params, benchmark_create_params, benchmark_start_run_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.benchmark_view import BenchmarkView
from ...types.benchmark_run_view import BenchmarkRunView
from ...types.benchmark_list_view import BenchmarkListView

__all__ = ["BenchmarksResource", "AsyncBenchmarksResource"]


class BenchmarksResource(SyncAPIResource):
    @cached_property
    def runs(self) -> RunsResource:
        return RunsResource(self._client)

    @cached_property
    def with_raw_response(self) -> BenchmarksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return BenchmarksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BenchmarksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return BenchmarksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        scenario_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BenchmarkView:
        """
        Create a Benchmark with a set of Scenarios.

        Args:
          name: The name of the Benchmark.

          scenario_ids: The Scenario IDs that make up the Benchmark.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/benchmarks",
            body=maybe_transform(
                {
                    "name": name,
                    "scenario_ids": scenario_ids,
                },
                benchmark_create_params.BenchmarkCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkView,
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
    ) -> BenchmarkView:
        """
        Get a previously created Benchmark.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/benchmarks/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BenchmarkView,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        public: bool | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BenchmarkListView:
        """
        List all Benchmarks matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          public: List public benchmarks, e.g. SWE-bench. Defaults to false, i.e. only
              user-defined benchmarks are listed.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/benchmarks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "public": public,
                        "starting_after": starting_after,
                    },
                    benchmark_list_params.BenchmarkListParams,
                ),
            ),
            cast_to=BenchmarkListView,
        )

    def start_run(
        self,
        *,
        benchmark_id: str,
        run_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BenchmarkRunView:
        """
        Start a new BenchmarkRun based on the provided Benchmark.

        Args:
          benchmark_id: ID of the Benchmark to run.

          run_name: Display name of the run.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/benchmarks/start_run",
            body=maybe_transform(
                {
                    "benchmark_id": benchmark_id,
                    "run_name": run_name,
                },
                benchmark_start_run_params.BenchmarkStartRunParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkRunView,
        )


class AsyncBenchmarksResource(AsyncAPIResource):
    @cached_property
    def runs(self) -> AsyncRunsResource:
        return AsyncRunsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBenchmarksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBenchmarksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBenchmarksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncBenchmarksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        scenario_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BenchmarkView:
        """
        Create a Benchmark with a set of Scenarios.

        Args:
          name: The name of the Benchmark.

          scenario_ids: The Scenario IDs that make up the Benchmark.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/benchmarks",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "scenario_ids": scenario_ids,
                },
                benchmark_create_params.BenchmarkCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkView,
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
    ) -> BenchmarkView:
        """
        Get a previously created Benchmark.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/benchmarks/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BenchmarkView,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        public: bool | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BenchmarkListView:
        """
        List all Benchmarks matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          public: List public benchmarks, e.g. SWE-bench. Defaults to false, i.e. only
              user-defined benchmarks are listed.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/benchmarks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "public": public,
                        "starting_after": starting_after,
                    },
                    benchmark_list_params.BenchmarkListParams,
                ),
            ),
            cast_to=BenchmarkListView,
        )

    async def start_run(
        self,
        *,
        benchmark_id: str,
        run_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BenchmarkRunView:
        """
        Start a new BenchmarkRun based on the provided Benchmark.

        Args:
          benchmark_id: ID of the Benchmark to run.

          run_name: Display name of the run.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/benchmarks/start_run",
            body=await async_maybe_transform(
                {
                    "benchmark_id": benchmark_id,
                    "run_name": run_name,
                },
                benchmark_start_run_params.BenchmarkStartRunParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkRunView,
        )


class BenchmarksResourceWithRawResponse:
    def __init__(self, benchmarks: BenchmarksResource) -> None:
        self._benchmarks = benchmarks

        self.create = to_raw_response_wrapper(
            benchmarks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            benchmarks.retrieve,
        )
        self.list = to_raw_response_wrapper(
            benchmarks.list,
        )
        self.start_run = to_raw_response_wrapper(
            benchmarks.start_run,
        )

    @cached_property
    def runs(self) -> RunsResourceWithRawResponse:
        return RunsResourceWithRawResponse(self._benchmarks.runs)


class AsyncBenchmarksResourceWithRawResponse:
    def __init__(self, benchmarks: AsyncBenchmarksResource) -> None:
        self._benchmarks = benchmarks

        self.create = async_to_raw_response_wrapper(
            benchmarks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            benchmarks.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            benchmarks.list,
        )
        self.start_run = async_to_raw_response_wrapper(
            benchmarks.start_run,
        )

    @cached_property
    def runs(self) -> AsyncRunsResourceWithRawResponse:
        return AsyncRunsResourceWithRawResponse(self._benchmarks.runs)


class BenchmarksResourceWithStreamingResponse:
    def __init__(self, benchmarks: BenchmarksResource) -> None:
        self._benchmarks = benchmarks

        self.create = to_streamed_response_wrapper(
            benchmarks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            benchmarks.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            benchmarks.list,
        )
        self.start_run = to_streamed_response_wrapper(
            benchmarks.start_run,
        )

    @cached_property
    def runs(self) -> RunsResourceWithStreamingResponse:
        return RunsResourceWithStreamingResponse(self._benchmarks.runs)


class AsyncBenchmarksResourceWithStreamingResponse:
    def __init__(self, benchmarks: AsyncBenchmarksResource) -> None:
        self._benchmarks = benchmarks

        self.create = async_to_streamed_response_wrapper(
            benchmarks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            benchmarks.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            benchmarks.list,
        )
        self.start_run = async_to_streamed_response_wrapper(
            benchmarks.start_run,
        )

    @cached_property
    def runs(self) -> AsyncRunsResourceWithStreamingResponse:
        return AsyncRunsResourceWithStreamingResponse(self._benchmarks.runs)
