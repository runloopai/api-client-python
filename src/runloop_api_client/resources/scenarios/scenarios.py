# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

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
    scenario_list_params,
    scenario_create_params,
    scenario_update_params,
    scenario_start_run_params,
    scenario_list_public_params,
)
from .scorers import (
    ScorersResource,
    AsyncScorersResource,
    ScorersResourceWithRawResponse,
    AsyncScorersResourceWithRawResponse,
    ScorersResourceWithStreamingResponse,
    AsyncScorersResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncScenariosCursorIDPage, AsyncScenariosCursorIDPage
from ...lib.polling import PollingConfig
from ..._base_client import AsyncPaginator, make_request_options
from ...types.scenario_view import ScenarioView
from ...types.scenario_run_view import ScenarioRunView
from ...types.input_context_param import InputContextParam
from ...types.scoring_contract_param import ScoringContractParam
from ...types.shared_params.run_profile import RunProfile
from ...types.input_context_update_param import InputContextUpdateParam
from ...types.scenario_environment_param import ScenarioEnvironmentParam
from ...types.scoring_contract_update_param import ScoringContractUpdateParam

__all__ = ["ScenariosResource", "AsyncScenariosResource"]


class ScenariosResource(SyncAPIResource):
    @cached_property
    def runs(self) -> RunsResource:
        return RunsResource(self._client)

    @cached_property
    def scorers(self) -> ScorersResource:
        return ScorersResource(self._client)

    @cached_property
    def with_raw_response(self) -> ScenariosResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return ScenariosResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScenariosResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return ScenariosResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        input_context: InputContextParam,
        name: str,
        scoring_contract: ScoringContractParam,
        environment_parameters: Optional[ScenarioEnvironmentParam] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        reference_output: Optional[str] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: Optional[SequenceNotStr[str]] | Omit = omit,
        validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScenarioView:
        """
        Create a Scenario, a repeatable AI coding evaluation test that defines the
        starting environment as well as evaluation success criteria.

        Args:
          input_context: The input context for the Scenario.

          name: Name of the scenario.

          scoring_contract: The scoring contract for the Scenario.

          environment_parameters: The Environment in which the Scenario will run.

          metadata: User defined metadata to attach to the scenario for organization.

          reference_output: A string representation of the reference output to solve the scenario. Commonly
              can be the result of a git diff or a sequence of command actions to apply to the
              environment.

          required_environment_variables: Environment variables required to run the scenario. If these variables are not
              provided, the scenario will fail to start.

          required_secret_names: Secrets required to run the scenario (user secret name to scenario required
              secret name). If these secrets are not provided or the mapping is incorrect, the
              scenario will fail to start.

          validation_type: Validation strategy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/scenarios",
            body=maybe_transform(
                {
                    "input_context": input_context,
                    "name": name,
                    "scoring_contract": scoring_contract,
                    "environment_parameters": environment_parameters,
                    "metadata": metadata,
                    "reference_output": reference_output,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
                    "validation_type": validation_type,
                },
                scenario_create_params.ScenarioCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScenarioView,
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
    ) -> ScenarioView:
        """
        Get a previously created scenario.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/scenarios/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScenarioView,
        )

    def update(
        self,
        id: str,
        *,
        environment_parameters: Optional[ScenarioEnvironmentParam] | Omit = omit,
        input_context: Optional[InputContextUpdateParam] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        reference_output: Optional[str] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: Optional[SequenceNotStr[str]] | Omit = omit,
        scoring_contract: Optional[ScoringContractUpdateParam] | Omit = omit,
        validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScenarioView:
        """
        Update a Scenario, a repeatable AI coding evaluation test that defines the
        starting environment as well as evaluation success criteria. Only provided
        fields will be updated.

        Args:
          environment_parameters: The Environment in which the Scenario will run.

          input_context: The input context for the Scenario.

          metadata: User defined metadata to attach to the scenario for organization.

          name: Name of the scenario.

          reference_output: A string representation of the reference output to solve the scenario. Commonly
              can be the result of a git diff or a sequence of command actions to apply to the
              environment.

          required_environment_variables: Environment variables required to run the scenario.

          required_secret_names: Secrets required to run the scenario.

          scoring_contract: The scoring contract for the Scenario.

          validation_type: Validation strategy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/scenarios/{id}",
            body=maybe_transform(
                {
                    "environment_parameters": environment_parameters,
                    "input_context": input_context,
                    "metadata": metadata,
                    "name": name,
                    "reference_output": reference_output,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
                    "scoring_contract": scoring_contract,
                    "validation_type": validation_type,
                },
                scenario_update_params.ScenarioUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScenarioView,
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
    ) -> SyncScenariosCursorIDPage[ScenarioView]:
        """
        List all Scenarios matching filter.

        Args:
          benchmark_id: Filter scenarios by benchmark ID.

          limit: The limit of items to return. Default is 20.

          name: Query for Scenarios with a given name.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/scenarios",
            page=SyncScenariosCursorIDPage[ScenarioView],
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
                    scenario_list_params.ScenarioListParams,
                ),
            ),
            model=ScenarioView,
        )

    def list_public(
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
    ) -> SyncScenariosCursorIDPage[ScenarioView]:
        """
        List all public scenarios matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          name: Query for Scenarios with a given name.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/scenarios/list_public",
            page=SyncScenariosCursorIDPage[ScenarioView],
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
                    scenario_list_public_params.ScenarioListPublicParams,
                ),
            ),
            model=ScenarioView,
        )

    def start_run(
        self,
        *,
        scenario_id: str,
        benchmark_run_id: Optional[str] | Omit = omit,
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
    ) -> ScenarioRunView:
        """
        Start a new ScenarioRun based on the provided Scenario.

        Args:
          scenario_id: ID of the Scenario to run.

          benchmark_run_id: Benchmark to associate the run.

          metadata: User defined metadata to attach to the run for organization.

          run_name: Display name of the run.

          run_profile: Runtime configuration to use for this benchmark run

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/scenarios/start_run",
            body=maybe_transform(
                {
                    "scenario_id": scenario_id,
                    "benchmark_run_id": benchmark_run_id,
                    "metadata": metadata,
                    "run_name": run_name,
                    "run_profile": run_profile,
                },
                scenario_start_run_params.ScenarioStartRunParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScenarioRunView,
        )

    def start_run_and_await_env_ready(
        self,
        *,
        scenario_id: str,
        benchmark_run_id: Optional[str] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        run_name: Optional[str] | NotGiven = NOT_GIVEN,
        run_profile: Optional[scenario_start_run_params.RunProfile] | NotGiven = NOT_GIVEN,
        polling_config: PollingConfig | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> ScenarioRunView:
        """Start a new ScenarioRun and wait for its environment to be ready.

        Args:
            scenario_id: ID of the Scenario to run
            benchmark_run_id: Benchmark to associate the run
            run_name: Display name of the run
            run_profile: Runtime configuration to use for this benchmark run
            polling_config: Optional polling configuration
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds
            idempotency_key: Specify a custom idempotency key for this request

        Returns:
            The scenario run in running state

        Raises:
            PollingTimeout: If polling times out before environment is ready
            RunloopError: If environment enters a non-running terminal state
        """
        run = self.start_run(
            scenario_id=scenario_id,
            benchmark_run_id=benchmark_run_id,
            metadata=metadata,
            run_name=run_name,
            run_profile=run_profile,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

        self._client.devboxes.await_running(
            run.devbox_id,
            polling_config=polling_config,
        )

        return run


class AsyncScenariosResource(AsyncAPIResource):
    @cached_property
    def runs(self) -> AsyncRunsResource:
        return AsyncRunsResource(self._client)

    @cached_property
    def scorers(self) -> AsyncScorersResource:
        return AsyncScorersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncScenariosResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncScenariosResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScenariosResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncScenariosResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        input_context: InputContextParam,
        name: str,
        scoring_contract: ScoringContractParam,
        environment_parameters: Optional[ScenarioEnvironmentParam] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        reference_output: Optional[str] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: Optional[SequenceNotStr[str]] | Omit = omit,
        validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScenarioView:
        """
        Create a Scenario, a repeatable AI coding evaluation test that defines the
        starting environment as well as evaluation success criteria.

        Args:
          input_context: The input context for the Scenario.

          name: Name of the scenario.

          scoring_contract: The scoring contract for the Scenario.

          environment_parameters: The Environment in which the Scenario will run.

          metadata: User defined metadata to attach to the scenario for organization.

          reference_output: A string representation of the reference output to solve the scenario. Commonly
              can be the result of a git diff or a sequence of command actions to apply to the
              environment.

          required_environment_variables: Environment variables required to run the scenario. If these variables are not
              provided, the scenario will fail to start.

          required_secret_names: Secrets required to run the scenario (user secret name to scenario required
              secret name). If these secrets are not provided or the mapping is incorrect, the
              scenario will fail to start.

          validation_type: Validation strategy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/scenarios",
            body=await async_maybe_transform(
                {
                    "input_context": input_context,
                    "name": name,
                    "scoring_contract": scoring_contract,
                    "environment_parameters": environment_parameters,
                    "metadata": metadata,
                    "reference_output": reference_output,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
                    "validation_type": validation_type,
                },
                scenario_create_params.ScenarioCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScenarioView,
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
    ) -> ScenarioView:
        """
        Get a previously created scenario.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/scenarios/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScenarioView,
        )

    async def update(
        self,
        id: str,
        *,
        environment_parameters: Optional[ScenarioEnvironmentParam] | Omit = omit,
        input_context: Optional[InputContextUpdateParam] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        reference_output: Optional[str] | Omit = omit,
        required_environment_variables: Optional[SequenceNotStr[str]] | Omit = omit,
        required_secret_names: Optional[SequenceNotStr[str]] | Omit = omit,
        scoring_contract: Optional[ScoringContractUpdateParam] | Omit = omit,
        validation_type: Optional[Literal["UNSPECIFIED", "FORWARD", "REVERSE", "EVALUATION"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScenarioView:
        """
        Update a Scenario, a repeatable AI coding evaluation test that defines the
        starting environment as well as evaluation success criteria. Only provided
        fields will be updated.

        Args:
          environment_parameters: The Environment in which the Scenario will run.

          input_context: The input context for the Scenario.

          metadata: User defined metadata to attach to the scenario for organization.

          name: Name of the scenario.

          reference_output: A string representation of the reference output to solve the scenario. Commonly
              can be the result of a git diff or a sequence of command actions to apply to the
              environment.

          required_environment_variables: Environment variables required to run the scenario.

          required_secret_names: Secrets required to run the scenario.

          scoring_contract: The scoring contract for the Scenario.

          validation_type: Validation strategy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/scenarios/{id}",
            body=await async_maybe_transform(
                {
                    "environment_parameters": environment_parameters,
                    "input_context": input_context,
                    "metadata": metadata,
                    "name": name,
                    "reference_output": reference_output,
                    "required_environment_variables": required_environment_variables,
                    "required_secret_names": required_secret_names,
                    "scoring_contract": scoring_contract,
                    "validation_type": validation_type,
                },
                scenario_update_params.ScenarioUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScenarioView,
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
    ) -> AsyncPaginator[ScenarioView, AsyncScenariosCursorIDPage[ScenarioView]]:
        """
        List all Scenarios matching filter.

        Args:
          benchmark_id: Filter scenarios by benchmark ID.

          limit: The limit of items to return. Default is 20.

          name: Query for Scenarios with a given name.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/scenarios",
            page=AsyncScenariosCursorIDPage[ScenarioView],
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
                    scenario_list_params.ScenarioListParams,
                ),
            ),
            model=ScenarioView,
        )

    def list_public(
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
    ) -> AsyncPaginator[ScenarioView, AsyncScenariosCursorIDPage[ScenarioView]]:
        """
        List all public scenarios matching filter.

        Args:
          limit: The limit of items to return. Default is 20.

          name: Query for Scenarios with a given name.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/scenarios/list_public",
            page=AsyncScenariosCursorIDPage[ScenarioView],
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
                    scenario_list_public_params.ScenarioListPublicParams,
                ),
            ),
            model=ScenarioView,
        )

    async def start_run(
        self,
        *,
        scenario_id: str,
        benchmark_run_id: Optional[str] | Omit = omit,
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
    ) -> ScenarioRunView:
        """
        Start a new ScenarioRun based on the provided Scenario.

        Args:
          scenario_id: ID of the Scenario to run.

          benchmark_run_id: Benchmark to associate the run.

          metadata: User defined metadata to attach to the run for organization.

          run_name: Display name of the run.

          run_profile: Runtime configuration to use for this benchmark run

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/scenarios/start_run",
            body=await async_maybe_transform(
                {
                    "scenario_id": scenario_id,
                    "benchmark_run_id": benchmark_run_id,
                    "metadata": metadata,
                    "run_name": run_name,
                    "run_profile": run_profile,
                },
                scenario_start_run_params.ScenarioStartRunParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScenarioRunView,
        )

    async def start_run_and_await_env_ready(
        self,
        scenario_id: str,
        benchmark_run_id: Optional[str] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        run_name: Optional[str] | NotGiven = NOT_GIVEN,
        run_profile: Optional[scenario_start_run_params.RunProfile] | NotGiven = NOT_GIVEN,
        polling_config: PollingConfig | None = None,
    ) -> ScenarioRunView:
        """Start a new ScenarioRun and wait for its environment to be ready.

        Args:
            scenario_id: ID of the Scenario to run
            benchmark_run_id: Benchmark to associate the run
            run_name: Display name of the run
            run_profile: Runtime configuration to use for this benchmark run
            polling_config: Optional polling configuration

        Returns:
            The scenario run in running state

        Raises:
            PollingTimeout: If polling times out before environment is ready
            RunloopError: If environment enters a non-running terminal state
        """
        run = await self.start_run(
            scenario_id=scenario_id,
            benchmark_run_id=benchmark_run_id,
            metadata=metadata,
            run_name=run_name,
            run_profile=run_profile,
        )

        await self._client.devboxes.await_running(
            run.devbox_id,
            polling_config=polling_config,
        )

        return run


class ScenariosResourceWithRawResponse:
    def __init__(self, scenarios: ScenariosResource) -> None:
        self._scenarios = scenarios

        self.create = to_raw_response_wrapper(
            scenarios.create,
        )
        self.retrieve = to_raw_response_wrapper(
            scenarios.retrieve,
        )
        self.update = to_raw_response_wrapper(
            scenarios.update,
        )
        self.list = to_raw_response_wrapper(
            scenarios.list,
        )
        self.list_public = to_raw_response_wrapper(
            scenarios.list_public,
        )
        self.start_run = to_raw_response_wrapper(
            scenarios.start_run,
        )

    @cached_property
    def runs(self) -> RunsResourceWithRawResponse:
        return RunsResourceWithRawResponse(self._scenarios.runs)

    @cached_property
    def scorers(self) -> ScorersResourceWithRawResponse:
        return ScorersResourceWithRawResponse(self._scenarios.scorers)


class AsyncScenariosResourceWithRawResponse:
    def __init__(self, scenarios: AsyncScenariosResource) -> None:
        self._scenarios = scenarios

        self.create = async_to_raw_response_wrapper(
            scenarios.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            scenarios.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            scenarios.update,
        )
        self.list = async_to_raw_response_wrapper(
            scenarios.list,
        )
        self.list_public = async_to_raw_response_wrapper(
            scenarios.list_public,
        )
        self.start_run = async_to_raw_response_wrapper(
            scenarios.start_run,
        )

    @cached_property
    def runs(self) -> AsyncRunsResourceWithRawResponse:
        return AsyncRunsResourceWithRawResponse(self._scenarios.runs)

    @cached_property
    def scorers(self) -> AsyncScorersResourceWithRawResponse:
        return AsyncScorersResourceWithRawResponse(self._scenarios.scorers)


class ScenariosResourceWithStreamingResponse:
    def __init__(self, scenarios: ScenariosResource) -> None:
        self._scenarios = scenarios

        self.create = to_streamed_response_wrapper(
            scenarios.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            scenarios.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            scenarios.update,
        )
        self.list = to_streamed_response_wrapper(
            scenarios.list,
        )
        self.list_public = to_streamed_response_wrapper(
            scenarios.list_public,
        )
        self.start_run = to_streamed_response_wrapper(
            scenarios.start_run,
        )

    @cached_property
    def runs(self) -> RunsResourceWithStreamingResponse:
        return RunsResourceWithStreamingResponse(self._scenarios.runs)

    @cached_property
    def scorers(self) -> ScorersResourceWithStreamingResponse:
        return ScorersResourceWithStreamingResponse(self._scenarios.scorers)


class AsyncScenariosResourceWithStreamingResponse:
    def __init__(self, scenarios: AsyncScenariosResource) -> None:
        self._scenarios = scenarios

        self.create = async_to_streamed_response_wrapper(
            scenarios.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            scenarios.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            scenarios.update,
        )
        self.list = async_to_streamed_response_wrapper(
            scenarios.list,
        )
        self.list_public = async_to_streamed_response_wrapper(
            scenarios.list_public,
        )
        self.start_run = async_to_streamed_response_wrapper(
            scenarios.start_run,
        )

    @cached_property
    def runs(self) -> AsyncRunsResourceWithStreamingResponse:
        return AsyncRunsResourceWithStreamingResponse(self._scenarios.runs)

    @cached_property
    def scorers(self) -> AsyncScorersResourceWithStreamingResponse:
        return AsyncScorersResourceWithStreamingResponse(self._scenarios.scorers)
