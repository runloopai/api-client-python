# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from .runs import (
    RunsResource,
    AsyncRunsResource,
    RunsResourceWithRawResponse,
    AsyncRunsResourceWithRawResponse,
    RunsResourceWithStreamingResponse,
    AsyncRunsResourceWithStreamingResponse,
)
from ...types import (
    benchmark_list_params,
    benchmark_create_params,
    benchmark_update_params,
    benchmark_start_run_params,
    benchmark_definitions_params,
    benchmark_list_public_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncBenchmarksCursorIDPage, AsyncBenchmarksCursorIDPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.benchmark_view import BenchmarkView
from ...types.benchmark_run_view import BenchmarkRunView
from ...types.shared_params.run_profile import RunProfile
from ...types.scenario_definition_list_view import ScenarioDefinitionListView

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
        attribution: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: SequenceNotStr[str] | Omit = omit,
        scenario_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkView:
        """
        Create a Benchmark with a set of Scenarios.

        Args:
          name: The name of the Benchmark. This must be unique.

          attribution: Attribution information for the benchmark.

          description: Detailed description of the benchmark.

          metadata: User defined metadata to attach to the benchmark for organization.

          required_environment_variables: Environment variables required to run the benchmark. If any required variables
              are not supplied, the benchmark will fail to start

          required_secret_names: Secrets required to run the benchmark with (environment variable name will be
              mapped to the your user secret by name). If any of these secrets are not
              provided or the mapping is incorrect, the benchmark will fail to start.

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
                    "attribution": attribution,
                    "description": description,
                    "metadata": metadata,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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

    def update(
        self,
        id: str,
        *,
        name: str,
        attribution: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: SequenceNotStr[str] | Omit = omit,
        scenario_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkView:
        """
        Update a Benchmark with a set of Scenarios.

        Args:
          name: The name of the Benchmark. This must be unique.

          attribution: Attribution information for the benchmark.

          description: Detailed description of the benchmark.

          metadata: User defined metadata to attach to the benchmark for organization.

          required_environment_variables: Environment variables required to run the benchmark. If any required variables
              are not supplied, the benchmark will fail to start

          required_secret_names: Secrets required to run the benchmark with (environment variable name will be
              mapped to the your user secret by name). If any of these secrets are not
              provided or the mapping is incorrect, the benchmark will fail to start.

          scenario_ids: The Scenario IDs that make up the Benchmark.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/benchmarks/{id}",
            body=maybe_transform(
                {
                    "name": name,
                    "attribution": attribution,
                    "description": description,
                    "metadata": metadata,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
                    "scenario_ids": scenario_ids,
                },
                benchmark_update_params.BenchmarkUpdateParams,
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

    def list(
        self,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncBenchmarksCursorIDPage[BenchmarkView]:
        """
        List all Benchmarks matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/benchmarks",
            page=SyncBenchmarksCursorIDPage[BenchmarkView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    benchmark_list_params.BenchmarkListParams,
                ),
            ),
            model=BenchmarkView,
        )

    def definitions(
        self,
        id: str,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScenarioDefinitionListView:
        """
        Get scenario definitions for a previously created Benchmark.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/benchmarks/{id}/definitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    benchmark_definitions_params.BenchmarkDefinitionsParams,
                ),
            ),
            cast_to=ScenarioDefinitionListView,
        )

    def list_public(
        self,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncBenchmarksCursorIDPage[BenchmarkView]:
        """
        List all public benchmarks matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/benchmarks/list_public",
            page=SyncBenchmarksCursorIDPage[BenchmarkView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    benchmark_list_public_params.BenchmarkListPublicParams,
                ),
            ),
            model=BenchmarkView,
        )

    def start_run(
        self,
        *,
        benchmark_id: str,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        run_name: Optional[str] | Omit = omit,
        run_profile: Optional[RunProfile] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkRunView:
        """
        Start a new BenchmarkRun based on the provided Benchmark.

        Args:
          benchmark_id: ID of the Benchmark to run.

          metadata: User defined metadata to attach to the benchmark run for organization.

          run_name: Display name of the run.

          run_profile: Runtime configuration to use for this benchmark run

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
                    "metadata": metadata,
                    "run_name": run_name,
                    "run_profile": run_profile,
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
        attribution: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: SequenceNotStr[str] | Omit = omit,
        scenario_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkView:
        """
        Create a Benchmark with a set of Scenarios.

        Args:
          name: The name of the Benchmark. This must be unique.

          attribution: Attribution information for the benchmark.

          description: Detailed description of the benchmark.

          metadata: User defined metadata to attach to the benchmark for organization.

          required_environment_variables: Environment variables required to run the benchmark. If any required variables
              are not supplied, the benchmark will fail to start

          required_secret_names: Secrets required to run the benchmark with (environment variable name will be
              mapped to the your user secret by name). If any of these secrets are not
              provided or the mapping is incorrect, the benchmark will fail to start.

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
                    "attribution": attribution,
                    "description": description,
                    "metadata": metadata,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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

    async def update(
        self,
        id: str,
        *,
        name: str,
        attribution: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: SequenceNotStr[str] | Omit = omit,
        scenario_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkView:
        """
        Update a Benchmark with a set of Scenarios.

        Args:
          name: The name of the Benchmark. This must be unique.

          attribution: Attribution information for the benchmark.

          description: Detailed description of the benchmark.

          metadata: User defined metadata to attach to the benchmark for organization.

          required_environment_variables: Environment variables required to run the benchmark. If any required variables
              are not supplied, the benchmark will fail to start

          required_secret_names: Secrets required to run the benchmark with (environment variable name will be
              mapped to the your user secret by name). If any of these secrets are not
              provided or the mapping is incorrect, the benchmark will fail to start.

          scenario_ids: The Scenario IDs that make up the Benchmark.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/benchmarks/{id}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "attribution": attribution,
                    "description": description,
                    "metadata": metadata,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
                    "scenario_ids": scenario_ids,
                },
                benchmark_update_params.BenchmarkUpdateParams,
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

    def list(
        self,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BenchmarkView, AsyncBenchmarksCursorIDPage[BenchmarkView]]:
        """
        List all Benchmarks matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/benchmarks",
            page=AsyncBenchmarksCursorIDPage[BenchmarkView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    benchmark_list_params.BenchmarkListParams,
                ),
            ),
            model=BenchmarkView,
        )

    async def definitions(
        self,
        id: str,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScenarioDefinitionListView:
        """
        Get scenario definitions for a previously created Benchmark.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/benchmarks/{id}/definitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    benchmark_definitions_params.BenchmarkDefinitionsParams,
                ),
            ),
            cast_to=ScenarioDefinitionListView,
        )

    def list_public(
        self,
        *,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BenchmarkView, AsyncBenchmarksCursorIDPage[BenchmarkView]]:
        """
        List all public benchmarks matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/benchmarks/list_public",
            page=AsyncBenchmarksCursorIDPage[BenchmarkView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    benchmark_list_public_params.BenchmarkListPublicParams,
                ),
            ),
            model=BenchmarkView,
        )

    async def start_run(
        self,
        *,
        benchmark_id: str,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        run_name: Optional[str] | Omit = omit,
        run_profile: Optional[RunProfile] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BenchmarkRunView:
        """
        Start a new BenchmarkRun based on the provided Benchmark.

        Args:
          benchmark_id: ID of the Benchmark to run.

          metadata: User defined metadata to attach to the benchmark run for organization.

          run_name: Display name of the run.

          run_profile: Runtime configuration to use for this benchmark run

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
                    "metadata": metadata,
                    "run_name": run_name,
                    "run_profile": run_profile,
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
        self.update = to_raw_response_wrapper(
            benchmarks.update,
        )
        self.list = to_raw_response_wrapper(
            benchmarks.list,
        )
        self.definitions = to_raw_response_wrapper(
            benchmarks.definitions,
        )
        self.list_public = to_raw_response_wrapper(
            benchmarks.list_public,
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
        self.update = async_to_raw_response_wrapper(
            benchmarks.update,
        )
        self.list = async_to_raw_response_wrapper(
            benchmarks.list,
        )
        self.definitions = async_to_raw_response_wrapper(
            benchmarks.definitions,
        )
        self.list_public = async_to_raw_response_wrapper(
            benchmarks.list_public,
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
        self.update = to_streamed_response_wrapper(
            benchmarks.update,
        )
        self.list = to_streamed_response_wrapper(
            benchmarks.list,
        )
        self.definitions = to_streamed_response_wrapper(
            benchmarks.definitions,
        )
        self.list_public = to_streamed_response_wrapper(
            benchmarks.list_public,
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
        self.update = async_to_streamed_response_wrapper(
            benchmarks.update,
        )
        self.list = async_to_streamed_response_wrapper(
            benchmarks.list,
        )
        self.definitions = async_to_streamed_response_wrapper(
            benchmarks.definitions,
        )
        self.list_public = async_to_streamed_response_wrapper(
            benchmarks.list_public,
        )
        self.start_run = async_to_streamed_response_wrapper(
            benchmarks.start_run,
        )

    @cached_property
    def runs(self) -> AsyncRunsResourceWithStreamingResponse:
        return AsyncRunsResourceWithStreamingResponse(self._benchmarks.runs)
