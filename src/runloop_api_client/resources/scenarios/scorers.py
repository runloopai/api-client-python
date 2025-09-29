# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncScenarioScorersCursorIDPage, AsyncScenarioScorersCursorIDPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.scenarios import scorer_list_params, scorer_create_params, scorer_update_params, scorer_validate_params
from ...types.scenario_environment_param import ScenarioEnvironmentParam
from ...types.scenarios.scorer_list_response import ScorerListResponse
from ...types.scenarios.scorer_create_response import ScorerCreateResponse
from ...types.scenarios.scorer_update_response import ScorerUpdateResponse
from ...types.scenarios.scorer_retrieve_response import ScorerRetrieveResponse
from ...types.scenarios.scorer_validate_response import ScorerValidateResponse

__all__ = ["ScorersResource", "AsyncScorersResource"]


class ScorersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ScorersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return ScorersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScorersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return ScorersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        bash_script: str,
        type: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerCreateResponse:
        """
        Create a custom scenario scorer.

        Args:
          bash_script: Bash script for the custom scorer taking context as a json object
              $RL_SCORER_CONTEXT.

          type: Name of the type of custom scorer.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/scenarios/scorers",
            body=maybe_transform(
                {
                    "bash_script": bash_script,
                    "type": type,
                },
                scorer_create_params.ScorerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerCreateResponse,
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
    ) -> ScorerRetrieveResponse:
        """
        Retrieve Scenario Scorer.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/scenarios/scorers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScorerRetrieveResponse,
        )

    def update(
        self,
        id: str,
        *,
        bash_script: str,
        type: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerUpdateResponse:
        """
        Update a scenario scorer.

        Args:
          bash_script: Bash script for the custom scorer taking context as a json object
              $RL_SCORER_CONTEXT.

          type: Name of the type of custom scorer.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/scenarios/scorers/{id}",
            body=maybe_transform(
                {
                    "bash_script": bash_script,
                    "type": type,
                },
                scorer_update_params.ScorerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerUpdateResponse,
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
    ) -> SyncScenarioScorersCursorIDPage[ScorerListResponse]:
        """
        List all Scenario Scorers matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/scenarios/scorers",
            page=SyncScenarioScorersCursorIDPage[ScorerListResponse],
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
                    scorer_list_params.ScorerListParams,
                ),
            ),
            model=ScorerListResponse,
        )

    def validate(
        self,
        id: str,
        *,
        scoring_context: object,
        environment_parameters: ScenarioEnvironmentParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerValidateResponse:
        """
        Validate a scenario scorer.

        Args:
          scoring_context: Json context that gets passed to the custom scorer

          environment_parameters: The Environment in which the Scenario will run.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/scenarios/scorers/{id}/validate",
            body=maybe_transform(
                {
                    "scoring_context": scoring_context,
                    "environment_parameters": environment_parameters,
                },
                scorer_validate_params.ScorerValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerValidateResponse,
        )


class AsyncScorersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncScorersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncScorersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScorersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncScorersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        bash_script: str,
        type: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerCreateResponse:
        """
        Create a custom scenario scorer.

        Args:
          bash_script: Bash script for the custom scorer taking context as a json object
              $RL_SCORER_CONTEXT.

          type: Name of the type of custom scorer.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/scenarios/scorers",
            body=await async_maybe_transform(
                {
                    "bash_script": bash_script,
                    "type": type,
                },
                scorer_create_params.ScorerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerCreateResponse,
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
    ) -> ScorerRetrieveResponse:
        """
        Retrieve Scenario Scorer.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/scenarios/scorers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScorerRetrieveResponse,
        )

    async def update(
        self,
        id: str,
        *,
        bash_script: str,
        type: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerUpdateResponse:
        """
        Update a scenario scorer.

        Args:
          bash_script: Bash script for the custom scorer taking context as a json object
              $RL_SCORER_CONTEXT.

          type: Name of the type of custom scorer.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/scenarios/scorers/{id}",
            body=await async_maybe_transform(
                {
                    "bash_script": bash_script,
                    "type": type,
                },
                scorer_update_params.ScorerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerUpdateResponse,
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
    ) -> AsyncPaginator[ScorerListResponse, AsyncScenarioScorersCursorIDPage[ScorerListResponse]]:
        """
        List all Scenario Scorers matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/scenarios/scorers",
            page=AsyncScenarioScorersCursorIDPage[ScorerListResponse],
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
                    scorer_list_params.ScorerListParams,
                ),
            ),
            model=ScorerListResponse,
        )

    async def validate(
        self,
        id: str,
        *,
        scoring_context: object,
        environment_parameters: ScenarioEnvironmentParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerValidateResponse:
        """
        Validate a scenario scorer.

        Args:
          scoring_context: Json context that gets passed to the custom scorer

          environment_parameters: The Environment in which the Scenario will run.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/scenarios/scorers/{id}/validate",
            body=await async_maybe_transform(
                {
                    "scoring_context": scoring_context,
                    "environment_parameters": environment_parameters,
                },
                scorer_validate_params.ScorerValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerValidateResponse,
        )


class ScorersResourceWithRawResponse:
    def __init__(self, scorers: ScorersResource) -> None:
        self._scorers = scorers

        self.create = to_raw_response_wrapper(
            scorers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            scorers.retrieve,
        )
        self.update = to_raw_response_wrapper(
            scorers.update,
        )
        self.list = to_raw_response_wrapper(
            scorers.list,
        )
        self.validate = to_raw_response_wrapper(
            scorers.validate,
        )


class AsyncScorersResourceWithRawResponse:
    def __init__(self, scorers: AsyncScorersResource) -> None:
        self._scorers = scorers

        self.create = async_to_raw_response_wrapper(
            scorers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            scorers.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            scorers.update,
        )
        self.list = async_to_raw_response_wrapper(
            scorers.list,
        )
        self.validate = async_to_raw_response_wrapper(
            scorers.validate,
        )


class ScorersResourceWithStreamingResponse:
    def __init__(self, scorers: ScorersResource) -> None:
        self._scorers = scorers

        self.create = to_streamed_response_wrapper(
            scorers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            scorers.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            scorers.update,
        )
        self.list = to_streamed_response_wrapper(
            scorers.list,
        )
        self.validate = to_streamed_response_wrapper(
            scorers.validate,
        )


class AsyncScorersResourceWithStreamingResponse:
    def __init__(self, scorers: AsyncScorersResource) -> None:
        self._scorers = scorers

        self.create = async_to_streamed_response_wrapper(
            scorers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            scorers.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            scorers.update,
        )
        self.list = async_to_streamed_response_wrapper(
            scorers.list,
        )
        self.validate = async_to_streamed_response_wrapper(
            scorers.validate,
        )
