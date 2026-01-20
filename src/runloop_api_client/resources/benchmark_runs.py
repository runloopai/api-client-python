# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import benchmark_run_list_params, benchmark_run_list_scenario_runs_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncBenchmarkRunsCursorIDPage, AsyncBenchmarkRunsCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.scenario_run_view import ScenarioRunView
from ..types.benchmark_run_view import BenchmarkRunView

__all__ = ["BenchmarkRunsResource", "AsyncBenchmarkRunsResource"]


class BenchmarkRunsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BenchmarkRunsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return BenchmarkRunsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BenchmarkRunsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return BenchmarkRunsResourceWithStreamingResponse(self)

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
    ) -> BenchmarkRunView:
        """
        Get a BenchmarkRun given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/benchmark_runs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BenchmarkRunView,
        )

    def list(
        self,
        *,
        benchmark_id: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncBenchmarkRunsCursorIDPage[BenchmarkRunView]:
        """
        List all BenchmarkRuns matching filter.

        Args:
          benchmark_id: The Benchmark ID to filter by.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/benchmark_runs",
            page=SyncBenchmarkRunsCursorIDPage[BenchmarkRunView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "benchmark_id": benchmark_id,
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    benchmark_run_list_params.BenchmarkRunListParams,
                ),
            ),
            model=BenchmarkRunView,
        )

    def cancel(
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
    ) -> BenchmarkRunView:
        """
        Cancel a currently running Benchmark run.

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
            f"/v1/benchmark_runs/{id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkRunView,
        )

    def complete(
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
    ) -> BenchmarkRunView:
        """
        Complete a currently running BenchmarkRun.

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
            f"/v1/benchmark_runs/{id}/complete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkRunView,
        )

    def list_scenario_runs(
        self,
        id: str,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        state: Literal["running", "scoring", "scored", "completed", "canceled", "timeout", "failed"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncBenchmarkRunsCursorIDPage[ScenarioRunView]:
        """
        List started scenario runs for a benchmark run.

        Args:
          limit: The limit of items to return. Default is 20. Max is 5000.

          starting_after: Load the next page of data starting after the item with the given ID.

          state: Filter by Scenario Run state

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            f"/v1/benchmark_runs/{id}/scenario_runs",
            page=SyncBenchmarkRunsCursorIDPage[ScenarioRunView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                        "state": state,
                    },
                    benchmark_run_list_scenario_runs_params.BenchmarkRunListScenarioRunsParams,
                ),
            ),
            model=ScenarioRunView,
        )


class AsyncBenchmarkRunsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBenchmarkRunsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBenchmarkRunsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBenchmarkRunsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncBenchmarkRunsResourceWithStreamingResponse(self)

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
    ) -> BenchmarkRunView:
        """
        Get a BenchmarkRun given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/benchmark_runs/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BenchmarkRunView,
        )

    def list(
        self,
        *,
        benchmark_id: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BenchmarkRunView, AsyncBenchmarkRunsCursorIDPage[BenchmarkRunView]]:
        """
        List all BenchmarkRuns matching filter.

        Args:
          benchmark_id: The Benchmark ID to filter by.

          limit: The limit of items to return. Default is 20. Max is 5000.

          name: Filter by name

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/benchmark_runs",
            page=AsyncBenchmarkRunsCursorIDPage[BenchmarkRunView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "benchmark_id": benchmark_id,
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    benchmark_run_list_params.BenchmarkRunListParams,
                ),
            ),
            model=BenchmarkRunView,
        )

    async def cancel(
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
    ) -> BenchmarkRunView:
        """
        Cancel a currently running Benchmark run.

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
            f"/v1/benchmark_runs/{id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkRunView,
        )

    async def complete(
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
    ) -> BenchmarkRunView:
        """
        Complete a currently running BenchmarkRun.

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
            f"/v1/benchmark_runs/{id}/complete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BenchmarkRunView,
        )

    def list_scenario_runs(
        self,
        id: str,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        state: Literal["running", "scoring", "scored", "completed", "canceled", "timeout", "failed"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ScenarioRunView, AsyncBenchmarkRunsCursorIDPage[ScenarioRunView]]:
        """
        List started scenario runs for a benchmark run.

        Args:
          limit: The limit of items to return. Default is 20. Max is 5000.

          starting_after: Load the next page of data starting after the item with the given ID.

          state: Filter by Scenario Run state

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            f"/v1/benchmark_runs/{id}/scenario_runs",
            page=AsyncBenchmarkRunsCursorIDPage[ScenarioRunView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                        "state": state,
                    },
                    benchmark_run_list_scenario_runs_params.BenchmarkRunListScenarioRunsParams,
                ),
            ),
            model=ScenarioRunView,
        )


class BenchmarkRunsResourceWithRawResponse:
    def __init__(self, benchmark_runs: BenchmarkRunsResource) -> None:
        self._benchmark_runs = benchmark_runs

        self.retrieve = to_raw_response_wrapper(
            benchmark_runs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            benchmark_runs.list,
        )
        self.cancel = to_raw_response_wrapper(
            benchmark_runs.cancel,
        )
        self.complete = to_raw_response_wrapper(
            benchmark_runs.complete,
        )
        self.list_scenario_runs = to_raw_response_wrapper(
            benchmark_runs.list_scenario_runs,
        )


class AsyncBenchmarkRunsResourceWithRawResponse:
    def __init__(self, benchmark_runs: AsyncBenchmarkRunsResource) -> None:
        self._benchmark_runs = benchmark_runs

        self.retrieve = async_to_raw_response_wrapper(
            benchmark_runs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            benchmark_runs.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            benchmark_runs.cancel,
        )
        self.complete = async_to_raw_response_wrapper(
            benchmark_runs.complete,
        )
        self.list_scenario_runs = async_to_raw_response_wrapper(
            benchmark_runs.list_scenario_runs,
        )


class BenchmarkRunsResourceWithStreamingResponse:
    def __init__(self, benchmark_runs: BenchmarkRunsResource) -> None:
        self._benchmark_runs = benchmark_runs

        self.retrieve = to_streamed_response_wrapper(
            benchmark_runs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            benchmark_runs.list,
        )
        self.cancel = to_streamed_response_wrapper(
            benchmark_runs.cancel,
        )
        self.complete = to_streamed_response_wrapper(
            benchmark_runs.complete,
        )
        self.list_scenario_runs = to_streamed_response_wrapper(
            benchmark_runs.list_scenario_runs,
        )


class AsyncBenchmarkRunsResourceWithStreamingResponse:
    def __init__(self, benchmark_runs: AsyncBenchmarkRunsResource) -> None:
        self._benchmark_runs = benchmark_runs

        self.retrieve = async_to_streamed_response_wrapper(
            benchmark_runs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            benchmark_runs.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            benchmark_runs.cancel,
        )
        self.complete = async_to_streamed_response_wrapper(
            benchmark_runs.complete,
        )
        self.list_scenario_runs = async_to_streamed_response_wrapper(
            benchmark_runs.list_scenario_runs,
        )
